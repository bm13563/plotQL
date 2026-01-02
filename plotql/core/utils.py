"""
Utility functions for PlotQL core.

Contains data transformations for rendering and timestamp detection.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

import polars as pl


# =============================================================================
# Size Normalization (for scatter plot markers)
# =============================================================================

def normalize_sizes(
    values: List[float],
    min_size: float = 1.0,
    max_size: float = 5.0
) -> List[float]:
    """
    Normalize a list of values to a range suitable for marker sizes.

    Uses min-max normalization to scale values between min_size and max_size.
    Handles edge cases like constant values or None/NaN.
    """
    # Filter out None/NaN and convert to float
    clean_values = []
    for v in values:
        try:
            if v is not None:
                clean_values.append(float(v))
            else:
                clean_values.append(None)
        except (TypeError, ValueError):
            clean_values.append(None)

    # Get valid values for statistics
    valid = [v for v in clean_values if v is not None]

    if not valid:
        return [min_size] * len(values)

    val_min = min(valid)
    val_max = max(valid)
    val_range = val_max - val_min

    # Handle constant values (no variance)
    if val_range == 0:
        mid_size = (min_size + max_size) / 2
        return [mid_size if v is not None else min_size for v in clean_values]

    # Normalize to [min_size, max_size]
    size_range = max_size - min_size
    normalized = []
    for v in clean_values:
        if v is None:
            normalized.append(min_size)
        else:
            # Scale to [0, 1] then to [min_size, max_size]
            scaled = (v - val_min) / val_range
            normalized.append(min_size + scaled * size_range)

    return normalized


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
