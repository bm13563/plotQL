"""AST definitions for PlotQL queries."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, Union


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


# Data Source Types
# -----------------

@dataclass
class DataSource:
    """Base class for data sources."""
    pass


@dataclass
class LiteralSource(DataSource):
    """
    A literal file path data source.

    Used for: WITH 'path/to/file.csv'
    """
    path: str


@dataclass
class ConnectorSource(DataSource):
    """
    A connector function call data source.

    Used for: WITH file(alias) or WITH clickhouse(alias)
    """
    connector: str  # "file", "clickhouse"
    alias: str


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
class PlotSeries:
    """
    A single plot series definition.

    Each series has its own columns, plot type, filter, and format options.
    Multiple series can be layered on the same chart.
    """
    x_column: ColumnRef
    y_column: ColumnRef
    plot_type: PlotType = PlotType.SCATTER
    filter: Optional[WhereClause] = None
    format: FormatOptions = field(default_factory=FormatOptions)

    @property
    def is_aggregate(self) -> bool:
        """True if either axis uses an aggregation function."""
        return self.x_column.is_aggregate or self.y_column.is_aggregate


@dataclass
class PlotQuery:
    """
    Complete PlotQL query AST.

    Example query with single series:
        WITH 'trades.csv'
        PLOT price AGAINST time AS 'line'
        FILTER symbol = 'AAPL' AND volume > 1000
        FORMAT marker_color = 'red' AND line_color = 'blue'

    Example query with multiple series (later series plot on top):
        WITH 'trades.csv'
        PLOT price AGAINST time
        PLOT price AGAINST time
            FILTER user_id = 'foo'
            FORMAT marker_size = 5

    Example with connectors:
        WITH file(trades) PLOT price AGAINST time
        WITH clickhouse(production) PLOT price AGAINST time
    """
    source: DataSource  # Data source (LiteralSource or ConnectorSource)
    series: List[PlotSeries] = field(default_factory=list)

    @property
    def is_aggregate(self) -> bool:
        """True if any series uses an aggregation function."""
        return any(s.is_aggregate for s in self.series)

    def __repr__(self) -> str:
        if isinstance(self.source, LiteralSource):
            source_str = f"WITH '{self.source.path}'"
        elif isinstance(self.source, ConnectorSource):
            source_str = f"WITH {self.source.connector}({self.source.alias})"
        else:
            source_str = f"WITH {self.source}"

        parts = [source_str]
        for s in self.series:
            parts.append(f"PLOT {s.y_column} AGAINST {s.x_column} AS '{s.plot_type.value}'")
            if s.filter:
                conds = []
                for i, cond in enumerate(s.filter.conditions):
                    conds.append(f"{cond.column} {cond.op.value} {cond.value!r}")
                    if i < len(s.filter.operators):
                        conds.append(s.filter.operators[i].value)
                parts.append("    FILTER " + " ".join(conds))
        return "\n".join(parts)
