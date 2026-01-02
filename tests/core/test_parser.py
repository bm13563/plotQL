"""
Unit tests for plotql.core.parser module.

Tests lexer tokenization and parser functionality at token level.
"""
import pytest

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    ComparisonOp,
    LogicalOp,
    PlotType,
)
from plotql.core.parser import Lexer, ParseError, Parser, Token, parse


# =============================================================================
# Lexer Token Tests
# =============================================================================

class TestLexerBasics:
    """Basic lexer functionality tests."""

    def test_tokenize_empty_string(self):
        """Test tokenizing empty string produces no tokens."""
        lexer = Lexer("")
        tokens = list(lexer.tokenize())
        assert tokens == []

    def test_tokenize_whitespace_only(self):
        """Test tokenizing whitespace produces no tokens."""
        lexer = Lexer("   \t\n  ")
        tokens = list(lexer.tokenize())
        assert tokens == []

    def test_tokenize_single_keyword(self):
        """Test tokenizing a single keyword."""
        lexer = Lexer("WITH")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == "WITH"
        assert tokens[0].value == "WITH"
        assert tokens[0].position == 0

    def test_tokenize_keyword_case_insensitive(self):
        """Test keywords are recognized regardless of case."""
        for kw in ["with", "WITH", "With", "wItH"]:
            lexer = Lexer(kw)
            tokens = list(lexer.tokenize())
            assert tokens[0].type == "WITH"

    def test_token_position_tracking(self):
        """Test that token positions are correctly tracked."""
        lexer = Lexer("WITH  'file'")
        tokens = list(lexer.tokenize())
        assert tokens[0].position == 0  # WITH
        assert tokens[1].position == 6  # 'file' (after WITH and 2 spaces)


class TestLexerKeywords:
    """Test lexer keyword recognition."""

    @pytest.mark.parametrize("keyword", [
        "WITH", "PLOT", "AGAINST", "AS", "FILTER", "AND", "OR", "FORMAT", "NOT", "NULL"
    ])
    def test_all_keywords(self, keyword):
        """Test all keywords are recognized."""
        lexer = Lexer(keyword)
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == keyword

    def test_keyword_not_in_string(self):
        """Test keywords inside strings are not recognized as keywords."""
        lexer = Lexer("'WITH'")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "'WITH'"


class TestLexerAggregateFunctions:
    """Test lexer aggregate function recognition."""

    @pytest.mark.parametrize("func", ["count", "sum", "avg", "min", "max", "median"])
    def test_aggregate_functions_lowercase(self, func):
        """Test aggregate functions are recognized in lowercase."""
        lexer = Lexer(func)
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "AGGFUNC"

    @pytest.mark.parametrize("func", ["COUNT", "SUM", "AVG", "MIN", "MAX", "MEDIAN"])
    def test_aggregate_functions_uppercase(self, func):
        """Test aggregate functions are recognized in uppercase."""
        lexer = Lexer(func)
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "AGGFUNC"

    def test_aggregate_function_with_parens(self):
        """Test aggregate function followed by parentheses."""
        lexer = Lexer("count(x)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 4
        assert tokens[0].type == "AGGFUNC"
        assert tokens[1].type == "LPAREN"
        assert tokens[2].type == "IDENT"
        assert tokens[3].type == "RPAREN"


class TestLexerStrings:
    """Test lexer string tokenization."""

    def test_single_quoted_string(self):
        """Test single-quoted string."""
        lexer = Lexer("'hello world'")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "'hello world'"

    def test_double_quoted_string(self):
        """Test double-quoted string."""
        lexer = Lexer('"hello world"')
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == "STRING"
        assert tokens[0].value == '"hello world"'

    def test_empty_string(self):
        """Test empty string literal."""
        lexer = Lexer("''")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "''"

    def test_string_with_path(self):
        """Test string containing file path."""
        lexer = Lexer("'/path/to/file.csv'")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "'/path/to/file.csv'"

    def test_string_with_special_chars(self):
        """Test string with special characters."""
        lexer = Lexer("'hello-world_123'")
        tokens = list(lexer.tokenize())
        assert tokens[0].value == "'hello-world_123'"


class TestLexerNumbers:
    """Test lexer number tokenization."""

    def test_integer(self):
        """Test integer tokenization."""
        lexer = Lexer("42")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == "42"

    def test_negative_integer(self):
        """Test negative integer tokenization."""
        lexer = Lexer("-42")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == "-42"

    def test_float(self):
        """Test float tokenization."""
        lexer = Lexer("3.14")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == "3.14"

    def test_negative_float(self):
        """Test negative float tokenization."""
        lexer = Lexer("-3.14")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == "-3.14"

    def test_zero(self):
        """Test zero tokenization."""
        lexer = Lexer("0")
        tokens = list(lexer.tokenize())
        assert tokens[0].value == "0"


class TestLexerOperators:
    """Test lexer operator tokenization."""

    @pytest.mark.parametrize("op", ["=", "!=", "<", "<=", ">", ">="])
    def test_comparison_operators(self, op):
        """Test all comparison operators are recognized."""
        lexer = Lexer(op)
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "OP"
        assert tokens[0].value == op

    def test_operator_order_longest_first(self):
        """Test that longer operators match before shorter ones."""
        # <= should match as one token, not < and =
        lexer = Lexer("<=")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].value == "<="

    def test_operators_without_spaces(self):
        """Test operators work without surrounding spaces."""
        lexer = Lexer("x>=10")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 3
        assert tokens[0].value == "x"
        assert tokens[1].value == ">="
        assert tokens[2].value == "10"


