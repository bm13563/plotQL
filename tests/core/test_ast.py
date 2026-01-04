"""
Unit tests for plotql.core.ast module.

Tests all AST node types, enums, and their behaviors.
"""
import pytest

from tests.conftest import make_plot_query
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


# =============================================================================
# PlotType Enum Tests
# =============================================================================

class TestPlotType:
    """Tests for PlotType enum."""

    def test_plot_type_values(self):
        """Test that all plot types have correct string values."""
        assert PlotType.SCATTER.value == "scatter"
        assert PlotType.LINE.value == "line"
        assert PlotType.BAR.value == "bar"
        assert PlotType.HIST.value == "hist"

    def test_plot_type_from_value(self):
        """Test creating PlotType from string value."""
        assert PlotType("scatter") == PlotType.SCATTER
        assert PlotType("line") == PlotType.LINE
        assert PlotType("bar") == PlotType.BAR
        assert PlotType("hist") == PlotType.HIST

    def test_plot_type_invalid_value(self):
        """Test that invalid plot type raises ValueError."""
        with pytest.raises(ValueError):
            PlotType("invalid")

    def test_plot_type_iteration(self):
        """Test that we can iterate over all plot types."""
        types = list(PlotType)
        assert len(types) == 4
        assert PlotType.SCATTER in types
        assert PlotType.LINE in types
        assert PlotType.BAR in types
        assert PlotType.HIST in types


# =============================================================================
# AggregateFunc Enum Tests
# =============================================================================

class TestAggregateFunc:
    """Tests for AggregateFunc enum."""

    def test_aggregate_func_values(self):
        """Test that all aggregate functions have correct string values."""
        assert AggregateFunc.COUNT.value == "count"
        assert AggregateFunc.SUM.value == "sum"
        assert AggregateFunc.AVG.value == "avg"
        assert AggregateFunc.MIN.value == "min"
        assert AggregateFunc.MAX.value == "max"
        assert AggregateFunc.MEDIAN.value == "median"

    def test_aggregate_func_from_value(self):
        """Test creating AggregateFunc from string value."""
        assert AggregateFunc("count") == AggregateFunc.COUNT
        assert AggregateFunc("sum") == AggregateFunc.SUM
        assert AggregateFunc("avg") == AggregateFunc.AVG
        assert AggregateFunc("min") == AggregateFunc.MIN
        assert AggregateFunc("max") == AggregateFunc.MAX
        assert AggregateFunc("median") == AggregateFunc.MEDIAN

    def test_aggregate_func_invalid_value(self):
        """Test that invalid aggregate function raises ValueError."""
        with pytest.raises(ValueError):
            AggregateFunc("mean")  # Not a valid func (avg is used instead)

    def test_aggregate_func_count(self):
        """Test that we have exactly 6 aggregate functions."""
        funcs = list(AggregateFunc)
        assert len(funcs) == 6


# =============================================================================
# ComparisonOp Enum Tests
# =============================================================================

class TestComparisonOp:
    """Tests for ComparisonOp enum."""

    def test_comparison_op_values(self):
        """Test that all comparison operators have correct string values."""
        assert ComparisonOp.EQ.value == "="
        assert ComparisonOp.NE.value == "!="
        assert ComparisonOp.LT.value == "<"
        assert ComparisonOp.LE.value == "<="
        assert ComparisonOp.GT.value == ">"
        assert ComparisonOp.GE.value == ">="

    def test_comparison_op_from_value(self):
        """Test creating ComparisonOp from string value."""
        assert ComparisonOp("=") == ComparisonOp.EQ
        assert ComparisonOp("!=") == ComparisonOp.NE
        assert ComparisonOp("<") == ComparisonOp.LT
        assert ComparisonOp("<=") == ComparisonOp.LE
        assert ComparisonOp(">") == ComparisonOp.GT
        assert ComparisonOp(">=") == ComparisonOp.GE

    def test_comparison_op_invalid_value(self):
        """Test that invalid comparison operator raises ValueError."""
        with pytest.raises(ValueError):
            ComparisonOp("==")  # Python style, not valid here

    def test_comparison_op_count(self):
        """Test that we have exactly 6 comparison operators."""
        ops = list(ComparisonOp)
        assert len(ops) == 6


# =============================================================================
# LogicalOp Enum Tests
# =============================================================================

