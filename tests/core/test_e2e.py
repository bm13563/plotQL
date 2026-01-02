"""
End-to-end tests for plotql.core module.

Tests the complete pipeline from query string to rendered output.
"""
from pathlib import Path

import pytest

from plotql.core import execute, parse, render
from plotql.core.engines import get_engine


# =============================================================================
# Full Pipeline E2E Tests
# =============================================================================

class TestFullPipeline:
    """Test complete parse -> execute -> render pipeline."""

    def test_simple_scatter(self, temp_csv: Path):
        """Test simple scatter plot end-to-end."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x"

        # Parse
        ast = parse(query_str)
        assert ast.source == str(temp_csv)

        # Execute
        data_list = execute(ast)
        data = data_list[0]
        assert len(data.x) == 5
        assert len(data.y) == 5

        # Render
        result = render(data)
        png_bytes = result.to_bytes()
        assert png_bytes[:4] == b"\x89PNG"
        result.close()

    def test_line_plot(self, temp_csv: Path):
        """Test line plot end-to-end."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x AS 'line'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        result = render(data)

        assert result.to_bytes()
        result.close()

    def test_bar_plot(self, temp_csv_categorical: Path):
        """Test bar plot with aggregation end-to-end."""
        query_str = f"WITH '{temp_csv_categorical}' PLOT sum(amount) AGAINST group AS 'bar'"

        ast = parse(query_str)
        assert ast.is_aggregate

        data_list = execute(ast)
        data = data_list[0]
        assert data.filtered_count == 3  # 3 groups

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_histogram(self, temp_csv: Path):
        """Test histogram end-to-end."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x AS 'hist'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        result = render(data)

        assert result.to_bytes()
        result.close()


class TestFilteredQueries:
    """Test queries with FILTER clause."""

    def test_filter_equals(self, temp_csv: Path):
        """Test FILTER with equals condition."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FILTER category = 'A'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        # Original has 5 rows, 3 are category A
        assert data.row_count == 5
        assert data.filtered_count == 3

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_filter_greater_than(self, temp_csv: Path):
        """Test FILTER with greater than condition."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FILTER x > 2"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.filtered_count == 3  # x=3,4,5

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_filter_compound_and(self, temp_csv: Path):
        """Test FILTER with AND operator."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FILTER x > 1 AND x < 5"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.filtered_count == 3  # x=2,3,4

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_filter_compound_or(self, temp_csv: Path):
        """Test FILTER with OR operator."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FILTER x = 1 OR x = 5"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.filtered_count == 2  # x=1,5

        result = render(data)
        assert result.to_bytes()
        result.close()


class TestAggregationQueries:
    """Test queries with aggregation functions."""

    def test_count_aggregation(self, temp_csv_categorical: Path):
        """Test COUNT aggregation."""
        query_str = f"WITH '{temp_csv_categorical}' PLOT count(amount) AGAINST group AS 'bar'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        # Each group has 2 entries
        assert data.filtered_count == 3
        assert all(y == 2 for y in data.y)

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_sum_aggregation(self, temp_csv_categorical: Path):
        """Test SUM aggregation."""
        query_str = f"WITH '{temp_csv_categorical}' PLOT sum(amount) AGAINST group AS 'bar'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        # Verify sums: A=30, B=70, C=110
        total = sum(data.y)
        assert total == 210

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_avg_aggregation(self, temp_csv_categorical: Path):
        """Test AVG aggregation."""
        query_str = f"WITH '{temp_csv_categorical}' PLOT avg(amount) AGAINST group AS 'bar'"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.filtered_count == 3

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_min_max_aggregation(self, temp_csv_categorical: Path):
        """Test MIN and MAX aggregation."""
        # MIN
        query_str = f"WITH '{temp_csv_categorical}' PLOT min(amount) AGAINST group AS 'bar'"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert data.filtered_count == 3

        # MAX
        query_str = f"WITH '{temp_csv_categorical}' PLOT max(amount) AGAINST group AS 'bar'"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert data.filtered_count == 3


class TestFormattedQueries:
    """Test queries with FORMAT clause."""

    def test_format_title(self, temp_csv: Path):
        """Test FORMAT with title."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT title = 'Custom Title'"

        ast = parse(query_str)
        assert ast.format.title == "Custom Title"

        data_list = execute(ast)
        data = data_list[0]
        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_labels(self, temp_csv: Path):
        """Test FORMAT with axis labels."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT xlabel = 'X Label' AND ylabel = 'Y Label'"

        ast = parse(query_str)
        assert ast.format.xlabel == "X Label"
        assert ast.format.ylabel == "Y Label"

        data_list = execute(ast)
        data = data_list[0]
        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_marker_color(self, temp_csv: Path):
        """Test FORMAT with marker_color."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT marker_color = blue"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.marker_colors is not None
        assert all(c == "blue" for c in data.marker_colors)

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_marker_size(self, temp_csv: Path):
        """Test FORMAT with marker_size."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT marker_size = 4"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.marker_sizes is not None
        assert all(s == 4.0 for s in data.marker_sizes)

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_dynamic_marker_color(self, temp_csv: Path):
        """Test FORMAT with column reference for marker_color."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT marker_color = category"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.marker_colors is not None
        assert data.color_info is not None
        assert data.color_info.is_continuous is False

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_dynamic_marker_size(self, temp_csv: Path):
        """Test FORMAT with column reference for marker_size."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x FORMAT marker_size = value"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.marker_sizes is not None
        assert data.size_info is not None

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_format_line_color(self, temp_csv: Path):
        """Test FORMAT with line_color for line plot."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x AS 'line' FORMAT line_color = red"

        ast = parse(query_str)
        assert ast.format.line_color == "red"

        data_list = execute(ast)
        data = data_list[0]
        result = render(data)
        assert result.to_bytes()
        result.close()