class TestLexerIdentifiers:
    """Test lexer identifier tokenization."""

    def test_simple_identifier(self):
        """Test simple identifier."""
        lexer = Lexer("column_name")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "IDENT"
        assert tokens[0].value == "column_name"

    def test_identifier_with_numbers(self):
        """Test identifier with numbers."""
        lexer = Lexer("col123")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "IDENT"
        assert tokens[0].value == "col123"

    def test_identifier_starting_with_underscore(self):
        """Test identifier starting with underscore."""
        lexer = Lexer("_private")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "IDENT"
        assert tokens[0].value == "_private"

    def test_identifier_not_keyword(self):
        """Test identifier that looks like keyword prefix."""
        lexer = Lexer("WITHDRAW")  # Contains WITH but is not WITH
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "IDENT"
        assert tokens[0].value == "WITHDRAW"


class TestLexerParentheses:
    """Test lexer parenthesis tokenization."""

    def test_left_paren(self):
        """Test left parenthesis."""
        lexer = Lexer("(")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "LPAREN"

    def test_right_paren(self):
        """Test right parenthesis."""
        lexer = Lexer(")")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "RPAREN"

    def test_matched_parens(self):
        """Test matched parentheses."""
        lexer = Lexer("(x)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 3
        assert tokens[0].type == "LPAREN"
        assert tokens[2].type == "RPAREN"


class TestLexerComma:
    """Test lexer comma tokenization."""

    def test_comma(self):
        """Test comma token."""
        lexer = Lexer(",")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == "COMMA"


class TestLexerErrors:
    """Test lexer error handling."""

    def test_unexpected_character(self):
        """Test error on unexpected character."""
        lexer = Lexer("@")
        with pytest.raises(ParseError) as exc_info:
            list(lexer.tokenize())
        assert "Unexpected character" in str(exc_info.value)
        assert "@" in str(exc_info.value)

    def test_error_position(self):
        """Test that error position is correct."""
        lexer = Lexer("WITH @")
        with pytest.raises(ParseError) as exc_info:
            list(lexer.tokenize())
        assert exc_info.value.position == 5


class TestLexerCompleteQueries:
    """Test lexer on complete query strings."""

    def test_simple_query(self):
        """Test tokenizing a simple query."""
        query = "WITH 'data.csv' PLOT y AGAINST x"
        lexer = Lexer(query)
        tokens = list(lexer.tokenize())

        assert tokens[0].type == "WITH"
        assert tokens[1].type == "STRING"
        assert tokens[2].type == "PLOT"
        assert tokens[3].type == "IDENT"
        assert tokens[4].type == "AGAINST"
        assert tokens[5].type == "IDENT"

    def test_query_with_filter(self):
        """Test tokenizing query with FILTER clause."""
        query = "WITH 'data.csv' PLOT y AGAINST x FILTER value > 10"
        lexer = Lexer(query)
        tokens = list(lexer.tokenize())

        types = [t.type for t in tokens]
        assert "FILTER" in types
        assert "OP" in types
        assert "NUMBER" in types

    def test_query_with_aggregation(self):
        """Test tokenizing query with aggregation."""
        query = "WITH 'data.csv' PLOT count(x) AGAINST category"
        lexer = Lexer(query)
        tokens = list(lexer.tokenize())

        types = [t.type for t in tokens]
        assert "AGGFUNC" in types
        assert "LPAREN" in types
        assert "RPAREN" in types

    def test_query_with_format(self):
        """Test tokenizing query with FORMAT clause."""
        query = "WITH 'data.csv' PLOT y AGAINST x FORMAT title = 'Test'"
        lexer = Lexer(query)
        tokens = list(lexer.tokenize())

        types = [t.type for t in tokens]
        assert "FORMAT" in types


# =============================================================================
# Parser Tests
# =============================================================================

class TestParserBasics:
    """Basic parser functionality tests."""

    def test_parse_minimal_query(self):
        """Test parsing minimal valid query."""
        query = "WITH 'data.csv' PLOT y AGAINST x"
        result = parse(query)

        assert result.source.path == "data.csv"
        assert result.series[0].x_column.name == "x"
        assert result.series[0].y_column.name == "y"
        assert result.series[0].plot_type == PlotType.SCATTER

    def test_parse_returns_plot_query(self):
        """Test that parse returns a PlotQuery."""
        from plotql.core.ast import PlotQuery
        result = parse("WITH 'data.csv' PLOT y AGAINST x")
        assert isinstance(result, PlotQuery)


class TestParserWithClause:
    """Test parsing WITH clause."""

    def test_with_single_quotes(self):
        """Test WITH clause with single quotes."""
        result = parse("WITH 'file.csv' PLOT y AGAINST x")
        assert result.source.path == "file.csv"

    def test_with_double_quotes(self):
        """Test WITH clause with double quotes."""
        result = parse('WITH "file.csv" PLOT y AGAINST x')
        assert result.source.path == "file.csv"

    def test_with_path(self):
        """Test WITH clause with full path."""
        result = parse("WITH '/path/to/data.csv' PLOT y AGAINST x")
        assert result.source.path == "/path/to/data.csv"

    def test_with_relative_path(self):
        """Test WITH clause with relative path."""
        result = parse("WITH './data/file.csv' PLOT y AGAINST x")
        assert result.source.path == "./data/file.csv"


class TestParserPlotClause:
    """Test parsing PLOT clause."""

    def test_simple_columns(self):
        """Test PLOT with simple column names."""
        result = parse("WITH 'data.csv' PLOT price AGAINST time")
        assert result.series[0].y_column.name == "price"
        assert result.series[0].x_column.name == "time"

    def test_columns_with_underscores(self):
        """Test PLOT with underscored column names."""
        result = parse("WITH 'data.csv' PLOT my_column AGAINST other_col")
        assert result.series[0].y_column.name == "my_column"
        assert result.series[0].x_column.name == "other_col"

    def test_default_plot_type_is_scatter(self):
        """Test default plot type is scatter."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x")
        assert result.series[0].plot_type == PlotType.SCATTER

    @pytest.mark.parametrize("plot_type,expected", [
        ("scatter", PlotType.SCATTER),
        ("line", PlotType.LINE),
        ("bar", PlotType.BAR),
        ("hist", PlotType.HIST),
    ])
    def test_as_plot_types(self, plot_type, expected):
        """Test AS clause with all plot types."""
        result = parse(f"WITH 'data.csv' PLOT y AGAINST x AS '{plot_type}'")
        assert result.series[0].plot_type == expected

    def test_plot_type_case_insensitive(self):
        """Test plot type is case insensitive."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x AS 'LINE'")
        assert result.series[0].plot_type == PlotType.LINE


