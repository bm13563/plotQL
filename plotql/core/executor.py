"""
Query executor - loads data with Polars and prepares it for plotting.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, Union

import polars as pl

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    ComparisonOp,
    ConnectorSource,
    DataSource,
    LiteralSource,
    LogicalOp,
    PlotQuery,
    PlotSeries,
    PlotType,
    SourceRef,
    WhereClause,
)
from plotql.core.config import get_source_config
from plotql.core.connectors import get_connector, LiteralConnector, ConnectorError
from plotql.core.utils import map_to_sizes, map_to_colors, TimestampInfo, detect_timestamp_columns


# Valid color names that can be used as literal marker_color values
VALID_COLORS = {
    "blue", "red", "green", "yellow", "orange", "pink",
    "purple", "cyan", "teal", "magenta", "white", "gray", "grey"
}


class ExecutionError(Exception):
    """Raised when query execution fails."""
    pass


@dataclass
class SizeInfo:
    """Information about marker sizes for legend display."""
    is_continuous: bool
    column_name: str
    # For continuous: (min_value, max_value)
    # For categorical: dict of {value: size}
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    category_sizes: Optional[dict] = None


@dataclass
class ColorInfo:
    """Information about marker colors for legend display."""
    is_continuous: bool
    column_name: str
    # For continuous: (min_value, max_value)
    # For categorical: dict of {value: color_name}
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    category_colors: Optional[dict] = None


@dataclass
class PlotData:
    """Result of executing a single series - ready for plotting."""
    x: List[Any]  # Can be float, datetime, or string depending on data
    y: List[Any]
    series: PlotSeries  # The series this data came from
    row_count: int
    filtered_count: int
    # Optional columns for dynamic formatting
    marker_sizes: Optional[List[float]] = None
    marker_colors: Optional[List[str]] = None
    size_info: Optional[SizeInfo] = None
    color_info: Optional[ColorInfo] = None
    # Timestamp info for datetime axes
    x_timestamp: Optional[TimestampInfo] = None
    y_timestamp: Optional[TimestampInfo] = None


def load_data(
    source: Union[SourceRef, DataSource],
    filters: Optional[List[WhereClause]] = None,
) -> tuple[pl.DataFrame, bool]:
    """
    Load data from any data source type.

    Args:
        source: A SourceRef or legacy DataSource
        filters: Optional list of WhereClause filters to push down.
                 Only used if the connector supports filter pushdown.
                 The connector is responsible for combining them appropriately.

    Returns:
        Tuple of (DataFrame, filter_applied) where filter_applied is True
        if filters were pushed down to the connector.

    Raises:
        ExecutionError: If data loading fails.
    """
    try:
        if isinstance(source, SourceRef):
            return _load_from_source_ref(source, filters)
        elif isinstance(source, LiteralSource):
            # Legacy: Literal file path - use LiteralConnector (no pushdown)
            connector = LiteralConnector()
            return connector.load({"path": source.path}), False
        elif isinstance(source, ConnectorSource):
            # Legacy: Connector function call - look up config and dispatch
            source_config = get_source_config(source.alias)
            connector = get_connector(source_config.type)
            # Pass filters if connector supports pushdown
            if connector.supports_filter_pushdown and filters:
                return connector.load(source_config.config, filters=filters), True
            else:
                return connector.load(source_config.config), False
        else:
            raise ExecutionError(f"Unknown data source type: {type(source)}")
    except ConnectorError as e:
        raise ExecutionError(str(e))


def _load_from_source_ref(
    source: SourceRef,
    filters: Optional[List[WhereClause]] = None,
) -> tuple[pl.DataFrame, bool]:
    """
    Load data from a SourceRef.

    Handles:
    - source('path.csv') -> literal file path (single arg, looks like file path)
    - source('trades') -> config alias lookup (single arg, no file extension)
    - source('pump_fun', 'trades') -> database alias + table
    - source('local_data', 'subdir', 'file.csv') -> folder alias + path segments

    For single-arg sources, we try config alias lookup first, falling back to
    literal file path if not found.
    """
    from plotql.core.config import ConfigError

    if len(source.args) == 1:
        # Single arg: try config alias first, fall back to file path
        arg = source.args[0]
        try:
            source_config = get_source_config(arg)
            connector = get_connector(source_config.type)
            config = dict(source_config.config)
            if connector.supports_filter_pushdown and filters:
                return connector.load(config, filters=filters), True
            else:
                return connector.load(config), False
        except ConfigError:
            # Not a config alias, treat as literal file path
            connector = LiteralConnector()
            return connector.load({"path": arg}), False

    # Multi-arg: always a config alias with additional args
    alias = source.args[0]
    source_config = get_source_config(alias)
    connector = get_connector(source_config.type)

    # Build config dict, adding extra args based on connector type
    config = dict(source_config.config)
    extra_args = source.args[1:]

    if source_config.type == "folder":
        # Folder connector: all extra args are path segments
        config["segments"] = extra_args
    elif extra_args:
        # Other connectors (clickhouse): first extra arg is table
        config["table"] = extra_args[0]

    # Pass filters if connector supports pushdown
    if connector.supports_filter_pushdown and filters:
        return connector.load(config, filters=filters), True
    else:
        return connector.load(config), False


def apply_where(df: pl.DataFrame, where: WhereClause) -> pl.DataFrame:
    """Apply WHERE clause filters to DataFrame."""
    if not where.conditions:
        return df

    def condition_to_expr(cond) -> pl.Expr:
        col = pl.col(cond.column)
        value = cond.value

        if cond.op == ComparisonOp.EQ:
            return col == value
        elif cond.op == ComparisonOp.NE:
            return col != value
        elif cond.op == ComparisonOp.LT:
            return col < value
        elif cond.op == ComparisonOp.LE:
            return col <= value
        elif cond.op == ComparisonOp.GT:
            return col > value
        elif cond.op == ComparisonOp.GE:
            return col >= value
        else:
            raise ExecutionError(f"Unknown operator: {cond.op}")

    # Build compound expression
    expr = condition_to_expr(where.conditions[0])

    for i, op in enumerate(where.operators):
        next_cond = condition_to_expr(where.conditions[i + 1])
        if op == LogicalOp.AND:
            expr = expr & next_cond
        else:  # OR
            expr = expr | next_cond

    return df.filter(expr)


def apply_aggregation(
    df: pl.DataFrame,
    x_col: ColumnRef,
    y_col: ColumnRef
) -> pl.DataFrame:
    """
    Apply aggregation to the dataframe based on column references.

    Groups by the non-aggregated column and applies the aggregate function.
    """
    # Determine group-by column (the one without aggregation)
    if y_col.is_aggregate and not x_col.is_aggregate:
        group_col = x_col.name
        agg_col = y_col
    elif x_col.is_aggregate and not y_col.is_aggregate:
        group_col = y_col.name
        agg_col = x_col
    elif y_col.is_aggregate and x_col.is_aggregate:
        raise ExecutionError("Cannot aggregate both x and y columns")
    else:
        # No aggregation needed
        return df

    # Build aggregation expression
    col_expr = pl.col(agg_col.name)

    if agg_col.aggregate == AggregateFunc.COUNT:
        agg_expr = col_expr.count()
    elif agg_col.aggregate == AggregateFunc.SUM:
        agg_expr = col_expr.sum()
    elif agg_col.aggregate == AggregateFunc.AVG:
        agg_expr = col_expr.mean()
    elif agg_col.aggregate == AggregateFunc.MIN:
        agg_expr = col_expr.min()
    elif agg_col.aggregate == AggregateFunc.MAX:
        agg_expr = col_expr.max()
    elif agg_col.aggregate == AggregateFunc.MEDIAN:
        agg_expr = col_expr.median()
    else:
        raise ExecutionError(f"Unknown aggregate function: {agg_col.aggregate}")

    # Perform groupby aggregation
    result = df.group_by(group_col).agg(agg_expr.alias(agg_col.name))

    return result


def validate_series_format_options(series: PlotSeries) -> None:
    """
    Validate that format options are compatible with the series plot type.

    Raises ExecutionError if invalid options are used.
    """
    fmt = series.format
    plot_type = series.plot_type

    # marker_color and marker_size only valid for scatter plots
    if fmt.marker_color and plot_type != PlotType.SCATTER:
        raise ExecutionError(
            f"marker_color is only valid for scatter plots, not {plot_type.value}"
        )
    if fmt.marker_size and plot_type != PlotType.SCATTER:
        raise ExecutionError(
            f"marker_size is only valid for scatter plots, not {plot_type.value}"
        )


def _execute_series(
    series: PlotSeries,
    base_df: pl.DataFrame,
    row_count: int,
) -> PlotData:
    """
    Execute a single series against a base dataframe.

    Args:
        series: The series definition
        base_df: The loaded dataframe (before any series-specific filtering)
        row_count: Total row count of the base dataframe

    Returns:
        PlotData for this series
    """
    # Validate format options for plot type
    validate_series_format_options(series)

    df = base_df

    # Get column names (from ColumnRef)
    x_col_name = series.x_column.name
    y_col_name = series.y_column.name

    # Validate columns exist
    for col in [x_col_name, y_col_name]:
        if col not in df.columns:
            available = ", ".join(df.columns)
            raise ExecutionError(
                f"Column '{col}' not found. Available: {available}"
            )

    # Apply filters (before aggregation)
    if series.filter:
        for cond in series.filter.conditions:
            if cond.column not in df.columns:
                available = ", ".join(df.columns)
                raise ExecutionError(
                    f"FILTER column '{cond.column}' not found. Available: {available}"
                )
        df = apply_where(df, series.filter)

    filtered_count = len(df)

    # Apply aggregation if needed
    if series.is_aggregate:
        df = apply_aggregation(df, series.x_column, series.y_column)
        # After aggregation, the counts change
        filtered_count = len(df)

    # Detect timestamp columns before extracting values
    x_timestamp, y_timestamp = detect_timestamp_columns(df, x_col_name, y_col_name)

    # Sort data based on plot type:
    # - LINE/SCATTER: sort ascending by x for proper visualization
    # - BAR/HIST: sort ascending by y (smallest bar first, largest last)
    if series.plot_type in (PlotType.LINE, PlotType.SCATTER):
        df = df.sort(x_col_name)
    elif series.plot_type in (PlotType.BAR, PlotType.HIST):
        df = df.sort(y_col_name)

    # Extract plot data
    x = df[x_col_name].to_list()
    y = df[y_col_name].to_list()

    # Extract dynamic format columns if they reference columns
    # (only valid for non-aggregated queries)
    marker_sizes = None
    marker_colors = None
    size_info = None
    color_info = None

    fmt = series.format
    if not series.is_aggregate:
        if fmt.marker_size:
            if fmt.marker_size in df.columns:
                # Column reference - map values to sizes
                raw_sizes = df[fmt.marker_size].to_list()
                marker_sizes, is_continuous = map_to_sizes(raw_sizes)

                # Build size info for legend
                if is_continuous:
                    valid_values = [float(v) for v in raw_sizes if v is not None]
                    size_info = SizeInfo(
                        is_continuous=True,
                        column_name=fmt.marker_size,
                        min_value=min(valid_values) if valid_values else 0,
                        max_value=max(valid_values) if valid_values else 0,
                    )
                else:
                    # Build category -> size mapping
                    unique_values = []
                    for v in raw_sizes:
                        if v not in unique_values:
                            unique_values.append(v)
                    n_categories = len(unique_values)
                    if n_categories == 1:
                        category_sizes = {unique_values[0]: 3.0}
                    else:
                        size_step = 4.0 / (n_categories - 1)
                        category_sizes = {
                            val: 1.0 + i * size_step
                            for i, val in enumerate(unique_values)
                        }
                    size_info = SizeInfo(
                        is_continuous=False,
                        column_name=fmt.marker_size,
                        category_sizes=category_sizes,
                    )
            else:
                # Try as literal number - create uniform size list
                try:
                    size_val = float(fmt.marker_size)
                    # Validate range (must be 1-5)
                    if size_val < 1.0 or size_val > 5.0:
                        raise ExecutionError(
                            f"marker_size must be between 1 and 5, got {size_val}"
                        )
                    marker_sizes = [size_val] * len(x)
                except ValueError:
                    raise ExecutionError(
                        f"marker_size '{fmt.marker_size}' is not a valid column name or number (1-5)"
                    )
        if fmt.marker_color:
            if fmt.marker_color in df.columns:
                # Column reference - map values to colors
                raw_colors = df[fmt.marker_color].to_list()
                marker_colors, is_continuous = map_to_colors(raw_colors)

                # Build color info for legend
                if is_continuous:
                    valid_values = [float(v) for v in raw_colors if v is not None]
                    color_info = ColorInfo(
                        is_continuous=True,
                        column_name=fmt.marker_color,
                        min_value=min(valid_values) if valid_values else 0,
                        max_value=max(valid_values) if valid_values else 0,
                    )
                else:
                    # Build category -> color mapping
                    from plotql.core.utils import BUCKET_COLORS
                    unique_values = []
                    for v in raw_colors:
                        if v not in unique_values:
                            unique_values.append(v)
                    category_colors = {
                        val: BUCKET_COLORS[i % len(BUCKET_COLORS)]
                        for i, val in enumerate(unique_values)
                    }
                    color_info = ColorInfo(
                        is_continuous=False,
                        column_name=fmt.marker_color,
                        category_colors=category_colors,
                    )
            elif fmt.marker_color.lower() in VALID_COLORS:
                # Valid literal color name - apply to all points
                marker_colors = [fmt.marker_color.lower()] * len(x)
            else:
                raise ExecutionError(
                    f"marker_color '{fmt.marker_color}' is not a valid column name or color. "
                    f"Valid colors: {', '.join(sorted(VALID_COLORS))}"
                )

    return PlotData(
        x=x,
        y=y,
        series=series,
        row_count=row_count,
        filtered_count=filtered_count,
        marker_sizes=marker_sizes,
        marker_colors=marker_colors,
        size_info=size_info,
        color_info=color_info,
        x_timestamp=x_timestamp,
        y_timestamp=y_timestamp,
    )


def execute(query: PlotQuery) -> List[PlotData]:
    """
    Execute a PlotQL query and return data ready for plotting.

    This function:
    1. Loads the data source (file, database, etc.) via connectors
    2. For each series: applies filters, aggregations, extracts data
    3. Returns list of PlotData (one per series) ready for visualization

    Later series in the list should be rendered on top of earlier ones.

    For connectors that support filter pushdown (like ClickHouse), filters
    are passed to the connector which handles combining and pushing them down.
    """
    # Collect all series filters for potential pushdown
    filters = [s.filter for s in query.series if s.filter is not None]

    # Load data via connector abstraction, with filters for potential pushdown
    df, _ = load_data(query.source, filters=filters)
    row_count = len(df)

    # Execute each series
    # Series still apply their own filters (pushdown is optimization only)
    results = []
    for series in query.series:
        plot_data = _execute_series(series, df, row_count)
        results.append(plot_data)

    return results