class TestComplexQueries:
    """Test complex queries combining multiple features."""

    def test_filter_and_aggregation(self, temp_csv_categorical: Path):
        """Test FILTER + aggregation."""
        query_str = (
            f"WITH '{temp_csv_categorical}' "
            "PLOT sum(amount) AGAINST group AS 'bar' "
            "FILTER amount > 20"
        )

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        # Filtered out amount <= 20 (10, 20), leaving 30,40,50,60
        # Groups B and C remain
        assert data.filtered_count == 2

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_filter_aggregation_and_format(self, temp_csv_categorical: Path):
        """Test FILTER + aggregation + FORMAT."""
        query_str = (
            f"WITH '{temp_csv_categorical}' "
            "PLOT sum(amount) AGAINST group AS 'bar' "
            "FILTER amount > 10 "
            "FORMAT title = 'Sales Report' AND color = green"
        )

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        result = render(data)

        assert result.to_bytes()
        result.close()

    def test_all_clauses(self, temp_csv: Path):
        """Test query with all clauses."""
        query_str = (
            f"WITH '{temp_csv}' "
            "PLOT y AGAINST x AS 'line' "
            "FILTER x > 1 AND x < 5 "
            "FORMAT title = 'Filtered Line' AND xlabel = 'Position' AND ylabel = 'Value' AND line_color = blue"
        )

        ast = parse(query_str)
        assert ast.plot_type.value == "line"
        assert ast.filter is not None
        assert ast.format.title == "Filtered Line"

        data_list = execute(ast)
        data = data_list[0]
        assert data.filtered_count == 3

        result = render(data)
        assert result.to_bytes()
        result.close()


