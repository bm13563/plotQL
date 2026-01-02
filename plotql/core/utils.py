"""
Utility functions for PlotQL core.

Contains data transformations for rendering and timestamp detection.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

import polars as pl

from plotql.themes import THEME


# =============================================================================
# Size Mapping (for scatter plot markers)
# =============================================================================

# Size range for markers (1.0 to 5.0)
SIZE_MIN = 1.0
SIZE_MAX = 5.0


def map_to_sizes(
    values: List,
    num_buckets: int = 5,
) -> tuple[List[float], bool]:
    """
    Map a list of values to marker sizes (1.0 to 5.0).

    For numeric data: uses continuous linear interpolation.
    For categorical data: maps unique values to discrete size buckets.

    Args:
        values: List of values (numeric or categorical)
        num_buckets: Number of size buckets for categorical data (default 5)

    Returns:
        Tuple of (list of sizes from 1.0-5.0, is_continuous)
    """
    if not values:
        return [], False

    # Check if values are numeric by trying to convert them
    numeric_values = []
    is_numeric = True
    for v in values:
        if v is None:
            numeric_values.append(None)
        else:
            try:
                numeric_values.append(float(v))
            except (TypeError, ValueError):
                is_numeric = False
                break

    if is_numeric:
        # Use continuous interpolation for numeric data
        valid = [v for v in numeric_values if v is not None]
        if not valid:
            mid_size = (SIZE_MIN + SIZE_MAX) / 2
            return [mid_size] * len(values), True

        val_min = min(valid)
        val_max = max(valid)
        val_range = val_max - val_min

        if val_range == 0:
            # All values the same - use middle size
            mid_size = (SIZE_MIN + SIZE_MAX) / 2
            return [mid_size] * len(values), True

        size_range = SIZE_MAX - SIZE_MIN
        result = []
        for v in numeric_values:
            if v is None:
                result.append(SIZE_MIN)
            else:
                t = (v - val_min) / val_range
                result.append(SIZE_MIN + t * size_range)
        return result, True
    else:
        # For categorical data, map unique values to discrete sizes
        unique_values = []
        for v in values:
            if v not in unique_values:
                unique_values.append(v)

        # Calculate size for each category
        n_categories = len(unique_values)
        if n_categories == 1:
            size_step = 0
            base_size = (SIZE_MIN + SIZE_MAX) / 2
        else:
            size_step = (SIZE_MAX - SIZE_MIN) / (n_categories - 1)
            base_size = SIZE_MIN

        value_to_size = {}
        for i, val in enumerate(unique_values):
            value_to_size[val] = base_size + i * size_step

        return [value_to_size[v] for v in values], False


# Default color palette for categorical colors (5 distinct colors)
BUCKET_COLORS = ["blue", "green", "yellow", "pink", "teal"]


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


# Gradient endpoints from theme (converted to RGB for interpolation)
GRADIENT_START = _hex_to_rgb(THEME.gradient[0])
GRADIENT_END = _hex_to_rgb(THEME.gradient[1])


def interpolate_color(t: float) -> str:
    """
    Interpolate between gradient start and end colors.

    Args:
        t: Value between 0 and 1

    Returns:
        Hex color string
    """
    t = max(0.0, min(1.0, t))
    r = int(GRADIENT_START[0] + t * (GRADIENT_END[0] - GRADIENT_START[0]))
    g = int(GRADIENT_START[1] + t * (GRADIENT_END[1] - GRADIENT_START[1]))
    b = int(GRADIENT_START[2] + t * (GRADIENT_END[2] - GRADIENT_START[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def map_to_colors(
    values: List,
    max_colors: int = 5,
) -> tuple[List[str], bool]:
    """
    Map a list of values to colors.

    For numeric data: uses continuous gradient interpolation.
    For categorical data: maps unique values to discrete colors.

    Args:
        values: List of values (numeric or categorical)
        max_colors: Maximum number of colors for categorical data (default 5)

    Returns:
        Tuple of (list of color strings, is_continuous)
        - For continuous: hex color strings (e.g., "#89b4fa")
        - For categorical: color names (e.g., "blue", "green")
    """
    if not values:
        return [], False

    colors = BUCKET_COLORS[:max_colors]

    # Check if values are numeric by trying to convert them
    numeric_values = []
    is_numeric = True
    for v in values:
        if v is None:
            numeric_values.append(None)
        else:
            try:
                numeric_values.append(float(v))
            except (TypeError, ValueError):
                is_numeric = False
                break

    if is_numeric:
        # Use continuous gradient for numeric data
        valid = [v for v in numeric_values if v is not None]
        if not valid:
            return [interpolate_color(0.5)] * len(values), True

        val_min = min(valid)
        val_max = max(valid)
        val_range = val_max - val_min

        if val_range == 0:
            # All values the same - use middle color
            return [interpolate_color(0.5)] * len(values), True

        result = []
        for v in numeric_values:
            if v is None:
                result.append(interpolate_color(0.0))
            else:
                t = (v - val_min) / val_range
                result.append(interpolate_color(t))
        return result, True
    else:
        # For categorical data, map unique values to colors
        unique_values = []
        for v in values:
            if v not in unique_values:
                unique_values.append(v)

        # Create mapping from value to color (cycle if more than max_colors)
        value_to_color = {}
        for i, val in enumerate(unique_values):
            value_to_color[val] = colors[i % max_colors]

        return [value_to_color[v] for v in values], False


# =============================================================================
# Timestamp Detection and Conversion
# =============================================================================

@dataclass
class TimestampInfo:
    """Information about a detected timestamp column."""
    column_name: str
    input_format: str
    output_format: str


# Mapping of regex patterns to (input_format, output_format)
DATETIME_PATTERNS = [
    # ISO format with microseconds: 2026-01-01 21:58:52.909000
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$", "Y-m-d H:M:S.f", "H:M:S"),
    # ISO format with T separator and microseconds
    (r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$", "Y-m-dTH:M:S.f", "H:M:S"),
    # ISO format: 2026-01-01 21:58:52
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", "Y-m-d H:M:S", "m-d H:M"),
    # ISO format with T: 2026-01-01T21:58:52
    (r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", "Y-m-dTH:M:S", "m-d H:M"),
    # ISO date only: 2026-01-01
    (r"^\d{4}-\d{2}-\d{2}$", "Y-m-d", "Y-m-d"),
    # US format with time: 01/01/2026 21:58:52
    (r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$", "m/d/Y H:M:S", "m/d H:M"),
    # US date: 01/01/2026
    (r"^\d{2}/\d{2}/\d{4}$", "m/d/Y", "m/d/Y"),
    # European format: 01-01-2026
    (r"^\d{2}-\d{2}-\d{4}$", "d-m-Y", "d-m-Y"),
    # Time only: 21:58:52
    (r"^\d{2}:\d{2}:\d{2}$", "H:M:S", "H:M:S"),
    # Time with microseconds: 21:58:52.909000
    (r"^\d{2}:\d{2}:\d{2}\.\d+$", "H:M:S.f", "H:M:S"),
]


def detect_datetime_format(sample: str) -> Optional[Tuple[str, str]]:
    """
    Detect the datetime format of a sample string.

    Returns (input_format, output_format) if detected, None otherwise.
    """
    sample = sample.strip()

    for pattern, input_fmt, output_fmt in DATETIME_PATTERNS:
        if re.match(pattern, sample):
            return input_fmt, output_fmt

    return None


def is_datetime_column(series: pl.Series) -> Optional[Tuple[str, str]]:
    """
    Check if a Polars series contains datetime values.

    Returns (input_format, output_format) if datetime, None otherwise.
    """
    # Check if already a Polars datetime type
    if series.dtype in (pl.Datetime, pl.Date):
        return "Y-m-d H:M:S", "m-d H:M"

    # Check if string that looks like datetime
    if series.dtype in (pl.Utf8, pl.String):
        non_null = series.drop_nulls()
        if len(non_null) == 0:
            return None

        samples = non_null.head(5).to_list()
        result = detect_datetime_format(str(samples[0]))
        if result:
            return result

    return None


def detect_timestamp_columns(
    df: pl.DataFrame,
    x_col: str,
    y_col: str
) -> Tuple[Optional[TimestampInfo], Optional[TimestampInfo]]:
    """
    Detect datetime columns and return format info.

    Returns (x_timestamp_info, y_timestamp_info).
    """
    x_info = None
    y_info = None

    # Check X column
    formats = is_datetime_column(df[x_col])
    if formats:
        x_info = TimestampInfo(
            column_name=x_col,
            input_format=formats[0],
            output_format=formats[1],
        )

    # Check Y column
    formats = is_datetime_column(df[y_col])
    if formats:
        y_info = TimestampInfo(
            column_name=y_col,
            input_format=formats[0],
            output_format=formats[1],
        )

    return x_info, y_info
