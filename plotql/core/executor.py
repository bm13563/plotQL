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
    PlotType,
    WhereClause,
)
from plotql.core.utils import normalize_sizes, TimestampInfo, detect_timestamp_columns


class ExecutionError(Exception):
    """Raised when query execution fails."""
    pass


@dataclass
class PlotData:
    """Result of executing a query - ready for plotting."""
    x: List[float]
    y: List[float]
    query: PlotQuery
    row_count: int
    filtered_count: int
    # Optional columns for dynamic formatting
    marker_sizes: Optional[List[float]] = None
    marker_colors: Optional[List[str]] = None
    # Timestamp info for datetime axes
    x_timestamp: Optional[TimestampInfo] = None
    y_timestamp: Optional[TimestampInfo] = None


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


def execute(query: PlotQuery) -> PlotData:
    """
    Execute a PlotQL query and return data ready for plotting.

    This function:
    1. Loads the source file with Polars
    2. Applies any WHERE filters
    3. Applies aggregations if specified
    4. Extracts x and y columns
    5. Returns PlotData ready for visualization
    """
    # Validate format options for plot type
    validate_format_options(query)

    # Load data
    df = load_file(query.source)
    row_count = len(df)

    # Get column names (from ColumnRef)
    x_col_name = query.x_column.name
    y_col_name = query.y_column.name

    # Validate columns exist
    for col in [x_col_name, y_col_name]:
        if col not in df.columns:
            available = ", ".join(df.columns)
            raise ExecutionError(
                f"Column '{col}' not found. Available: {available}"
            )

    # Apply filters (before aggregation)
    if query.filter:
        for cond in query.filter.conditions:
            if cond.column not in df.columns:
                available = ", ".join(df.columns)
                raise ExecutionError(
                    f"FILTER column '{cond.column}' not found. Available: {available}"
                )
        df = apply_where(df, query.filter)

    filtered_count = len(df)

    # Apply aggregation if needed
    if query.is_aggregate:
        df = apply_aggregation(df, query.x_column, query.y_column)
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

    fmt = query.format
    if not query.is_aggregate:
        if fmt.marker_size:
            if fmt.marker_size in df.columns:
                # Column reference - normalize values
                raw_sizes = df[fmt.marker_size].to_list()
                marker_sizes = normalize_sizes(raw_sizes)
            else:
                # Try as literal number - create uniform size list
                try:
                    size_val = float(fmt.marker_size)
                    # Clamp to valid range (1-5)
                    size_val = max(1.0, min(5.0, size_val))
                    marker_sizes = [size_val] * len(x)
                except ValueError:
                    pass  # Not a valid number, ignore
        if fmt.marker_color and fmt.marker_color in df.columns:
            marker_colors = df[fmt.marker_color].to_list()

    return PlotData(
        x=x,
        y=y,
        query=query,
        row_count=row_count,
        filtered_count=filtered_count,
        marker_sizes=marker_sizes,
        marker_colors=marker_colors,
        x_timestamp=x_timestamp,
        y_timestamp=y_timestamp,
    )
