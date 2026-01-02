"""
Unit tests for plotql.core.utils module.

Tests size mapping, color mapping, and timestamp detection utilities.
"""
import pytest
import polars as pl

from plotql.core.utils import (
    BUCKET_COLORS,
    GRADIENT_END,
    GRADIENT_START,
    SIZE_MAX,
    SIZE_MIN,
    TimestampInfo,
    detect_datetime_format,
    detect_timestamp_columns,
    interpolate_color,
    is_datetime_column,
    map_to_colors,
    map_to_sizes,
)


# =============================================================================
# Constants Tests
# =============================================================================

class TestConstants:
    """Tests for module constants."""

    def test_size_range(self):
        """Test size range constants."""
        assert SIZE_MIN == 1.0
        assert SIZE_MAX == 5.0
        assert SIZE_MIN < SIZE_MAX

    def test_bucket_colors(self):
        """Test bucket colors list."""
        assert len(BUCKET_COLORS) == 5
        assert "blue" in BUCKET_COLORS
        assert "green" in BUCKET_COLORS
        assert "yellow" in BUCKET_COLORS
        assert "pink" in BUCKET_COLORS
        assert "teal" in BUCKET_COLORS

    def test_gradient_colors(self):
        """Test gradient endpoint colors."""
        assert len(GRADIENT_START) == 3
        assert len(GRADIENT_END) == 3
        # All RGB values should be 0-255
        assert all(0 <= v <= 255 for v in GRADIENT_START)
        assert all(0 <= v <= 255 for v in GRADIENT_END)


# =============================================================================
# map_to_sizes Tests
# =============================================================================

class TestMapToSizes:
    """Tests for map_to_sizes function."""

    def test_empty_list(self):
        """Test with empty list."""
        sizes, is_continuous = map_to_sizes([])
        assert sizes == []
        assert is_continuous is False

    def test_single_numeric_value(self):
        """Test with single numeric value."""
        sizes, is_continuous = map_to_sizes([5])
        assert len(sizes) == 1
        assert sizes[0] == 3.0  # Middle size for single value
        assert is_continuous is True

    def test_two_numeric_values(self):
        """Test with two numeric values."""
        sizes, is_continuous = map_to_sizes([0, 10])
        assert len(sizes) == 2
        assert sizes[0] == SIZE_MIN  # 0 maps to min
        assert sizes[1] == SIZE_MAX  # 10 maps to max
        assert is_continuous is True

    def test_numeric_values_range(self):
        """Test numeric values are mapped to 1-5 range."""
        values = [0, 25, 50, 75, 100]
        sizes, is_continuous = map_to_sizes(values)

        assert len(sizes) == 5
        assert sizes[0] == SIZE_MIN
        assert sizes[4] == SIZE_MAX
        # Middle value should be mid-range
        assert sizes[2] == pytest.approx(3.0)
        assert is_continuous is True

    def test_all_same_numeric_values(self):
        """Test when all numeric values are the same."""
        sizes, is_continuous = map_to_sizes([5, 5, 5, 5])
        assert len(sizes) == 4
        # All should be middle size
        assert all(s == 3.0 for s in sizes)
        assert is_continuous is True

    def test_negative_values(self):
        """Test with negative values."""
        sizes, is_continuous = map_to_sizes([-10, 0, 10])
        assert sizes[0] == SIZE_MIN
        assert sizes[2] == SIZE_MAX
        assert is_continuous is True

    def test_float_values(self):
        """Test with float values."""
        sizes, is_continuous = map_to_sizes([0.0, 0.5, 1.0])
        assert sizes[0] == SIZE_MIN
        assert sizes[2] == SIZE_MAX
        assert is_continuous is True

    def test_categorical_values(self):
        """Test with categorical (string) values."""
        values = ["A", "B", "C"]
        sizes, is_continuous = map_to_sizes(values)

        assert len(sizes) == 3
        assert all(SIZE_MIN <= s <= SIZE_MAX for s in sizes)
        assert is_continuous is False

    def test_categorical_values_same_size_per_category(self):
        """Test that same category gets same size."""
        values = ["A", "B", "A", "B", "A"]
        sizes, is_continuous = map_to_sizes(values)

        # All A's should have same size
        a_sizes = [s for v, s in zip(values, sizes) if v == "A"]
        assert all(s == a_sizes[0] for s in a_sizes)

    def test_single_category(self):
        """Test with single category repeated."""
        sizes, is_continuous = map_to_sizes(["A", "A", "A"])
        assert len(sizes) == 3
        # Single category gets middle size
        assert all(s == 3.0 for s in sizes)
        assert is_continuous is False

    def test_none_values_numeric(self):
        """Test None values in numeric list."""
        sizes, is_continuous = map_to_sizes([0, None, 10])
        assert len(sizes) == 3
        assert sizes[1] == SIZE_MIN  # None maps to minimum
        assert is_continuous is True

    def test_all_none_values(self):
        """Test all None values."""
        sizes, is_continuous = map_to_sizes([None, None, None])
        assert len(sizes) == 3
        # All None -> middle size
        assert all(s == 3.0 for s in sizes)
        assert is_continuous is True

    def test_mixed_types_becomes_categorical(self):
        """Test that mixed types are treated as categorical."""
        values = [1, "A", 2]
        sizes, is_continuous = map_to_sizes(values)
        assert is_continuous is False

    def test_num_buckets_parameter(self):
        """Test num_buckets parameter for categorical."""
        values = list(range(10))  # 0-9 as strings
        values = [str(v) for v in values]
        sizes, _ = map_to_sizes(values, num_buckets=5)
        # Should still work with 10 categories
        assert len(sizes) == 10


