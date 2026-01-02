"""
Shared fixtures for PlotQL test suite.
"""
import os
import tempfile
from pathlib import Path
from typing import List

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
    PlotType,
    WhereClause,
)
from plotql.core.executor import PlotData, SizeInfo, ColorInfo
from plotql.core.parser import Token


# =============================================================================
# Path Fixtures
# =============================================================================

@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def examples_dir() -> Path:
    """Return the path to the examples directory."""
    return Path(__file__).parent.parent / "examples"


@pytest.fixture
def trades_csv(examples_dir: Path) -> Path:
    """Return the path to the trades.csv example file."""
    return examples_dir / "trades.csv"


# =============================================================================
# Temporary File Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_csv(temp_dir: Path) -> Path:
    """Create a temporary CSV file with sample data."""
    path = temp_dir / "test_data.csv"
    df = pl.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 30, 40, 50],
        "category": ["A", "B", "A", "B", "A"],
        "value": [1.5, 2.5, 3.5, 4.5, 5.5],
    })
    df.write_csv(path)
    return path


@pytest.fixture
def temp_csv_with_timestamps(temp_dir: Path) -> Path:
    """Create a temporary CSV with timestamp data."""
    path = temp_dir / "timestamps.csv"
    df = pl.DataFrame({
        "timestamp": [
            "2026-01-01 10:00:00",
            "2026-01-01 10:01:00",
            "2026-01-01 10:02:00",
            "2026-01-01 10:03:00",
        ],
        "value": [100, 200, 150, 250],
    })
    df.write_csv(path)
    return path


@pytest.fixture
def temp_csv_categorical(temp_dir: Path) -> Path:
    """Create a temporary CSV with categorical data for aggregation tests."""
    path = temp_dir / "categorical.csv"
    df = pl.DataFrame({
        "group": ["A", "A", "B", "B", "C", "C"],
        "amount": [10, 20, 30, 40, 50, 60],
        "count": [1, 2, 3, 4, 5, 6],
    })
    df.write_csv(path)
    return path


@pytest.fixture
def temp_parquet(temp_dir: Path) -> Path:
    """Create a temporary Parquet file."""
    path = temp_dir / "test_data.parquet"
    df = pl.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6],
    })
    df.write_parquet(path)
    return path


@pytest.fixture
def temp_json(temp_dir: Path) -> Path:
    """Create a temporary JSON file."""
    path = temp_dir / "test_data.json"
    df = pl.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6],
    })
    df.write_json(path)
    return path


@pytest.fixture
def temp_ndjson(temp_dir: Path) -> Path:
    """Create a temporary NDJSON file."""
    path = temp_dir / "test_data.ndjson"
    df = pl.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6],
    })
    df.write_ndjson(path)
    return path


# =============================================================================
# Token Fixtures
# =============================================================================

@pytest.fixture
def sample_tokens() -> List[Token]:
    """Sample tokens for a simple query."""
    return [
        Token("WITH", "WITH", 0),
        Token("STRING", "'data.csv'", 5),
        Token("PLOT", "PLOT", 16),
        Token("IDENT", "y", 21),
        Token("AGAINST", "AGAINST", 23),
        Token("IDENT", "x", 31),
    ]


@pytest.fixture
def tokens_with_aggregate() -> List[Token]:
    """Tokens for a query with aggregation."""
    return [
        Token("WITH", "WITH", 0),
        Token("STRING", "'data.csv'", 5),
        Token("PLOT", "PLOT", 16),
        Token("AGGFUNC", "count", 21),
        Token("LPAREN", "(", 26),
        Token("IDENT", "price", 27),
        Token("RPAREN", ")", 32),
        Token("AGAINST", "AGAINST", 34),
        Token("IDENT", "symbol", 42),
    ]


@pytest.fixture
def tokens_with_filter() -> List[Token]:
    """Tokens for a query with FILTER clause."""
    return [
        Token("WITH", "WITH", 0),
        Token("STRING", "'data.csv'", 5),
        Token("PLOT", "PLOT", 16),
        Token("IDENT", "y", 21),
        Token("AGAINST", "AGAINST", 23),
        Token("IDENT", "x", 31),
        Token("FILTER", "FILTER", 33),
        Token("IDENT", "value", 40),
        Token("OP", ">", 46),
        Token("NUMBER", "10", 48),
    ]


# =============================================================================
# AST Fixtures
# =============================================================================

@pytest.fixture
def simple_column_ref() -> ColumnRef:
    """A simple column reference without aggregation."""
    return ColumnRef(name="price")


@pytest.fixture
def aggregate_column_ref() -> ColumnRef:
    """A column reference with aggregation."""
    return ColumnRef(name="price", aggregate=AggregateFunc.COUNT)


@pytest.fixture
def simple_condition() -> Condition:
    """A simple filter condition."""
    return Condition(column="value", op=ComparisonOp.GT, value=100)


@pytest.fixture
def simple_where_clause(simple_condition: Condition) -> WhereClause:
    """A WHERE clause with a single condition."""
    return WhereClause(conditions=[simple_condition])


@pytest.fixture
def compound_where_clause() -> WhereClause:
    """A WHERE clause with multiple conditions."""
    return WhereClause(
        conditions=[
            Condition(column="value", op=ComparisonOp.GT, value=10),
            Condition(column="category", op=ComparisonOp.EQ, value="A"),
        ],
        operators=[LogicalOp.AND],
    )


@pytest.fixture
def simple_format_options() -> FormatOptions:
    """Simple format options."""
    return FormatOptions(
        title="Test Plot",
        xlabel="X Axis",
        ylabel="Y Axis",
    )