class TestParserAggregation:
    """Test parsing aggregation functions."""

    @pytest.mark.parametrize("func,expected", [
        ("count", AggregateFunc.COUNT),
        ("sum", AggregateFunc.SUM),
        ("avg", AggregateFunc.AVG),
        ("min", AggregateFunc.MIN),
        ("max", AggregateFunc.MAX),
        ("median", AggregateFunc.MEDIAN),
    ])
    def test_aggregate_functions(self, func, expected):
        """Test all aggregate functions parse correctly."""
        result = parse(f"WITH 'data.csv' PLOT {func}(value) AGAINST category")
        assert result.series[0].y_column.aggregate == expected
        assert result.series[0].y_column.name == "value"

    def test_aggregate_in_y_column(self):
        """Test aggregation in y column."""
        result = parse("WITH 'data.csv' PLOT count(id) AGAINST category")
        assert result.series[0].y_column.is_aggregate
        assert not result.series[0].x_column.is_aggregate

    def test_aggregate_in_x_column(self):
        """Test aggregation in x column."""
        result = parse("WITH 'data.csv' PLOT value AGAINST avg(score)")
        assert result.series[0].x_column.is_aggregate
        assert not result.series[0].y_column.is_aggregate

    def test_query_is_aggregate_property(self):
        """Test PlotQuery.is_aggregate property."""
        result = parse("WITH 'data.csv' PLOT sum(amount) AGAINST category")
        assert result.is_aggregate is True