# =============================================================================
# interpolate_color Tests
# =============================================================================

class TestInterpolateColor:
    """Tests for interpolate_color function."""

    def test_interpolate_at_zero(self):
        """Test interpolation at t=0 returns start color."""
        color = interpolate_color(0.0)
        assert color.startswith("#")
        # Should be close to GRADIENT_START
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        assert r == GRADIENT_START[0]
        assert g == GRADIENT_START[1]
        assert b == GRADIENT_START[2]

    def test_interpolate_at_one(self):
        """Test interpolation at t=1 returns end color."""
        color = interpolate_color(1.0)
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        assert r == GRADIENT_END[0]
        assert g == GRADIENT_END[1]
        assert b == GRADIENT_END[2]

    def test_interpolate_at_half(self):
        """Test interpolation at t=0.5."""
        color = interpolate_color(0.5)
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        # Should be midpoint of each channel
        expected_r = int((GRADIENT_START[0] + GRADIENT_END[0]) / 2)
        expected_g = int((GRADIENT_START[1] + GRADIENT_END[1]) / 2)
        expected_b = int((GRADIENT_START[2] + GRADIENT_END[2]) / 2)
        # Allow for rounding differences
        assert abs(r - expected_r) <= 1
        assert abs(g - expected_g) <= 1
        assert abs(b - expected_b) <= 1

    def test_interpolate_returns_hex_format(self):
        """Test that result is valid hex color."""
        color = interpolate_color(0.5)
        assert color.startswith("#")
        assert len(color) == 7
        # Should be valid hex
        int(color[1:], 16)

    def test_interpolate_clamps_negative(self):
        """Test that negative t is clamped to 0."""
        color = interpolate_color(-0.5)
        assert color == interpolate_color(0.0)

    def test_interpolate_clamps_over_one(self):
        """Test that t > 1 is clamped to 1."""
        color = interpolate_color(1.5)
        assert color == interpolate_color(1.0)


# =============================================================================
# map_to_colors Tests
# =============================================================================

class TestMapToColors:
    """Tests for map_to_colors function."""

    def test_empty_list(self):
        """Test with empty list."""
        colors, is_continuous = map_to_colors([])
        assert colors == []
        assert is_continuous is False

    def test_single_numeric_value(self):
        """Test with single numeric value."""
        colors, is_continuous = map_to_colors([5])
        assert len(colors) == 1
        assert colors[0].startswith("#")  # Middle gradient color
        assert is_continuous is True

    def test_two_numeric_values(self):
        """Test with two numeric values."""
        colors, is_continuous = map_to_colors([0, 10])
        assert len(colors) == 2
        assert colors[0] == interpolate_color(0.0)
        assert colors[1] == interpolate_color(1.0)
        assert is_continuous is True

    def test_numeric_gradient(self):
        """Test numeric values get gradient colors."""
        values = [0, 50, 100]
        colors, is_continuous = map_to_colors(values)

        assert all(c.startswith("#") for c in colors)
        assert is_continuous is True

    def test_all_same_numeric_values(self):
        """Test when all numeric values are the same."""
        colors, is_continuous = map_to_colors([5, 5, 5])
        assert all(c == interpolate_color(0.5) for c in colors)
        assert is_continuous is True

    def test_categorical_values(self):
        """Test with categorical values."""
        values = ["A", "B", "C"]
        colors, is_continuous = map_to_colors(values)

        assert len(colors) == 3
        assert all(c in BUCKET_COLORS for c in colors)
        assert is_continuous is False

    def test_categorical_consistent_mapping(self):
        """Test that same category gets same color."""
        values = ["A", "B", "A", "B"]
        colors, is_continuous = map_to_colors(values)

        assert colors[0] == colors[2]  # Both A
        assert colors[1] == colors[3]  # Both B

    def test_categorical_exceeds_palette(self):
        """Test categories exceeding palette size cycle."""
        # More categories than BUCKET_COLORS
        values = ["A", "B", "C", "D", "E", "F", "G"]
        colors, is_continuous = map_to_colors(values)

        # Should cycle back
        assert colors[5] == colors[0]  # 6th category = 1st color

    def test_none_values_numeric(self):
        """Test None values in numeric list."""
        colors, is_continuous = map_to_colors([0, None, 10])
        assert len(colors) == 3
        # None should get start color
        assert colors[1] == interpolate_color(0.0)
        assert is_continuous is True

    def test_all_none_values(self):
        """Test all None values."""
        colors, is_continuous = map_to_colors([None, None])
        # All None -> middle gradient color
        assert all(c == interpolate_color(0.5) for c in colors)
        assert is_continuous is True

    def test_max_colors_parameter(self):
        """Test max_colors parameter."""
        values = ["A", "B", "C", "D", "E", "F"]
        colors, _ = map_to_colors(values, max_colors=3)
        # Should only use first 3 palette colors
        unique_colors = set(colors)
        assert len(unique_colors) <= 3


