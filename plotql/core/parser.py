"""
Parser for PlotQL DSL.

Grammar (simplified):
    query       := with_clause plot_clause [where_clause] [options_clause]
    with_clause := WITH string
    plot_clause := PLOT column AGAINST column [AS plot_type]
    where_clause := WHERE condition ((AND|OR) condition)*
    condition   := column op value
    options_clause := OPTIONS option (, option)*
    option      := key = value
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    Condition,
    ComparisonOp,
    FormatOptions,
    LogicalOp,
    PlotQuery,
    PlotSeries,
    PlotType,
    WhereClause,
)


class ParseError(Exception):
    """Raised when parsing fails."""
    def __init__(self, message: str, position: int = 0):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")


# Load grammar definitions from shared JSON
_GRAMMAR_PATH = Path(__file__).parent.parent / "grammar.json"
with open(_GRAMMAR_PATH) as f:
    _GRAMMAR = json.load(f)


@dataclass
class Token:
    """A lexical token."""
    type: str
    value: str
    position: int


class Lexer:
    """Tokenizer for PlotQL."""

    KEYWORDS = {kw.upper() for kw in _GRAMMAR["keywords"]}
    AGGREGATE_FUNCS = {fn.upper() for fn in _GRAMMAR["functions"]}

    # Build operator pattern from grammar (escape special chars, longest first)
    _ops_sorted = sorted(_GRAMMAR["operators"], key=len, reverse=True)
    _ops_pattern = "|".join(re.escape(op) for op in _ops_sorted)

    TOKEN_PATTERNS = [
        (_GRAMMAR["tokens"]["STRING"], "STRING"),
        (_ops_pattern, "OP"),
        (r",", "COMMA"),
        (r"\(", "LPAREN"),
        (r"\)", "RPAREN"),
        (_GRAMMAR["tokens"]["IDENT"], "IDENT"),
        (_GRAMMAR["tokens"]["NUMBER"], "NUMBER"),
        (r"\s+", "WHITESPACE"),
    ]

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def tokenize(self) -> Iterator[Token]:
        """Generate tokens from input text."""
        while self.pos < len(self.text):
            match = None
            for pattern, token_type in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    if token_type != "WHITESPACE":
                        # Classify identifiers as keywords or aggregate funcs
                        if token_type == "IDENT":
                            upper = value.upper()
                            if upper in self.KEYWORDS:
                                token_type = upper
                            elif upper in self.AGGREGATE_FUNCS:
                                token_type = "AGGFUNC"
                        yield Token(token_type, value, self.pos)
                    self.pos = match.end()
                    break
            if not match:
                raise ParseError(f"Unexpected character: {self.text[self.pos]!r}", self.pos)


class Parser:
    """
    Recursive descent parser for PlotQL.

    Designed to be composable - you can use individual parse methods
    or extend this class for custom syntax.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self) -> Optional[Token]:
        token = self.current
        self.pos += 1
        return token

    def expect(self, token_type: str) -> Token:
        token = self.current
        if token is None:
            raise ParseError(f"Expected {token_type}, got end of input")
        if token.type != token_type:
            raise ParseError(
                f"Expected {token_type}, got {token.type} ({token.value!r})",
                token.position
            )
        self.advance()
        return token

    def match(self, *token_types: str) -> Optional[Token]:
        if self.current and self.current.type in token_types:
            return self.advance()
        return None

    def parse(self) -> PlotQuery:
        """Parse a complete PlotQL query."""
        source = self.parse_with_clause()

        # Parse one or more series (PLOT clauses with optional FILTER/FORMAT)
        series_list: List[PlotSeries] = []
        while self.current and self.current.type == "PLOT":
            x_col, y_col, plot_type = self.parse_plot_clause()
            filter_clause = self.parse_filter_clause()
            format_opts = self.parse_format_clause()

            series_list.append(PlotSeries(
                x_column=x_col,
                y_column=y_col,
                plot_type=plot_type,
                filter=filter_clause,
                format=format_opts,
            ))

        if not series_list:
            raise ParseError("Expected at least one PLOT clause")

        if self.current is not None:
            raise ParseError(
                f"Unexpected token: {self.current.value!r}",
                self.current.position
            )

        return PlotQuery(
            source=source,
            series=series_list,
        )

    def parse_with_clause(self) -> str:
        """Parse: WITH 'filename'"""
        self.expect("WITH")
        token = self.expect("STRING")
        # Strip quotes
        return token.value[1:-1]

    def parse_column_ref(self) -> ColumnRef:
        """
        Parse a column reference, optionally with aggregation.

        Examples:
            price          -> ColumnRef(name="price")
            count(price)   -> ColumnRef(name="price", aggregate=AggregateFunc.COUNT)
        """
        # Check for aggregate function
        if self.current and self.current.type == "AGGFUNC":
            func_token = self.advance()
            func_name = func_token.value.lower()
            try:
                agg_func = AggregateFunc(func_name)
            except ValueError:
                raise ParseError(
                    f"Unknown aggregate function: {func_name}",
                    func_token.position
                )
            self.expect("LPAREN")
            col_name = self.expect("IDENT").value
            self.expect("RPAREN")
            return ColumnRef(name=col_name, aggregate=agg_func)
        else:
            col_name = self.expect("IDENT").value
            return ColumnRef(name=col_name)

    def parse_plot_clause(self) -> Tuple[ColumnRef, ColumnRef, PlotType]:
        """Parse: PLOT y_col AGAINST x_col [AS 'plot_type']"""
        self.expect("PLOT")
        y_col = self.parse_column_ref()
        self.expect("AGAINST")
        x_col = self.parse_column_ref()

        plot_type = PlotType.SCATTER
        if self.match("AS"):
            type_token = self.expect("STRING")
            type_value = type_token.value[1:-1].lower()  # Strip quotes
            try:
                plot_type = PlotType(type_value)
            except ValueError:
                valid = ", ".join(t.value for t in PlotType)
                raise ParseError(
                    f"Unknown plot type '{type_value}'. Valid: {valid}",
                    type_token.position
                )

        return x_col, y_col, plot_type

    def parse_filter_clause(self) -> Optional[WhereClause]:
        """Parse: FILTER condition ((AND|OR) condition)*"""
        if not self.match("FILTER"):
            return None

        conditions = [self.parse_condition()]
        operators: List[LogicalOp] = []

        while True:
            op_token = self.match("AND", "OR")
            if not op_token:
                break
            operators.append(LogicalOp(op_token.type))
            conditions.append(self.parse_condition())

        return WhereClause(conditions=conditions, operators=operators)

    def parse_condition(self) -> Condition:
        """Parse: column op value"""
        column = self.expect("IDENT").value
        op_token = self.expect("OP")
        op = ComparisonOp(op_token.value)

        # Parse value (string, number, or identifier)
        value_token = self.current
        if value_token is None:
            raise ParseError("Expected value after operator")

        if value_token.type == "STRING":
            self.advance()
            value = value_token.value[1:-1]
        elif value_token.type == "NUMBER":
            self.advance()
            value = float(value_token.value)
            if value.is_integer():
                value = int(value)
        elif value_token.type == "IDENT":
            self.advance()
            value = value_token.value
        else:
            raise ParseError(
                f"Expected value, got {value_token.type}",
                value_token.position
            )

        return Condition(column=column, op=op, value=value)

    def parse_format_clause(self) -> FormatOptions:
        """Parse: FORMAT key = value AND key = value ..."""
        options = FormatOptions()

        if not self.match("FORMAT"):
            return options

        while True:
            key = self.expect("IDENT").value
            self.expect("OP")  # = sign

            value_token = self.current
            if value_token is None:
                raise ParseError("Expected value after =")

            if value_token.type == "STRING":
                self.advance()
                value = value_token.value[1:-1]
            elif value_token.type == "NUMBER":
                self.advance()
                value = value_token.value
            elif value_token.type == "NULL":
                self.advance()
                value = None
            elif value_token.type == "IDENT":
                self.advance()
                value = value_token.value
            else:
                raise ParseError(f"Unexpected token: {value_token.value!r}")

            # Map to FormatOptions fields
            key_lower = key.lower()
            if key_lower in ("marker_size", "size"):
                options.marker_size = str(value) if value is not None else None
            elif key_lower in ("marker_color", "marker_colour"):
                options.marker_color = str(value) if value is not None else None
            elif key_lower == "marker":
                options.marker = str(value) if value is not None else None
            elif key_lower in ("line_color", "line_colour", "color", "colour"):
                options.line_color = str(value) if value is not None else None
            elif key_lower in ("line_style", "style"):
                options.line_style = str(value) if value is not None else None
            elif key_lower == "title":
                options.title = str(value) if value is not None else None
            elif key_lower == "xlabel":
                options.xlabel = str(value) if value is not None else None
            elif key_lower == "ylabel":
                options.ylabel = str(value) if value is not None else None

            # Use AND as separator instead of comma
            if not self.match("AND"):
                break

        return options


def parse(query: str) -> PlotQuery:
    """
    Parse a PlotQL query string into an AST.

    Example:
        >>> ast = parse("WITH 'data.csv' PLOT price AGAINST time AS line")
        >>> ast.source
        'data.csv'
        >>> ast.plot_type
        PlotType.LINE
    """
    lexer = Lexer(query)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    return parser.parse()