class TestParserFilterClause:
    """Test parsing FILTER clause."""

    def test_single_condition_equals_number(self):
        """Test FILTER with equals and number."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER value = 10")
        assert result.series[0].filter is not None
        assert len(result.series[0].filter.conditions) == 1
        assert result.series[0].filter.conditions[0].column == "value"
        assert result.series[0].filter.conditions[0].op == ComparisonOp.EQ
        assert result.series[0].filter.conditions[0].value == 10

    def test_single_condition_equals_string(self):
        """Test FILTER with equals and string."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER status = 'active'")
        assert result.series[0].filter.conditions[0].value == "active"

    def test_single_condition_greater_than(self):
        """Test FILTER with greater than."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER price > 100")
        assert result.series[0].filter.conditions[0].op == ComparisonOp.GT

    def test_single_condition_less_than(self):
        """Test FILTER with less than."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER quantity < 5")
        assert result.series[0].filter.conditions[0].op == ComparisonOp.LT

    def test_single_condition_greater_equals(self):
        """Test FILTER with greater than or equals."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER age >= 18")
        assert result.series[0].filter.conditions[0].op == ComparisonOp.GE

    def test_single_condition_less_equals(self):
        """Test FILTER with less than or equals."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER score <= 100")
        assert result.series[0].filter.conditions[0].op == ComparisonOp.LE

    def test_single_condition_not_equals(self):
        """Test FILTER with not equals."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER type != 'hidden'")
        assert result.series[0].filter.conditions[0].op == ComparisonOp.NE

    def test_two_conditions_and(self):
        """Test FILTER with two conditions and AND."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER a = 1 AND b = 2")
        assert len(result.series[0].filter.conditions) == 2
        assert len(result.series[0].filter.operators) == 1
        assert result.series[0].filter.operators[0] == LogicalOp.AND

    def test_two_conditions_or(self):
        """Test FILTER with two conditions and OR."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER a = 1 OR b = 2")
        assert result.series[0].filter.operators[0] == LogicalOp.OR

    def test_three_conditions_mixed(self):
        """Test FILTER with three conditions and mixed operators."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER a = 1 AND b = 2 OR c = 3")
        assert len(result.series[0].filter.conditions) == 3
        assert len(result.series[0].filter.operators) == 2
        assert result.series[0].filter.operators[0] == LogicalOp.AND
        assert result.series[0].filter.operators[1] == LogicalOp.OR

    def test_filter_with_float(self):
        """Test FILTER with float value."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER price > 99.99")
        assert result.series[0].filter.conditions[0].value == 99.99

    def test_filter_with_negative_number(self):
        """Test FILTER with negative number."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER delta < -10")
        assert result.series[0].filter.conditions[0].value == -10

    def test_filter_with_identifier_value(self):
        """Test FILTER with identifier as value."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER type = active")
        assert result.series[0].filter.conditions[0].value == "active"


class TestParserFormatClause:
    """Test parsing FORMAT clause."""

    def test_format_title(self):
        """Test FORMAT with title."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT title = 'My Plot'")
        assert result.series[0].format.title == "My Plot"

    def test_format_xlabel(self):
        """Test FORMAT with xlabel."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT xlabel = 'X Axis'")
        assert result.series[0].format.xlabel == "X Axis"

    def test_format_ylabel(self):
        """Test FORMAT with ylabel."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT ylabel = 'Y Axis'")
        assert result.series[0].format.ylabel == "Y Axis"

    def test_format_marker_size(self):
        """Test FORMAT with marker_size."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT marker_size = 3")
        assert result.series[0].format.marker_size == "3"

    def test_format_marker_size_alias(self):
        """Test FORMAT with size alias."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT size = 2")
        assert result.series[0].format.marker_size == "2"

    def test_format_marker_color(self):
        """Test FORMAT with marker_color."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT marker_color = blue")
        assert result.series[0].format.marker_color == "blue"

    def test_format_marker_colour_alias(self):
        """Test FORMAT with British spelling."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT marker_colour = red")
        assert result.series[0].format.marker_color == "red"

    def test_format_line_color(self):
        """Test FORMAT with line_color."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT line_color = green")
        assert result.series[0].format.line_color == "green"

    def test_format_color_alias(self):
        """Test FORMAT with color alias."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT color = yellow")
        assert result.series[0].format.line_color == "yellow"

    def test_format_line_style(self):
        """Test FORMAT with line_style."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT line_style = dashed")
        assert result.series[0].format.line_style == "dashed"

    def test_format_style_alias(self):
        """Test FORMAT with style alias."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT style = dotted")
        assert result.series[0].format.line_style == "dotted"

    def test_format_marker_null(self):
        """Test FORMAT with marker = NULL."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT marker = NULL")
        assert result.series[0].format.marker is None

    def test_format_multiple_options(self):
        """Test FORMAT with multiple options."""
        result = parse(
            "WITH 'data.csv' PLOT y AGAINST x "
            "FORMAT title = 'Plot' AND xlabel = 'X' AND ylabel = 'Y'"
        )
        assert result.series[0].format.title == "Plot"
        assert result.series[0].format.xlabel == "X"
        assert result.series[0].format.ylabel == "Y"

    def test_format_column_reference(self):
        """Test FORMAT with column reference as value."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FORMAT marker_color = category")
        assert result.series[0].format.marker_color == "category"


