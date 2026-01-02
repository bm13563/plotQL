"""
Unit tests for plotql.core.executor module.

Tests data loading, filtering, aggregation, and query execution.
"""
from pathlib import Path

import polars as pl
import pytest

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    ComparisonOp,
    Condition,
    FormatOptions,
    LogicalOp,
    PlotQuery,
    PlotSeries,
    PlotType,
    WhereClause,
)
from plotql.core.executor import (
    ColorInfo,
    ExecutionError,
    PlotData,
    SizeInfo,
    apply_aggregation,
    apply_where,
    execute,
    load_file,
    validate_series_format_options,
)
from tests.conftest import make_plot_query


# =============================================================================
# load_file Tests
# =============================================================================

class TestLoadFile:
    """Tests for load_file function."""

    def test_load_csv(self, temp_csv: Path):
        """Test loading a CSV file."""
        df = load_file(str(temp_csv))
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 5
        assert "x" in df.columns
        assert "y" in df.columns

    def test_load_parquet(self, temp_parquet: Path):
        """Test loading a Parquet file."""
        df = load_file(str(temp_parquet))
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3

    def test_load_json(self, temp_json: Path):
        """Test loading a JSON file."""
        df = load_file(str(temp_json))
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3

    def test_load_ndjson(self, temp_ndjson: Path):
        """Test loading an NDJSON file."""
        df = load_file(str(temp_ndjson))
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3

    def test_load_file_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(ExecutionError) as exc_info:
            load_file("/nonexistent/path/file.csv")
        assert "File not found" in str(exc_info.value)

    def test_load_unknown_extension_as_csv(self, temp_dir: Path):
        """Test loading unknown extension as CSV."""
        path = temp_dir / "data.txt"
        df = pl.DataFrame({"x": [1, 2], "y": [3, 4]})
        df.write_csv(path)

        result = load_file(str(path))
        assert len(result) == 2


# =============================================================================
# apply_where Tests
# =============================================================================