class TestLogicalOp:
    """Tests for LogicalOp enum."""

    def test_logical_op_values(self):
        """Test that all logical operators have correct string values."""
        assert LogicalOp.AND.value == "AND"
        assert LogicalOp.OR.value == "OR"

    def test_logical_op_from_value(self):
        """Test creating LogicalOp from string value."""
        assert LogicalOp("AND") == LogicalOp.AND
        assert LogicalOp("OR") == LogicalOp.OR

    def test_logical_op_invalid_value(self):
        """Test that invalid logical operator raises ValueError."""
        with pytest.raises(ValueError):
            LogicalOp("NOT")

    def test_logical_op_count(self):
        """Test that we have exactly 2 logical operators."""
        ops = list(LogicalOp)
        assert len(ops) == 2


# =============================================================================
# ColumnRef Tests
# =============================================================================

class TestColumnRef:
    """Tests for ColumnRef dataclass."""

    def test_simple_column_ref(self):
        """Test creating a simple column reference."""
        col = ColumnRef(name="price")
        assert col.name == "price"
        assert col.aggregate is None

    def test_column_ref_with_aggregate(self):
        """Test creating a column reference with aggregation."""
        col = ColumnRef(name="price", aggregate=AggregateFunc.COUNT)
        assert col.name == "price"
        assert col.aggregate == AggregateFunc.COUNT

    def test_is_aggregate_property_false(self):
        """Test is_aggregate returns False for simple column."""
        col = ColumnRef(name="price")
        assert col.is_aggregate is False

    def test_is_aggregate_property_true(self):
        """Test is_aggregate returns True for aggregated column."""
        col = ColumnRef(name="price", aggregate=AggregateFunc.SUM)
        assert col.is_aggregate is True

    def test_str_simple_column(self):
        """Test string representation of simple column."""
        col = ColumnRef(name="price")
        assert str(col) == "price"

    def test_str_aggregate_column(self):
        """Test string representation of aggregated column."""
        col = ColumnRef(name="price", aggregate=AggregateFunc.COUNT)
        assert str(col) == "count(price)"

    @pytest.mark.parametrize("agg_func,expected", [
        (AggregateFunc.COUNT, "count(value)"),
        (AggregateFunc.SUM, "sum(value)"),
        (AggregateFunc.AVG, "avg(value)"),
        (AggregateFunc.MIN, "min(value)"),
        (AggregateFunc.MAX, "max(value)"),
        (AggregateFunc.MEDIAN, "median(value)"),
    ])
    def test_str_all_aggregates(self, agg_func, expected):
        """Test string representation for all aggregate functions."""
        col = ColumnRef(name="value", aggregate=agg_func)
        assert str(col) == expected

    def test_column_ref_equality(self):
        """Test column reference equality."""
        col1 = ColumnRef(name="price", aggregate=AggregateFunc.SUM)
        col2 = ColumnRef(name="price", aggregate=AggregateFunc.SUM)
        assert col1 == col2

    def test_column_ref_inequality(self):
        """Test column reference inequality."""
        col1 = ColumnRef(name="price", aggregate=AggregateFunc.SUM)
        col2 = ColumnRef(name="price", aggregate=AggregateFunc.AVG)
        assert col1 != col2


# =============================================================================
# Condition Tests
# =============================================================================

class TestCondition:
    """Tests for Condition dataclass."""

    def test_condition_creation(self):
        """Test creating a condition."""
        cond = Condition(column="value", op=ComparisonOp.GT, value=100)
        assert cond.column == "value"
        assert cond.op == ComparisonOp.GT
        assert cond.value == 100

    def test_condition_with_string_value(self):
        """Test condition with string value."""
        cond = Condition(column="status", op=ComparisonOp.EQ, value="active")
        assert cond.value == "active"

    def test_condition_with_float_value(self):
        """Test condition with float value."""
        cond = Condition(column="price", op=ComparisonOp.LE, value=99.99)
        assert cond.value == 99.99

    def test_condition_with_negative_value(self):
        """Test condition with negative value."""
        cond = Condition(column="delta", op=ComparisonOp.LT, value=-10)
        assert cond.value == -10

    def test_condition_equality(self):
        """Test condition equality."""
        cond1 = Condition(column="x", op=ComparisonOp.EQ, value=5)
        cond2 = Condition(column="x", op=ComparisonOp.EQ, value=5)
        assert cond1 == cond2