class TestParserCompleteQueries:
    """Test parsing complete queries with all clauses."""

    def test_full_query(self):
        """Test parsing a full query with all clauses."""
        query = (
            "WITH 'trades.csv' "
            "PLOT sum(amount) AGAINST category AS 'bar' "
            "FILTER status = 'active' AND value > 100 "
            "FORMAT title = 'Sales' AND ylabel = 'Amount'"
        )
        result = parse(query)

        assert result.source.path == "trades.csv"
        assert result.series[0].y_column.aggregate == AggregateFunc.SUM
        assert result.series[0].x_column.name == "category"
        assert result.series[0].plot_type == PlotType.BAR
        assert len(result.series[0].filter.conditions) == 2
        assert result.series[0].format.title == "Sales"

    def test_multiline_query(self):
        """Test parsing a multiline query."""
        query = """
        WITH 'data.csv'
        PLOT y AGAINST x AS 'line'
        FILTER value > 0
        FORMAT title = 'Chart'
        """
        result = parse(query)

        assert result.source.path == "data.csv"
        assert result.series[0].plot_type == PlotType.LINE
        assert result.series[0].filter is not None
        assert result.series[0].format.title == "Chart"


class TestParserErrors:
    """Test parser error handling."""

    def test_missing_with(self):
        """Test error when WITH is missing."""
        with pytest.raises(ParseError) as exc_info:
            parse("PLOT y AGAINST x")
        assert "Expected WITH" in str(exc_info.value)

    def test_missing_file_after_with(self):
        """Test error when file path is missing after WITH."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH PLOT y AGAINST x")
        # Error can be about STRING or connector function
        assert "file path" in str(exc_info.value).lower() or "connector" in str(exc_info.value).lower()

    def test_missing_plot(self):
        """Test error when PLOT is missing."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv'")
        assert "PLOT" in str(exc_info.value)

    def test_missing_against(self):
        """Test error when AGAINST is missing."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT y x")
        assert "Expected AGAINST" in str(exc_info.value)

    def test_invalid_plot_type(self):
        """Test error for invalid plot type."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT y AGAINST x AS 'invalid'")
        assert "Unknown plot type" in str(exc_info.value)

    def test_unexpected_token_at_end(self):
        """Test error for unexpected token at end."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT y AGAINST x EXTRA")
        assert "Unexpected token" in str(exc_info.value)

    def test_missing_closing_paren_in_aggregate(self):
        """Test error for missing closing paren in aggregate."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT count(x AGAINST y")
        assert "Expected RPAREN" in str(exc_info.value)

    def test_missing_value_after_filter_operator(self):
        """Test error when value is missing after filter operator."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT y AGAINST x FILTER value >")
        assert "Expected value" in str(exc_info.value)

    def test_missing_value_after_format_equals(self):
        """Test error when value is missing after FORMAT =."""
        with pytest.raises(ParseError) as exc_info:
            parse("WITH 'data.csv' PLOT y AGAINST x FORMAT title =")
        assert "Expected value" in str(exc_info.value)


class TestParserEdgeCases:
    """Test parser edge cases."""

    def test_extra_whitespace(self):
        """Test query with extra whitespace."""
        query = "WITH   'data.csv'   PLOT   y   AGAINST   x"
        result = parse(query)
        assert result.source.path == "data.csv"

    def test_tabs_in_query(self):
        """Test query with tabs."""
        query = "WITH\t'data.csv'\tPLOT\ty\tAGAINST\tx"
        result = parse(query)
        assert result.source.path == "data.csv"

    def test_newlines_in_query(self):
        """Test query with newlines."""
        query = "WITH\n'data.csv'\nPLOT\ny\nAGAINST\nx"
        result = parse(query)
        assert result.source.path == "data.csv"

    def test_integer_converted_properly(self):
        """Test integer values are converted to int."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER value = 10")
        assert result.series[0].filter.conditions[0].value == 10
        assert isinstance(result.series[0].filter.conditions[0].value, int)

    def test_float_kept_as_float(self):
        """Test float values are kept as float."""
        result = parse("WITH 'data.csv' PLOT y AGAINST x FILTER value = 10.5")
        assert result.series[0].filter.conditions[0].value == 10.5
        assert isinstance(result.series[0].filter.conditions[0].value, float)


