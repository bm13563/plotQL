"""
Query executor - loads data with Polars and prepares it for plotting.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import polars as pl

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    ComparisonOp,
    LogicalOp,
    PlotQuery,
    PlotSeries,
    PlotType,
    WhereClause,
)
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
    x: List[float]
    y: List[float]
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

    # Backward compatibility - delegate to series
    @property
    def query(self) -> PlotSeries:
        """Backward compatibility alias for series."""
        return self.series


def load_file(path: str) -> pl.DataFrame:
    """
    Load a data file into a Polars DataFrame.

    Supports: CSV, Parquet, JSON, NDJSON
    """
    p = Path(path)

    if not p.exists():
        raise ExecutionError(f"File not found: {path}")

    suffix = p.suffix.lower()

    try:
        if suffix == ".csv":
            return pl.read_csv(path)
        elif suffix == ".parquet":
            return pl.read_parquet(path)
        elif suffix == ".json":
            return pl.read_json(path)
        elif suffix == ".ndjson":
            return pl.read_ndjson(path)
        else:
            # Try CSV as default
            return pl.read_csv(path)
    except Exception as e:
        raise ExecutionError(f"Failed to load {path}: {e}")


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


def validate_format_options(query: PlotQuery) -> None:
    """
    Validate that format options are compatible with the plot type.

    Raises ExecutionError if invalid options are used.
    """
    fmt = query.format
    plot_type = query.plot_type

    # marker_color and marker_size only valid for scatter plots
    if fmt.marker_color and plot_type != PlotType.SCATTER:
        raise ExecutionError(
            f"marker_color is only valid for scatter plots, not {plot_type.value}"
        )
    if fmt.marker_size and plot_type != PlotType.SCATTER:
        raise ExecutionError(
            f"marker_size is only valid for scatter plots, not {plot_type.value}"
        )


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
    1. Loads the source file with Polars
    2. For each series: applies filters, aggregations, extracts data
    3. Returns list of PlotData (one per series) ready for visualization

    Later series in the list should be rendered on top of earlier ones.
    """
    # Load data once
    df = load_file(query.source)
    row_count = len(df)

    # Execute each series
    results = []
    for series in query.series:
        plot_data = _execute_series(series, df, row_count)
        results.append(plot_data)

    return results