class TestApplyWhere:
    """Tests for apply_where function."""

    @pytest.fixture
    def sample_df(self) -> pl.DataFrame:
        """Create a sample DataFrame for testing."""
        return pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 30, 40, 50],
            "category": ["A", "B", "A", "B", "A"],
        })

    def test_empty_conditions(self, sample_df: pl.DataFrame):
        """Test with empty conditions returns original DataFrame."""
        where = WhereClause(conditions=[])
        result = apply_where(sample_df, where)
        assert len(result) == len(sample_df)

    def test_equals_numeric(self, sample_df: pl.DataFrame):
        """Test equals condition with numeric value."""
        where = WhereClause(conditions=[
            Condition(column="x", op=ComparisonOp.EQ, value=3)
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 1
        assert result["x"].to_list() == [3]

    def test_equals_string(self, sample_df: pl.DataFrame):
        """Test equals condition with string value."""
        where = WhereClause(conditions=[
            Condition(column="category", op=ComparisonOp.EQ, value="A")
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 3

    def test_not_equals(self, sample_df: pl.DataFrame):
        """Test not equals condition."""
        where = WhereClause(conditions=[
            Condition(column="category", op=ComparisonOp.NE, value="A")
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 2
        assert all(cat == "B" for cat in result["category"].to_list())

    def test_less_than(self, sample_df: pl.DataFrame):
        """Test less than condition."""
        where = WhereClause(conditions=[
            Condition(column="y", op=ComparisonOp.LT, value=30)
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 2
        assert result["y"].to_list() == [10, 20]

    def test_less_than_or_equal(self, sample_df: pl.DataFrame):
        """Test less than or equal condition."""
        where = WhereClause(conditions=[
            Condition(column="y", op=ComparisonOp.LE, value=30)
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 3

    def test_greater_than(self, sample_df: pl.DataFrame):
        """Test greater than condition."""
        where = WhereClause(conditions=[
            Condition(column="x", op=ComparisonOp.GT, value=3)
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 2
        assert result["x"].to_list() == [4, 5]

    def test_greater_than_or_equal(self, sample_df: pl.DataFrame):
        """Test greater than or equal condition."""
        where = WhereClause(conditions=[
            Condition(column="x", op=ComparisonOp.GE, value=3)
        ])
        result = apply_where(sample_df, where)
        assert len(result) == 3

    def test_and_operator(self, sample_df: pl.DataFrame):
        """Test AND operator with two conditions."""
        where = WhereClause(
            conditions=[
                Condition(column="x", op=ComparisonOp.GT, value=2),
                Condition(column="category", op=ComparisonOp.EQ, value="A"),
            ],
            operators=[LogicalOp.AND]
        )
        result = apply_where(sample_df, where)
        assert len(result) == 2  # x=3 and x=5 are category A

    def test_or_operator(self, sample_df: pl.DataFrame):
        """Test OR operator with two conditions."""
        where = WhereClause(
            conditions=[
                Condition(column="x", op=ComparisonOp.EQ, value=1),
                Condition(column="x", op=ComparisonOp.EQ, value=5),
            ],
            operators=[LogicalOp.OR]
        )
        result = apply_where(sample_df, where)
        assert len(result) == 2
        assert set(result["x"].to_list()) == {1, 5}

    def test_three_conditions_mixed_operators(self, sample_df: pl.DataFrame):
        """Test three conditions with mixed AND/OR."""
        # x > 2 AND y < 50 OR category = 'B'
        where = WhereClause(
            conditions=[
                Condition(column="x", op=ComparisonOp.GT, value=2),
                Condition(column="y", op=ComparisonOp.LT, value=50),
                Condition(column="category", op=ComparisonOp.EQ, value="B"),
            ],
            operators=[LogicalOp.AND, LogicalOp.OR]
        )
        result = apply_where(sample_df, where)
        # (x>2 AND y<50) includes x=3,4 with y=30,40
        # OR category='B' includes x=2,4
        # Combined: x=2,3,4
        assert len(result) >= 3


# =============================================================================
# apply_aggregation Tests
# =============================================================================

class TestApplyAggregation:
    """Tests for apply_aggregation function."""

    @pytest.fixture
    def categorical_df(self) -> pl.DataFrame:
        """Create a DataFrame for aggregation testing."""
        return pl.DataFrame({
            "group": ["A", "A", "B", "B", "C"],
            "value": [10, 20, 30, 40, 50],
            "count": [1, 2, 3, 4, 5],
        })

    def test_no_aggregation(self, categorical_df: pl.DataFrame):
        """Test when no aggregation is needed."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value")
        result = apply_aggregation(categorical_df, x_col, y_col)
        assert len(result) == len(categorical_df)

    def test_count_aggregation(self, categorical_df: pl.DataFrame):
        """Test COUNT aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.COUNT)
        result = apply_aggregation(categorical_df, x_col, y_col)

        assert len(result) == 3  # A, B, C
        # Check that counts are correct
        a_count = result.filter(pl.col("group") == "A")["value"].to_list()[0]
        assert a_count == 2

    def test_sum_aggregation(self, categorical_df: pl.DataFrame):
        """Test SUM aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.SUM)
        result = apply_aggregation(categorical_df, x_col, y_col)

        a_sum = result.filter(pl.col("group") == "A")["value"].to_list()[0]
        assert a_sum == 30  # 10 + 20

    def test_avg_aggregation(self, categorical_df: pl.DataFrame):
        """Test AVG aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.AVG)
        result = apply_aggregation(categorical_df, x_col, y_col)

        a_avg = result.filter(pl.col("group") == "A")["value"].to_list()[0]
        assert a_avg == 15.0  # (10 + 20) / 2

    def test_min_aggregation(self, categorical_df: pl.DataFrame):
        """Test MIN aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.MIN)
        result = apply_aggregation(categorical_df, x_col, y_col)

        b_min = result.filter(pl.col("group") == "B")["value"].to_list()[0]
        assert b_min == 30

    def test_max_aggregation(self, categorical_df: pl.DataFrame):
        """Test MAX aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.MAX)
        result = apply_aggregation(categorical_df, x_col, y_col)

        b_max = result.filter(pl.col("group") == "B")["value"].to_list()[0]
        assert b_max == 40

    def test_median_aggregation(self, categorical_df: pl.DataFrame):
        """Test MEDIAN aggregation."""
        x_col = ColumnRef(name="group")
        y_col = ColumnRef(name="value", aggregate=AggregateFunc.MEDIAN)
        result = apply_aggregation(categorical_df, x_col, y_col)

        a_median = result.filter(pl.col("group") == "A")["value"].to_list()[0]
        assert a_median == 15.0  # median of 10, 20

    def test_aggregation_on_x_column(self, categorical_df: pl.DataFrame):
        """Test aggregation on x column instead of y."""
        x_col = ColumnRef(name="value", aggregate=AggregateFunc.SUM)
        y_col = ColumnRef(name="group")
        result = apply_aggregation(categorical_df, x_col, y_col)
        assert len(result) == 3

    def test_both_columns_aggregated_error(self, categorical_df: pl.DataFrame):
        """Test error when both columns have aggregation."""
        x_col = ColumnRef(name="value", aggregate=AggregateFunc.SUM)
        y_col = ColumnRef(name="count", aggregate=AggregateFunc.AVG)
        with pytest.raises(ExecutionError) as exc_info:
            apply_aggregation(categorical_df, x_col, y_col)
        assert "Cannot aggregate both" in str(exc_info.value)


# =============================================================================
# validate_format_options Tests
# =============================================================================

class TestValidateFormatOptions:
    """Tests for validate_format_options function."""

    def test_scatter_with_marker_color_valid(self, temp_csv: Path):
        """Test marker_color is valid for scatter plot."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="blue"),
        )
        # Should not raise
        validate_series_format_options(query.series[0])

    def test_line_with_marker_color_invalid(self, temp_csv: Path):
        """Test marker_color is invalid for line plot."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
            format=FormatOptions(marker_color="blue"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            validate_series_format_options(query.series[0])
        assert "marker_color is only valid for scatter" in str(exc_info.value)

    def test_scatter_with_marker_size_valid(self, temp_csv: Path):
        """Test marker_size is valid for scatter plot."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="3"),
        )
        validate_series_format_options(query.series[0])

    def test_bar_with_marker_size_invalid(self, temp_csv: Path):
        """Test marker_size is invalid for bar plot."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.BAR,
            format=FormatOptions(marker_size="3"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            validate_series_format_options(query.series[0])
        assert "marker_size is only valid for scatter" in str(exc_info.value)

    def test_hist_with_marker_color_invalid(self, temp_csv: Path):
        """Test marker_color is invalid for histogram."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.HIST,
            format=FormatOptions(marker_color="red"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            validate_series_format_options(query.series[0])
        assert "marker_color is only valid for scatter" in str(exc_info.value)


# =============================================================================
# execute Function Tests
# =============================================================================

class TestExecute:
    """Tests for execute function."""

    def test_execute_simple_query(self, temp_csv: Path):
        """Test executing a simple query."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        results = execute(query)
        result = results[0]

        assert isinstance(result, PlotData)
        assert result.x == [1, 2, 3, 4, 5]
        assert result.y == [10, 20, 30, 40, 50]
        assert result.row_count == 5
        assert result.filtered_count == 5

    def test_execute_with_filter(self, temp_csv: Path):
        """Test executing with FILTER clause."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            filter=WhereClause(conditions=[
                Condition(column="x", op=ComparisonOp.GT, value=2)
            ]),
        )
        results = execute(query)
        result = results[0]

        assert result.row_count == 5
        assert result.filtered_count == 3
        assert result.x == [3, 4, 5]

    def test_execute_with_aggregation(self, temp_csv_categorical: Path):
        """Test executing with aggregation."""
        query = make_plot_query(
            source=str(temp_csv_categorical),
            x_column=ColumnRef(name="group"),
            y_column=ColumnRef(name="amount", aggregate=AggregateFunc.SUM),
            plot_type=PlotType.BAR,
        )
        results = execute(query)
        result = results[0]

        assert result.filtered_count == 3  # 3 groups
        # Check values (groups may be in any order)
        total_sum = sum(result.y)
        assert total_sum == 210  # 10+20 + 30+40 + 50+60

    def test_execute_with_filter_and_aggregation(self, temp_csv_categorical: Path):
        """Test executing with both FILTER and aggregation."""
        query = make_plot_query(
            source=str(temp_csv_categorical),
            x_column=ColumnRef(name="group"),
            y_column=ColumnRef(name="amount", aggregate=AggregateFunc.SUM),
            plot_type=PlotType.BAR,
            filter=WhereClause(conditions=[
                Condition(column="amount", op=ComparisonOp.GT, value=20)
            ]),
        )
        results = execute(query)
        result = results[0]

        # Filter removes amount=10,20, leaving 30,40,50,60 in groups B and C
        assert result.filtered_count == 2  # B and C

    def test_execute_column_not_found(self, temp_csv: Path):
        """Test error when column doesn't exist."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="nonexistent"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        with pytest.raises(ExecutionError) as exc_info:
            execute(query)
        assert "Column 'nonexistent' not found" in str(exc_info.value)

    def test_execute_filter_column_not_found(self, temp_csv: Path):
        """Test error when FILTER column doesn't exist."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            filter=WhereClause(conditions=[
                Condition(column="nonexistent", op=ComparisonOp.GT, value=0)
            ]),
        )
        with pytest.raises(ExecutionError) as exc_info:
            execute(query)
        assert "FILTER column 'nonexistent' not found" in str(exc_info.value)


# =============================================================================
# execute with Dynamic Formatting Tests
# =============================================================================

class TestExecuteWithDynamicFormatting:
    """Tests for execute with marker_size and marker_color."""

    def test_marker_size_column_reference(self, temp_csv: Path):
        """Test marker_size with column reference."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="value"),
        )
        results = execute(query)
        result = results[0]

        assert result.marker_sizes is not None
        assert len(result.marker_sizes) == 5
        # Sizes should be mapped to 1-5 range
        assert all(1.0 <= s <= 5.0 for s in result.marker_sizes)
        assert result.size_info is not None

    def test_marker_size_literal_value(self, temp_csv: Path):
        """Test marker_size with literal numeric value."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="3"),
        )
        results = execute(query)
        result = results[0]

        assert result.marker_sizes is not None
        assert all(s == 3.0 for s in result.marker_sizes)

    def test_marker_size_out_of_range_error(self, temp_csv: Path):
        """Test error when marker_size literal is out of range."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="10"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            execute(query)
        assert "marker_size must be between 1 and 5" in str(exc_info.value)

    def test_marker_size_invalid_value_error(self, temp_csv: Path):
        """Test error when marker_size is neither column nor valid number."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="invalid"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            execute(query)
        assert "not a valid column name or number" in str(exc_info.value)

    def test_marker_color_column_reference(self, temp_csv: Path):
        """Test marker_color with column reference."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="category"),
        )
        results = execute(query)
        result = results[0]

        assert result.marker_colors is not None
        assert len(result.marker_colors) == 5
        assert result.color_info is not None
        assert result.color_info.column_name == "category"

    def test_marker_color_literal_value(self, temp_csv: Path):
        """Test marker_color with literal color name."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="blue"),
        )
        results = execute(query)
        result = results[0]

        assert result.marker_colors is not None
        assert all(c == "blue" for c in result.marker_colors)

    def test_marker_color_invalid_value_error(self, temp_csv: Path):
        """Test error when marker_color is neither column nor valid color."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="notacolor"),
        )
        with pytest.raises(ExecutionError) as exc_info:
            execute(query)
        assert "not a valid column name or color" in str(exc_info.value)

    def test_continuous_color_info(self, temp_csv: Path):
        """Test ColorInfo for continuous numeric column."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="value"),
        )
        results = execute(query)
        result = results[0]

        assert result.color_info is not None
        assert result.color_info.is_continuous is True
        assert result.color_info.min_value is not None
        assert result.color_info.max_value is not None

    def test_categorical_color_info(self, temp_csv: Path):
        """Test ColorInfo for categorical column."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="category"),
        )
        results = execute(query)
        result = results[0]

        assert result.color_info is not None
        assert result.color_info.is_continuous is False
        assert result.color_info.category_colors is not None


# =============================================================================
# execute with Timestamps Tests
# =============================================================================

class TestExecuteWithTimestamps:
    """Tests for execute with timestamp columns."""

    def test_timestamp_detection(self, temp_csv_with_timestamps: Path):
        """Test that timestamps are detected."""
        query = make_plot_query(
            source=str(temp_csv_with_timestamps),
            x_column=ColumnRef(name="timestamp"),
            y_column=ColumnRef(name="value"),
            plot_type=PlotType.LINE,
        )
        results = execute(query)
        result = results[0]

        assert result.x_timestamp is not None
        assert result.x_timestamp.column_name == "timestamp"

    def test_no_timestamp_for_numeric(self, temp_csv: Path):
        """Test that numeric columns don't get timestamp info."""
        query = make_plot_query(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        results = execute(query)
        result = results[0]

        assert result.x_timestamp is None
        assert result.y_timestamp is None


# =============================================================================
# PlotData Dataclass Tests
# =============================================================================

class TestPlotData:
    """Tests for PlotData dataclass."""

    def test_plot_data_creation(self, simple_plot_query: PlotQuery):
        """Test creating PlotData."""
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            series=simple_plot_query.series[0],
            row_count=3,
            filtered_count=3,
        )
        assert len(data.x) == 3
        assert len(data.y) == 3
        assert data.marker_sizes is None
        assert data.marker_colors is None

    def test_plot_data_with_optional_fields(self, simple_plot_query: PlotQuery):
        """Test PlotData with all optional fields."""
        data = PlotData(
            x=[1.0, 2.0],
            y=[3.0, 4.0],
            series=simple_plot_query.series[0],
            row_count=2,
            filtered_count=2,
            marker_sizes=[1.0, 2.0],
            marker_colors=["blue", "red"],
            size_info=SizeInfo(is_continuous=True, column_name="s", min_value=1.0, max_value=2.0),
            color_info=ColorInfo(is_continuous=False, column_name="c", category_colors={"A": "blue"}),
        )
        assert data.marker_sizes is not None
        assert data.marker_colors is not None
        assert data.size_info is not None
        assert data.color_info is not None


# =============================================================================
# SizeInfo and ColorInfo Tests
# =============================================================================

class TestSizeInfo:
    """Tests for SizeInfo dataclass."""

    def test_continuous_size_info(self):
        """Test continuous SizeInfo."""
        info = SizeInfo(
            is_continuous=True,
            column_name="value",
            min_value=0.0,
            max_value=100.0,
        )
        assert info.is_continuous is True
        assert info.min_value == 0.0
        assert info.max_value == 100.0
        assert info.category_sizes is None

    def test_categorical_size_info(self):
        """Test categorical SizeInfo."""
        info = SizeInfo(
            is_continuous=False,
            column_name="category",
            category_sizes={"A": 1.0, "B": 3.0, "C": 5.0},
        )
        assert info.is_continuous is False
        assert info.category_sizes is not None
        assert len(info.category_sizes) == 3


class TestColorInfo:
    """Tests for ColorInfo dataclass."""

    def test_continuous_color_info(self):
        """Test continuous ColorInfo."""
        info = ColorInfo(
            is_continuous=True,
            column_name="value",
            min_value=0.0,
            max_value=100.0,
        )
        assert info.is_continuous is True

    def test_categorical_color_info(self):
        """Test categorical ColorInfo."""
        info = ColorInfo(
            is_continuous=False,
            column_name="category",
            category_colors={"A": "blue", "B": "green"},
        )
        assert info.is_continuous is False
        assert info.category_colors["A"] == "blue"


# =============================================================================
# Real Data Tests
# =============================================================================

class TestExecuteWithRealData:
    """Tests using the actual trades.csv example file."""

    def test_execute_trades_csv(self, trades_csv: Path):
        """Test executing with real trades.csv file."""
        if not trades_csv.exists():
            pytest.skip("trades.csv not found")

        query = make_plot_query(
            source=str(trades_csv),
            x_column=ColumnRef(name="received_at"),
            y_column=ColumnRef(name="price"),
            plot_type=PlotType.SCATTER,
        )
        results = execute(query)
        result = results[0]

        assert result.row_count > 0
        assert len(result.x) == len(result.y)
        assert result.x_timestamp is not None  # Should detect timestamp

    def test_execute_trades_with_filter(self, trades_csv: Path):
        """Test executing trades.csv with filter."""
        if not trades_csv.exists():
            pytest.skip("trades.csv not found")

        query = make_plot_query(
            source=str(trades_csv),
            x_column=ColumnRef(name="received_at"),
            y_column=ColumnRef(name="price"),
            plot_type=PlotType.SCATTER,
            filter=WhereClause(conditions=[
                Condition(column="price", op=ComparisonOp.GT, value=10)
            ]),
        )
        results = execute(query)
        result = results[0]

        assert result.filtered_count <= result.row_count
        assert all(p > 10 for p in result.y)