class TestFileFormats:
    """Test different file format support."""

    def test_csv_file(self, temp_csv: Path):
        """Test CSV file loading."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert len(data.x) > 0

    def test_parquet_file(self, temp_parquet: Path):
        """Test Parquet file loading."""
        query_str = f"WITH '{temp_parquet}' PLOT y AGAINST x"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert len(data.x) == 3

    def test_json_file(self, temp_json: Path):
        """Test JSON file loading."""
        query_str = f"WITH '{temp_json}' PLOT y AGAINST x"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert len(data.x) == 3

    def test_ndjson_file(self, temp_ndjson: Path):
        """Test NDJSON file loading."""
        query_str = f"WITH '{temp_ndjson}' PLOT y AGAINST x"
        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        assert len(data.x) == 3


class TestTimestampHandling:
    """Test timestamp detection and handling."""

    def test_timestamp_detection(self, temp_csv_with_timestamps: Path):
        """Test that timestamps are detected."""
        query_str = f"WITH '{temp_csv_with_timestamps}' PLOT value AGAINST timestamp"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.x_timestamp is not None
        assert data.x_timestamp.column_name == "timestamp"

        result = render(data)
        assert result.to_bytes()
        result.close()


class TestRealDataFile:
    """Test with actual trades.csv file if available."""

    def test_trades_csv_scatter(self, trades_csv: Path):
        """Test scatter plot with trades.csv."""
        if not trades_csv.exists():
            pytest.skip("trades.csv not found")

        query_str = f"WITH '{trades_csv}' PLOT price AGAINST received_at"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.row_count > 0
        assert data.x_timestamp is not None

        result = render(data)
        png_bytes = result.to_bytes()
        assert len(png_bytes) > 1000  # Should be a reasonable size
        result.close()

    def test_trades_csv_with_filter(self, trades_csv: Path):
        """Test filtered query with trades.csv."""
        if not trades_csv.exists():
            pytest.skip("trades.csv not found")

        query_str = f"WITH '{trades_csv}' PLOT price AGAINST received_at FILTER price > 10"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert all(p > 10 for p in data.y)

        result = render(data)
        assert result.to_bytes()
        result.close()

    def test_trades_csv_with_format(self, trades_csv: Path):
        """Test formatted query with trades.csv."""
        if not trades_csv.exists():
            pytest.skip("trades.csv not found")

        query_str = (
            f"WITH '{trades_csv}' "
            "PLOT price AGAINST received_at "
            "FORMAT title = 'Price Over Time' AND marker_color = tx_sol_amount"
        )

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        assert data.marker_colors is not None
        assert data.color_info is not None
        assert data.color_info.is_continuous is True

        result = render(data)
        assert result.to_bytes()
        result.close()


class TestErrorHandling:
    """Test error handling throughout the pipeline."""

    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        query_str = "WITH '/nonexistent/file.csv' PLOT y AGAINST x"

        ast = parse(query_str)

        from plotql.core.executor import ExecutionError
        with pytest.raises(ExecutionError) as exc_info:
            execute(ast)
        assert "File not found" in str(exc_info.value)

    def test_column_not_found(self, temp_csv: Path):
        """Test error when column doesn't exist."""
        query_str = f"WITH '{temp_csv}' PLOT nonexistent AGAINST x"

        ast = parse(query_str)

        from plotql.core.executor import ExecutionError
        with pytest.raises(ExecutionError) as exc_info:
            execute(ast)
        assert "Column 'nonexistent' not found" in str(exc_info.value)

    def test_invalid_marker_size_for_non_scatter(self, temp_csv: Path):
        """Test error when marker_size used with non-scatter plot."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x AS 'line' FORMAT marker_size = 3"

        ast = parse(query_str)

        from plotql.core.executor import ExecutionError
        with pytest.raises(ExecutionError) as exc_info:
            execute(ast)
        assert "marker_size is only valid for scatter" in str(exc_info.value)

    def test_parse_error_invalid_syntax(self):
        """Test parse error on invalid syntax."""
        query_str = "INVALID QUERY"

        from plotql.core.parser import ParseError
        with pytest.raises(ParseError):
            parse(query_str)


# =============================================================================
# Output Quality Tests
# =============================================================================

class TestOutputQuality:
    """Test quality of rendered output."""

    def test_image_dimensions(self, temp_csv: Path):
        """Test that output has correct dimensions."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]

        engine = get_engine()
        result = engine.render(data, 800, 600)

        img = result.to_image()
        assert img.size == (800, 600)
        result.close()

    def test_image_is_non_empty(self, temp_csv: Path):
        """Test that output image has content."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        result = render(data)

        img = result.to_image()
        # Check that not all pixels are the same (image has content)
        pixels = list(img.getdata())
        unique_pixels = set(pixels)
        assert len(unique_pixels) > 1

        result.close()

    def test_svg_output(self, temp_csv: Path):
        """Test SVG output format."""
        query_str = f"WITH '{temp_csv}' PLOT y AGAINST x"

        ast = parse(query_str)
        data_list = execute(ast)
        data = data_list[0]
        result = render(data)

        svg_bytes = result.to_bytes(format="svg")
        assert b"<svg" in svg_bytes
        assert b"</svg>" in svg_bytes

        result.close()