# =============================================================================
# Parser Class Direct Tests
# =============================================================================

class TestParserClass:
    """Test Parser class methods directly."""

    def test_parser_current_property(self):
        """Test Parser.current property."""
        tokens = [Token("WITH", "WITH", 0)]
        parser = Parser(tokens)
        assert parser.current is not None
        assert parser.current.type == "WITH"

    def test_parser_current_returns_none_at_end(self):
        """Test Parser.current returns None at end."""
        parser = Parser([])
        assert parser.current is None

    def test_parser_advance(self):
        """Test Parser.advance method."""
        tokens = [
            Token("WITH", "WITH", 0),
            Token("STRING", "'file'", 5),
        ]
        parser = Parser(tokens)
        token = parser.advance()
        assert token.type == "WITH"
        assert parser.current.type == "STRING"

    def test_parser_expect_success(self):
        """Test Parser.expect with matching token."""
        tokens = [Token("WITH", "WITH", 0)]
        parser = Parser(tokens)
        token = parser.expect("WITH")
        assert token.type == "WITH"

    def test_parser_expect_failure(self):
        """Test Parser.expect with non-matching token."""
        tokens = [Token("PLOT", "PLOT", 0)]
        parser = Parser(tokens)
        with pytest.raises(ParseError) as exc_info:
            parser.expect("WITH")
        assert "Expected WITH" in str(exc_info.value)

    def test_parser_match_success(self):
        """Test Parser.match with matching token."""
        tokens = [Token("WITH", "WITH", 0)]
        parser = Parser(tokens)
        token = parser.match("WITH")
        assert token is not None
        assert token.type == "WITH"

    def test_parser_match_failure(self):
        """Test Parser.match with non-matching token."""
        tokens = [Token("PLOT", "PLOT", 0)]
        parser = Parser(tokens)
        token = parser.match("WITH")
        assert token is None
        # Position should not advance
        assert parser.current.type == "PLOT"

    def test_parser_match_multiple_types(self):
        """Test Parser.match with multiple possible types."""
        tokens = [Token("AND", "AND", 0)]
        parser = Parser(tokens)
        token = parser.match("AND", "OR")
        assert token is not None
        assert token.type == "AND"


# =============================================================================
# Multiple Series Tests
# =============================================================================