# =============================================================================
# WhereClause Tests
# =============================================================================

class TestWhereClause:
    """Tests for WhereClause dataclass."""

    def test_single_condition(self):
        """Test WHERE clause with single condition."""
        cond = Condition(column="x", op=ComparisonOp.GT, value=0)
        where = WhereClause(conditions=[cond])
        assert len(where.conditions) == 1
        assert len(where.operators) == 0

    def test_multiple_conditions_and(self):
        """Test WHERE clause with AND operator."""
        cond1 = Condition(column="x", op=ComparisonOp.GT, value=0)
        cond2 = Condition(column="y", op=ComparisonOp.LT, value=100)
        where = WhereClause(
            conditions=[cond1, cond2],
            operators=[LogicalOp.AND],
        )
        assert len(where.conditions) == 2
        assert len(where.operators) == 1
        assert where.operators[0] == LogicalOp.AND

    def test_multiple_conditions_or(self):
        """Test WHERE clause with OR operator."""
        cond1 = Condition(column="status", op=ComparisonOp.EQ, value="active")
        cond2 = Condition(column="status", op=ComparisonOp.EQ, value="pending")
        where = WhereClause(
            conditions=[cond1, cond2],
            operators=[LogicalOp.OR],
        )
        assert where.operators[0] == LogicalOp.OR

    def test_three_conditions_mixed(self):
        """Test WHERE clause with three conditions and mixed operators."""
        cond1 = Condition(column="a", op=ComparisonOp.EQ, value=1)
        cond2 = Condition(column="b", op=ComparisonOp.EQ, value=2)
        cond3 = Condition(column="c", op=ComparisonOp.EQ, value=3)
        where = WhereClause(
            conditions=[cond1, cond2, cond3],
            operators=[LogicalOp.AND, LogicalOp.OR],
        )
        assert len(where.conditions) == 3
        assert len(where.operators) == 2

    def test_default_operators_empty(self):
        """Test that operators default to empty list."""
        cond = Condition(column="x", op=ComparisonOp.GT, value=0)
        where = WhereClause(conditions=[cond])
        assert where.operators == []


# =============================================================================
# FormatOptions Tests
# =============================================================================

class TestFormatOptions:
    """Tests for FormatOptions dataclass."""

    def test_default_format_options(self):
        """Test default FormatOptions values."""
        fmt = FormatOptions()
        assert fmt.marker_size is None
        assert fmt.marker_color is None
        assert fmt.marker == "default"
        assert fmt.line_color is None
        assert fmt.line_style is None
        assert fmt.title is None
        assert fmt.xlabel is None
        assert fmt.ylabel is None

    def test_format_options_with_title(self):
        """Test FormatOptions with title."""
        fmt = FormatOptions(title="My Plot")
        assert fmt.title == "My Plot"

    def test_format_options_with_labels(self):
        """Test FormatOptions with axis labels."""
        fmt = FormatOptions(xlabel="X Axis", ylabel="Y Axis")
        assert fmt.xlabel == "X Axis"
        assert fmt.ylabel == "Y Axis"

    def test_format_options_scatter(self):
        """Test FormatOptions for scatter plot."""
        fmt = FormatOptions(
            marker_size="3",
            marker_color="blue",
        )
        assert fmt.marker_size == "3"
        assert fmt.marker_color == "blue"

    def test_format_options_line(self):
        """Test FormatOptions for line plot."""
        fmt = FormatOptions(
            line_color="red",
            line_style="dashed",
        )
        assert fmt.line_color == "red"
        assert fmt.line_style == "dashed"

    def test_format_options_marker_null(self):
        """Test FormatOptions with marker disabled."""
        fmt = FormatOptions(marker=None)
        assert fmt.marker is None

    def test_format_options_equality(self):
        """Test FormatOptions equality."""
        fmt1 = FormatOptions(title="Test", xlabel="X")
        fmt2 = FormatOptions(title="Test", xlabel="X")
        assert fmt1 == fmt2


# =============================================================================
# PlotQuery Tests
# =============================================================================