@pytest.fixture
def scatter_format_options() -> FormatOptions:
    """Format options for scatter plot."""
    return FormatOptions(
        marker_size="3",
        marker_color="blue",
        title="Scatter Plot",
    )


@pytest.fixture
def simple_plot_query(temp_csv: Path) -> PlotQuery:
    """A simple PlotQuery AST."""
    return PlotQuery(
        source=str(temp_csv),
        x_column=ColumnRef(name="x"),
        y_column=ColumnRef(name="y"),
        plot_type=PlotType.SCATTER,
    )


@pytest.fixture
def line_plot_query(temp_csv: Path) -> PlotQuery:
    """A line plot query."""
    return PlotQuery(
        source=str(temp_csv),
        x_column=ColumnRef(name="x"),
        y_column=ColumnRef(name="y"),
        plot_type=PlotType.LINE,
        format=FormatOptions(line_color="blue"),
    )


@pytest.fixture
def bar_plot_query(temp_csv_categorical: Path) -> PlotQuery:
    """A bar plot query with aggregation."""
    return PlotQuery(
        source=str(temp_csv_categorical),
        x_column=ColumnRef(name="group"),
        y_column=ColumnRef(name="amount", aggregate=AggregateFunc.SUM),
        plot_type=PlotType.BAR,
    )


@pytest.fixture
def filtered_plot_query(temp_csv: Path) -> PlotQuery:
    """A query with FILTER clause."""
    return PlotQuery(
        source=str(temp_csv),
        x_column=ColumnRef(name="x"),
        y_column=ColumnRef(name="y"),
        plot_type=PlotType.SCATTER,
        filter=WhereClause(
            conditions=[Condition(column="category", op=ComparisonOp.EQ, value="A")],
        ),
    )


# =============================================================================
# PlotData Fixtures
# =============================================================================

@pytest.fixture
def simple_plot_data(simple_plot_query: PlotQuery) -> PlotData:
    """Simple PlotData for testing."""
    return PlotData(
        x=[1.0, 2.0, 3.0, 4.0, 5.0],
        y=[10.0, 20.0, 30.0, 40.0, 50.0],
        query=simple_plot_query,
        row_count=5,
        filtered_count=5,
    )


@pytest.fixture
def plot_data_with_sizes(simple_plot_query: PlotQuery) -> PlotData:
    """PlotData with marker sizes."""
    return PlotData(
        x=[1.0, 2.0, 3.0, 4.0, 5.0],
        y=[10.0, 20.0, 30.0, 40.0, 50.0],
        query=simple_plot_query,
        row_count=5,
        filtered_count=5,
        marker_sizes=[1.0, 2.0, 3.0, 4.0, 5.0],
        size_info=SizeInfo(
            is_continuous=True,
            column_name="size",
            min_value=1.0,
            max_value=5.0,
        ),
    )


@pytest.fixture
def plot_data_with_colors(simple_plot_query: PlotQuery) -> PlotData:
    """PlotData with marker colors."""
    return PlotData(
        x=[1.0, 2.0, 3.0, 4.0, 5.0],
        y=[10.0, 20.0, 30.0, 40.0, 50.0],
        query=simple_plot_query,
        row_count=5,
        filtered_count=5,
        marker_colors=["blue", "green", "yellow", "pink", "teal"],
        color_info=ColorInfo(
            is_continuous=False,
            column_name="category",
            category_colors={"A": "blue", "B": "green"},
        ),
    )


# =============================================================================
# Query String Fixtures
# =============================================================================

@pytest.fixture
def query_simple() -> str:
    """Simple query string."""
    return "WITH 'data.csv' PLOT y AGAINST x"


@pytest.fixture
def query_with_plot_type() -> str:
    """Query with AS clause."""
    return "WITH 'data.csv' PLOT y AGAINST x AS 'line'"


@pytest.fixture
def query_with_filter() -> str:
    """Query with FILTER clause."""
    return "WITH 'data.csv' PLOT y AGAINST x FILTER value > 10"


@pytest.fixture
def query_with_format() -> str:
    """Query with FORMAT clause."""
    return "WITH 'data.csv' PLOT y AGAINST x FORMAT title = 'My Plot' AND xlabel = 'X'"


@pytest.fixture
def query_with_aggregation() -> str:
    """Query with aggregation function."""
    return "WITH 'data.csv' PLOT count(id) AGAINST category AS 'bar'"


@pytest.fixture
def query_full() -> str:
    """Full query with all clauses."""
    return (
        "WITH 'data.csv' "
        "PLOT sum(amount) AGAINST category AS 'bar' "
        "FILTER status = 'active' AND value > 100 "
        "FORMAT title = 'Sales by Category' AND ylabel = 'Total'"
    )


# =============================================================================
# Invalid Query Fixtures
# =============================================================================

@pytest.fixture
def invalid_query_no_with() -> str:
    """Query missing WITH clause."""
    return "PLOT y AGAINST x"


@pytest.fixture
def invalid_query_no_plot() -> str:
    """Query missing PLOT clause."""
    return "WITH 'data.csv'"


@pytest.fixture
def invalid_query_bad_plot_type() -> str:
    """Query with invalid plot type."""
    return "WITH 'data.csv' PLOT y AGAINST x AS 'invalid'"


@pytest.fixture
def invalid_query_bad_operator() -> str:
    """Query with unknown character."""
    return "WITH 'data.csv' PLOT y AGAINST x FILTER value @ 10"
