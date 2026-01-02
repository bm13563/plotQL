"""AST definitions for PlotQL queries."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional


class PlotType(Enum):
    """Supported plot types."""
    SCATTER = "scatter"
    LINE = "line"
    BAR = "bar"
    HIST = "hist"


class AggregateFunc(Enum):
    """Supported aggregation functions."""
    COUNT = "count"
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"


@dataclass
class ColumnRef:
    """
    A column reference, optionally with an aggregation function.

    Examples:
        price          -> ColumnRef(name="price", aggregate=None)
        count(price)   -> ColumnRef(name="price", aggregate=AggregateFunc.COUNT)
        avg(volume)    -> ColumnRef(name="volume", aggregate=AggregateFunc.AVG)
    """
    name: str
    aggregate: Optional[AggregateFunc] = None

    @property
    def is_aggregate(self) -> bool:
        return self.aggregate is not None

    def __str__(self) -> str:
        if self.aggregate:
            return f"{self.aggregate.value}({self.name})"
        return self.name


class ComparisonOp(Enum):
    """Comparison operators for WHERE clauses."""
    EQ = "="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="


class LogicalOp(Enum):
    """Logical operators for combining conditions."""
    AND = "AND"
    OR = "OR"


@dataclass
class Condition:
    """A single WHERE condition."""
    column: str
    op: ComparisonOp
    value: Any


@dataclass
class WhereClause:
    """WHERE clause with one or more conditions."""
    conditions: List[Condition]
    operators: List[LogicalOp] = field(default_factory=list)


@dataclass
class FormatOptions:
    """Visual formatting options for the plot."""
    marker_size: Optional[str] = None  # Can be a column name or literal
    marker_color: Optional[str] = None
    marker: Optional[str] = "default"  # Marker type for line plots, "default" enables, None/NULL disables
    line_color: Optional[str] = None
    line_style: Optional[str] = None  # solid, dashed, dotted
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None


@dataclass
class PlotQuery:
    """
    Complete PlotQL query AST.

    Example query:
        WITH 'trades.csv'
        PLOT price AGAINST time AS 'line'
        FILTER symbol = 'AAPL' AND volume > 1000
        FORMAT marker_color = 'red' AND line_color = 'blue'

    With aggregation:
        WITH 'trades.csv'
        PLOT count(price) AGAINST symbol AS 'bar'
    """
    source: str  # File path
    x_column: ColumnRef
    y_column: ColumnRef
    plot_type: PlotType = PlotType.SCATTER
    filter: Optional[WhereClause] = None
    format: FormatOptions = field(default_factory=FormatOptions)

    @property
    def is_aggregate(self) -> bool:
        """True if either axis uses an aggregation function."""
        return self.x_column.is_aggregate or self.y_column.is_aggregate

    def __repr__(self) -> str:
        parts = [
            f"WITH '{self.source}'",
            f"PLOT {self.y_column} AGAINST {self.x_column} AS '{self.plot_type.value}'",
        ]
        if self.filter:
            conds = []
            for i, cond in enumerate(self.filter.conditions):
                conds.append(f"{cond.column} {cond.op.value} {cond.value!r}")
                if i < len(self.filter.operators):
                    conds.append(self.filter.operators[i].value)
            parts.append("FILTER " + " ".join(conds))
        return "\n".join(parts)