# =============================================================================
# detect_datetime_format Tests
# =============================================================================

class TestDetectDatetimeFormat:
    """Tests for detect_datetime_format function."""

    def test_iso_with_microseconds(self):
        """Test ISO format with microseconds."""
        result = detect_datetime_format("2026-01-01 21:58:52.909000")
        assert result is not None
        assert "Y-m-d" in result[0]

    def test_iso_with_t_separator(self):
        """Test ISO format with T separator."""
        result = detect_datetime_format("2026-01-01T21:58:52")
        assert result is not None

    def test_iso_date_only(self):
        """Test ISO date only."""
        result = detect_datetime_format("2026-01-01")
        assert result is not None
        assert result[0] == "Y-m-d"

    def test_us_format_with_time(self):
        """Test US date format with time."""
        result = detect_datetime_format("01/01/2026 21:58:52")
        assert result is not None
        assert "m/d/Y" in result[0]

    def test_us_date_only(self):
        """Test US date format only."""
        result = detect_datetime_format("01/01/2026")
        assert result is not None
        assert result[0] == "m/d/Y"

    def test_european_format(self):
        """Test European date format."""
        result = detect_datetime_format("01-01-2026")
        assert result is not None
        assert result[0] == "d-m-Y"

    def test_time_only(self):
        """Test time only format."""
        result = detect_datetime_format("21:58:52")
        assert result is not None
        assert result[0] == "H:M:S"

    def test_time_with_microseconds(self):
        """Test time with microseconds."""
        result = detect_datetime_format("21:58:52.909000")
        assert result is not None
        assert "H:M:S" in result[0]

    def test_not_datetime(self):
        """Test non-datetime string."""
        result = detect_datetime_format("hello world")
        assert result is None

    def test_number_string(self):
        """Test number string."""
        result = detect_datetime_format("12345")
        assert result is None

    def test_empty_string(self):
        """Test empty string."""
        result = detect_datetime_format("")
        assert result is None

    def test_whitespace_handling(self):
        """Test whitespace is stripped."""
        result = detect_datetime_format("  2026-01-01  ")
        assert result is not None


# =============================================================================
# is_datetime_column Tests
# =============================================================================

class TestIsDatetimeColumn:
    """Tests for is_datetime_column function."""

    def test_polars_datetime_type(self):
        """Test Polars Datetime column."""
        series = pl.Series("ts", []).cast(pl.Datetime)
        result = is_datetime_column(series)
        assert result is not None

    def test_polars_date_type(self):
        """Test Polars Date column."""
        series = pl.Series("dt", []).cast(pl.Date)
        result = is_datetime_column(series)
        assert result is not None

    def test_string_datetime_column(self):
        """Test string column with datetime values."""
        series = pl.Series("ts", ["2026-01-01 10:00:00", "2026-01-02 11:00:00"])
        result = is_datetime_column(series)
        assert result is not None

    def test_string_non_datetime_column(self):
        """Test string column without datetime values."""
        series = pl.Series("s", ["hello", "world"])
        result = is_datetime_column(series)
        assert result is None

    def test_numeric_column(self):
        """Test numeric column."""
        series = pl.Series("n", [1, 2, 3, 4, 5])
        result = is_datetime_column(series)
        assert result is None

    def test_empty_series(self):
        """Test empty series."""
        series = pl.Series("empty", [], dtype=pl.Utf8)
        result = is_datetime_column(series)
        assert result is None

    def test_series_with_nulls(self):
        """Test series with null values but valid datetimes."""
        series = pl.Series("ts", ["2026-01-01", None, "2026-01-02"])
        result = is_datetime_column(series)
        assert result is not None


# =============================================================================
# detect_timestamp_columns Tests
# =============================================================================