class TestParserMultipleSeries:
    """Test parsing queries with multiple PLOT clauses (series)."""

    def test_two_plot_clauses_basic(self):
        """Test parsing query with two PLOT clauses."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time
        PLOT volume AGAINST time
        """
        result = parse(query)

        assert result.source.path == "data.csv"
        assert len(result.series) == 2
        assert result.series[0].y_column.name == "price"
        assert result.series[0].x_column.name == "time"
        assert result.series[1].y_column.name == "volume"
        assert result.series[1].x_column.name == "time"

    def test_second_plot_with_filter(self):
        """Test that FILTER applies to the preceding PLOT clause."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time
        PLOT price AGAINST time
            FILTER user_id = 'foo'
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[0].filter is None
        assert result.series[1].filter is not None
        assert result.series[1].filter.conditions[0].column == "user_id"
        assert result.series[1].filter.conditions[0].value == "foo"

    def test_second_plot_with_format(self):
        """Test that FORMAT applies to the preceding PLOT clause."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time
        PLOT price AGAINST time
            FORMAT marker_size = 5
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[0].format.marker_size is None
        assert result.series[1].format.marker_size == "5"

    def test_second_plot_with_filter_and_format(self):
        """Test PLOT with both FILTER and FORMAT."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time
        PLOT price AGAINST time
            FILTER user_id = 'foo'
            FORMAT marker_size = 5
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[1].filter is not None
        assert result.series[1].format.marker_size == "5"

    def test_multiple_series_with_plot_types(self):
        """Test multiple PLOT clauses with AS type declarations."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time AS 'line'
        PLOT volume AGAINST time AS 'scatter'
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[0].plot_type == PlotType.LINE
        assert result.series[1].plot_type == PlotType.SCATTER

    def test_three_plot_clauses(self):
        """Test parsing query with three PLOT clauses."""
        query = """
        WITH 'data.csv'
        PLOT a AGAINST x
        PLOT b AGAINST x
        PLOT c AGAINST x
        """
        result = parse(query)

        assert len(result.series) == 3
        assert result.series[0].y_column.name == "a"
        assert result.series[1].y_column.name == "b"
        assert result.series[2].y_column.name == "c"

    def test_first_series_with_filter_format(self):
        """Test first PLOT clause can have FILTER and FORMAT too."""
        query = """
        WITH 'data.csv'
        PLOT price AGAINST time
            FILTER category = 'A'
            FORMAT marker_color = 'blue'
        PLOT price AGAINST time
            FILTER category = 'B'
            FORMAT marker_color = 'red'
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[0].filter.conditions[0].value == "A"
        assert result.series[0].format.marker_color == "blue"
        assert result.series[1].filter.conditions[0].value == "B"
        assert result.series[1].format.marker_color == "red"

    def test_mixed_aggregated_and_raw(self):
        """Test mixing aggregated and non-aggregated series."""
        query = """
        WITH 'data.csv'
        PLOT count(id) AGAINST category AS 'bar'
        PLOT avg(value) AGAINST category AS 'line'
        """
        result = parse(query)

        assert len(result.series) == 2
        assert result.series[0].y_column.is_aggregate
        assert result.series[0].y_column.aggregate == AggregateFunc.COUNT
        assert result.series[1].y_column.is_aggregate
        assert result.series[1].y_column.aggregate == AggregateFunc.AVG

    def test_backward_compatible_single_plot(self):
        """Test that single PLOT queries still work (backward compatibility)."""
        query = "WITH 'data.csv' PLOT y AGAINST x"
        result = parse(query)

        # Should have exactly one series
        assert len(result.series) == 1
        assert result.series[0].y_column.name == "y"
        assert result.series[0].x_column.name == "x"

    def test_backward_compatible_with_filter_format(self):
        """Test backward compatibility with FILTER and FORMAT."""
        query = "WITH 'data.csv' PLOT y AGAINST x FILTER a = 1 FORMAT title = 'Test'"
        result = parse(query)

        assert len(result.series) == 1
        assert result.series[0].filter is not None
        assert result.series[0].format.title == "Test"

    def test_example_from_todo(self):
        """Test the exact example from the todo.md."""
        query = """
        WITH 'example/trades.csv'
        PLOT
            price AGAINST received_at
        PLOT
            price AGAINST received_at
            FILTER user_id = 'foo'
            FORMAT marker_size = 5
        """
        result = parse(query)

        assert result.source.path == "example/trades.csv"
        assert len(result.series) == 2

        # First series: all data, no filter/format
        assert result.series[0].y_column.name == "price"
        assert result.series[0].x_column.name == "received_at"
        assert result.series[0].filter is None

        # Second series: filtered with custom marker size
        assert result.series[1].y_column.name == "price"
        assert result.series[1].x_column.name == "received_at"
        assert result.series[1].filter is not None
        assert result.series[1].filter.conditions[0].column == "user_id"
        assert result.series[1].format.marker_size == "5"