class TestPlotQuery:
    """Tests for PlotQuery dataclass."""

    def test_minimal_plot_query(self):
        """Test creating a minimal PlotQuery."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
        )
        assert query.source.args[0] == "data.csv"
        assert query.series[0].x_column.name == "x"
        assert query.series[0].y_column.name == "y"
        assert query.series[0].plot_type == PlotType.SCATTER  # Default
        assert query.series[0].filter is None
        assert query.series[0].format is not None

    def test_plot_query_with_plot_type(self):
        """Test PlotQuery with specific plot type."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
        )
        assert query.series[0].plot_type == PlotType.LINE

    def test_plot_query_with_filter(self):
        """Test PlotQuery with filter clause."""
        where = WhereClause(
            conditions=[Condition(column="x", op=ComparisonOp.GT, value=0)],
        )
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            filter=where,
        )
        assert query.series[0].filter is not None
        assert len(query.series[0].filter.conditions) == 1

    def test_plot_query_with_format(self):
        """Test PlotQuery with format options."""
        fmt = FormatOptions(title="My Plot")
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            format=fmt,
        )
        assert query.series[0].format.title == "My Plot"

    def test_is_aggregate_false_both_simple(self):
        """Test is_aggregate when both columns are simple."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
        )
        assert query.is_aggregate is False

    def test_is_aggregate_true_y_aggregate(self):
        """Test is_aggregate when y column has aggregation."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="category"),
            y_column=ColumnRef(name="value", aggregate=AggregateFunc.SUM),
        )
        assert query.is_aggregate is True

    def test_is_aggregate_true_x_aggregate(self):
        """Test is_aggregate when x column has aggregation."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="value", aggregate=AggregateFunc.AVG),
            y_column=ColumnRef(name="y"),
        )
        assert query.is_aggregate is True

    def test_repr_simple(self):
        """Test __repr__ for simple query."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        repr_str = repr(query)
        assert "WITH source('data.csv')" in repr_str
        assert "PLOT y AGAINST x AS 'scatter'" in repr_str

    def test_repr_with_aggregation(self):
        """Test __repr__ with aggregation."""
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="category"),
            y_column=ColumnRef(name="price", aggregate=AggregateFunc.COUNT),
            plot_type=PlotType.BAR,
        )
        repr_str = repr(query)
        assert "count(price)" in repr_str
        assert "AS 'bar'" in repr_str

    def test_repr_with_filter(self):
        """Test __repr__ with filter clause."""
        where = WhereClause(
            conditions=[
                Condition(column="x", op=ComparisonOp.GT, value=10),
                Condition(column="y", op=ComparisonOp.LT, value=100),
            ],
            operators=[LogicalOp.AND],
        )
        query = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            filter=where,
        )
        repr_str = repr(query)
        assert "FILTER" in repr_str
        assert "x > 10" in repr_str
        assert "AND" in repr_str
        assert "y < 100" in repr_str

    def test_plot_query_equality(self):
        """Test PlotQuery equality."""
        query1 = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
        )
        query2 = make_plot_query(
            source="data.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
        )
        assert query1 == query2


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_column_name(self):
        """Test ColumnRef with empty name (should be allowed by dataclass)."""
        col = ColumnRef(name="")
        assert col.name == ""
        assert str(col) == ""

    def test_column_name_with_underscore(self):
        """Test ColumnRef with underscore in name."""
        col = ColumnRef(name="my_column_name")
        assert str(col) == "my_column_name"

    def test_column_name_with_numbers(self):
        """Test ColumnRef with numbers in name."""
        col = ColumnRef(name="col123")
        assert str(col) == "col123"

    def test_condition_with_zero(self):
        """Test condition with zero value."""
        cond = Condition(column="x", op=ComparisonOp.EQ, value=0)
        assert cond.value == 0

    def test_condition_with_empty_string(self):
        """Test condition with empty string value."""
        cond = Condition(column="name", op=ComparisonOp.EQ, value="")
        assert cond.value == ""

    def test_where_clause_empty_conditions(self):
        """Test WhereClause with empty conditions list."""
        where = WhereClause(conditions=[])
        assert len(where.conditions) == 0

    def test_format_options_column_reference_as_color(self):
        """Test FormatOptions with column name as marker_color."""
        fmt = FormatOptions(marker_color="category_column")
        assert fmt.marker_color == "category_column"

    def test_plot_query_source_with_path(self):
        """Test PlotQuery with full file path."""
        query = make_plot_query(
            source="/path/to/data/file.csv",
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
        )
        assert query.source.args[0] == "/path/to/data/file.csv"