class TestDetectTimestampColumns:
    """Tests for detect_timestamp_columns function."""

    def test_both_columns_timestamp(self):
        """Test when both columns are timestamps."""
        df = pl.DataFrame({
            "x": ["2026-01-01", "2026-01-02"],
            "y": ["2026-02-01", "2026-02-02"],
        })
        x_info, y_info = detect_timestamp_columns(df, "x", "y")
        assert x_info is not None
        assert y_info is not None

    def test_only_x_timestamp(self):
        """Test when only x column is timestamp."""
        df = pl.DataFrame({
            "x": ["2026-01-01", "2026-01-02"],
            "y": [1, 2],
        })
        x_info, y_info = detect_timestamp_columns(df, "x", "y")
        assert x_info is not None
        assert y_info is None

    def test_only_y_timestamp(self):
        """Test when only y column is timestamp."""
        df = pl.DataFrame({
            "x": [1, 2],
            "y": ["2026-01-01", "2026-01-02"],
        })
        x_info, y_info = detect_timestamp_columns(df, "x", "y")
        assert x_info is None
        assert y_info is not None

    def test_neither_timestamp(self):
        """Test when neither column is timestamp."""
        df = pl.DataFrame({
            "x": [1, 2],
            "y": [3, 4],
        })
        x_info, y_info = detect_timestamp_columns(df, "x", "y")
        assert x_info is None
        assert y_info is None

    def test_timestamp_info_fields(self):
        """Test TimestampInfo has correct fields."""
        df = pl.DataFrame({
            "ts": ["2026-01-01 10:00:00", "2026-01-02 11:00:00"],
            "v": [1, 2],
        })
        x_info, _ = detect_timestamp_columns(df, "ts", "v")

        assert isinstance(x_info, TimestampInfo)
        assert x_info.column_name == "ts"
        assert x_info.input_format is not None
        assert x_info.output_format is not None


# =============================================================================
# TimestampInfo Tests
# =============================================================================

class TestTimestampInfo:
    """Tests for TimestampInfo dataclass."""

    def test_timestamp_info_creation(self):
        """Test creating TimestampInfo."""
        info = TimestampInfo(
            column_name="timestamp",
            input_format="Y-m-d H:M:S",
            output_format="H:M:S",
        )
        assert info.column_name == "timestamp"
        assert info.input_format == "Y-m-d H:M:S"
        assert info.output_format == "H:M:S"

    def test_timestamp_info_equality(self):
        """Test TimestampInfo equality."""
        info1 = TimestampInfo("ts", "Y-m-d", "Y-m-d")
        info2 = TimestampInfo("ts", "Y-m-d", "Y-m-d")
        assert info1 == info2


# =============================================================================
# Edge Cases and Integration
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_size_mapping_preserves_order(self):
        """Test that size mapping preserves value order."""
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        sizes, _ = map_to_sizes(values)

        # Higher values should have higher sizes
        val_size_pairs = list(zip(values, sizes))
        for i, (v1, s1) in enumerate(val_size_pairs):
            for v2, s2 in val_size_pairs[i + 1:]:
                if v1 < v2:
                    assert s1 <= s2

    def test_color_mapping_preserves_order(self):
        """Test that continuous color mapping preserves value order."""
        values = [0, 50, 100]
        colors, _ = map_to_colors(values)

        # Colors should progress through gradient
        # Can check by comparing individual channels
        def hex_to_rgb(hex_color):
            return (
                int(hex_color[1:3], 16),
                int(hex_color[3:5], 16),
                int(hex_color[5:7], 16),
            )

        rgb0 = hex_to_rgb(colors[0])
        rgb100 = hex_to_rgb(colors[2])

        # Start should be closer to GRADIENT_START
        assert rgb0[0] == GRADIENT_START[0]
        # End should be closer to GRADIENT_END
        assert rgb100[0] == GRADIENT_END[0]

    def test_very_large_values(self):
        """Test with very large numeric values."""
        values = [0, 1e10, 2e10]
        sizes, is_continuous = map_to_sizes(values)
        colors, _ = map_to_colors(values)

        assert len(sizes) == 3
        assert len(colors) == 3
        assert all(SIZE_MIN <= s <= SIZE_MAX for s in sizes)

    def test_very_small_float_differences(self):
        """Test with very small float differences."""
        values = [1.0, 1.0000001, 1.0000002]
        sizes, _ = map_to_sizes(values)

        # Should still map across range
        assert len(sizes) == 3
        assert sizes[0] < sizes[2]  # Order preserved

    def test_unicode_categorical_values(self):
        """Test with unicode categorical values."""
        values = ["", "", ""]
        colors, is_continuous = map_to_colors(values)

        assert len(colors) == 3
        assert is_continuous is False
