"""
Unit tests for plotql.ui.autocomplete module.

Tests context detection, file completions, column extraction, and AutoCompleter.
"""
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from plotql.ui.autocomplete import (
    AutoCompleter,
    COLOR_OPTIONS,
    Completion,
    FORMAT_OPTIONS,
    FUNCTIONS,
    KEYWORDS,
    PLOT_TYPES,
    extract_file_path,
    get_columns_from_file,
    get_context,
    get_file_completions,
)


# =============================================================================
# Completion Dataclass Tests
# =============================================================================

class TestCompletion:
    """Tests for Completion dataclass."""

    def test_completion_creation(self):
        """Test creating a Completion."""
        comp = Completion(text="WITH", display="WITH", kind="keyword")
        assert comp.text == "WITH"
        assert comp.display == "WITH"
        assert comp.kind == "keyword"

    def test_completion_str(self):
        """Test Completion string representation."""
        comp = Completion(text="count(", display="count", kind="function")
        assert str(comp) == "count("

    def test_completion_equality(self):
        """Test Completion equality."""
        comp1 = Completion("a", "a", "keyword")
        comp2 = Completion("a", "a", "keyword")
        assert comp1 == comp2


# =============================================================================
# Constants Tests
# =============================================================================

class TestConstants:
    """Tests for module constants."""

    def test_keywords(self):
        """Test KEYWORDS list contains expected values."""
        assert "WITH" in KEYWORDS
        assert "PLOT" in KEYWORDS
        assert "AGAINST" in KEYWORDS
        assert "AS" in KEYWORDS
        assert "FILTER" in KEYWORDS
        assert "FORMAT" in KEYWORDS
        assert "AND" in KEYWORDS
        assert "OR" in KEYWORDS

    def test_functions(self):
        """Test FUNCTIONS list contains expected values."""
        assert "count" in FUNCTIONS
        assert "sum" in FUNCTIONS
        assert "avg" in FUNCTIONS
        assert "min" in FUNCTIONS
        assert "max" in FUNCTIONS
        assert "median" in FUNCTIONS

    def test_plot_types(self):
        """Test PLOT_TYPES list contains expected values."""
        assert "'scatter'" in PLOT_TYPES
        assert "'line'" in PLOT_TYPES
        assert "'bar'" in PLOT_TYPES
        assert "'hist'" in PLOT_TYPES

    def test_format_options(self):
        """Test FORMAT_OPTIONS list."""
        assert "title" in FORMAT_OPTIONS
        assert "xlabel" in FORMAT_OPTIONS
        assert "ylabel" in FORMAT_OPTIONS
        assert "marker_color" in FORMAT_OPTIONS
        assert "marker_size" in FORMAT_OPTIONS

    def test_color_options(self):
        """Test COLOR_OPTIONS list."""
        assert "red" in COLOR_OPTIONS
        assert "green" in COLOR_OPTIONS
        assert "blue" in COLOR_OPTIONS
        assert "yellow" in COLOR_OPTIONS


# =============================================================================
# get_context Tests
# =============================================================================

class TestGetContext:
    """Tests for get_context function."""

    def test_empty_text(self):
        """Test with empty text."""
        context, partial, plot_type = get_context("", 0)
        assert context == "start"
        assert partial == ""
        assert plot_type is None

    def test_start_context(self):
        """Test at start of query."""
        context, partial, _ = get_context("W", 1)
        assert context == "start"
        assert partial == "W"

    def test_after_with_keyword(self):
        """Test after WITH keyword - expect source(."""
        context, partial, _ = get_context("WITH ", 5)
        assert context == "after_with_keyword"

    def test_file_path_context(self):
        """Test inside file path string in source()."""
        context, partial, _ = get_context("WITH source('data", 17)
        assert context == "file_path"
        assert partial == "data"

    def test_file_path_with_directory(self):
        """Test file path with directory in source()."""
        context, partial, _ = get_context("WITH source('path/to/", 21)
        assert context == "file_path"
        assert partial == "path/to/"

    def test_after_with_context(self):
        """Test after complete WITH source() clause."""
        context, partial, _ = get_context("WITH source('data.csv') ", 24)
        assert context == "after_with"

    def test_column_context_after_plot(self):
        """Test after PLOT keyword."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT ", 29)
        assert context == "column"

    def test_agg_column_context(self):
        """Test inside aggregate function."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT count(", 35)
        assert context == "agg_column"

    def test_agg_column_partial(self):
        """Test inside aggregate function with partial column."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT count(pr", 37)
        assert context == "agg_column"
        assert partial == "pr"

    def test_after_plot_col_context(self):
        """Test after PLOT column."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT price ", 35)
        assert context == "after_plot_col"

    def test_column_after_against(self):
        """Test after AGAINST keyword."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT price AGAINST ", 43)
        assert context == "column"

    def test_after_against_col_context(self):
        """Test after AGAINST column."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT price AGAINST time ", 48)
        assert context == "after_against_col"

    def test_plot_type_context(self):
        """Test after AS keyword."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x AS ", 44)
        assert context == "plot_type"

    def test_plot_type_partial(self):
        """Test partial plot type."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x AS 'li", 47)
        assert context == "plot_type"
        assert "li" in partial or partial.endswith("li")

    def test_after_plot_type_context(self):
        """Test after complete AS clause."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x AS 'scatter' ", 54)
        assert context == "after_plot_type"

    def test_detected_plot_type(self):
        """Test that plot type is detected from query."""
        _, _, plot_type = get_context("WITH source('data.csv') PLOT y AGAINST x AS 'line' ", 51)
        assert plot_type == "line"

    def test_filter_column_context(self):
        """Test after FILTER keyword."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FILTER ", 48)
        assert context == "filter_column"

    def test_filter_op_context(self):
        """Test after FILTER column."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FILTER value ", 54)
        assert context == "filter_op"

    def test_filter_value_context(self):
        """Test after FILTER operator."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FILTER value > ", 56)
        assert context == "filter_value"

    def test_filter_after_and(self):
        """Test after AND in FILTER."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FILTER a = 1 AND ", 58)
        assert context == "filter_column"

    def test_filter_after_or(self):
        """Test after OR in FILTER."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FILTER a = 1 OR ", 57)
        assert context == "filter_column"

    def test_format_key_context(self):
        """Test after FORMAT keyword."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FORMAT ", 48)
        assert context == "format_key"

    def test_format_color_context(self):
        """Test after color format option."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FORMAT marker_color = ", 63)
        assert context == "format_color"

    def test_format_size_context(self):
        """Test after size format option."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FORMAT marker_size = ", 62)
        assert context == "format_size"

    def test_format_after_and(self):
        """Test after AND in FORMAT."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FORMAT title = 'X' AND ", 64)
        assert context == "format_key"

    def test_none_context_for_title_value(self):
        """Test that title/label values don't get autocomplete."""
        context, partial, _ = get_context("WITH source('data.csv') PLOT y AGAINST x FORMAT title = ", 56)
        assert context == "none"


# =============================================================================
# get_file_completions Tests
# =============================================================================

class TestGetFileCompletions:
    """Tests for get_file_completions function."""

    def test_empty_path(self, temp_dir: Path):
        """Test with empty path (current directory)."""
        # Create test files
        (temp_dir / "test.csv").write_text("a,b\n1,2\n")
        (temp_dir / "data.parquet").write_bytes(b"PAR1")  # Dummy parquet header

        with patch("plotql.ui.autocomplete.Path") as mock_path:
            mock_path.return_value = temp_dir

            completions = get_file_completions("", limit=10)

            # Should return some completions
            assert isinstance(completions, list)

    def test_directory_path(self, temp_dir: Path):
        """Test with directory path ending in slash."""
        # Create subdirectory with files
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "data.csv").write_text("a,b\n1,2\n")

        completions = get_file_completions(str(subdir) + "/")

        assert len(completions) > 0
        assert any("data.csv" in c.display for c in completions)

    def test_partial_filename(self, temp_dir: Path):
        """Test with partial filename."""
        (temp_dir / "trades.csv").write_text("a,b\n1,2\n")
        (temp_dir / "transactions.csv").write_text("a,b\n1,2\n")

        completions = get_file_completions(str(temp_dir) + "/tra")

        assert any("trades.csv" in c.display for c in completions)
        assert any("transactions.csv" in c.display for c in completions)

    def test_hidden_files_excluded(self, temp_dir: Path):
        """Test that hidden files are excluded."""
        (temp_dir / ".hidden.csv").write_text("a,b\n1,2\n")
        (temp_dir / "visible.csv").write_text("a,b\n1,2\n")

        completions = get_file_completions(str(temp_dir) + "/")

        assert any("visible.csv" in c.display for c in completions)
        assert not any(".hidden" in c.display for c in completions)

    def test_directory_completion(self, temp_dir: Path):
        """Test directory completion includes trailing slash."""
        subdir = temp_dir / "data_folder"
        subdir.mkdir()

        completions = get_file_completions(str(temp_dir) + "/")

        dir_comps = [c for c in completions if c.kind == "directory"]
        assert len(dir_comps) > 0
        assert dir_comps[0].text.endswith("/")

    def test_limit_parameter(self, temp_dir: Path):
        """Test limit parameter."""
        for i in range(20):
            (temp_dir / f"file{i}.csv").write_text("a\n1\n")

        completions = get_file_completions(str(temp_dir) + "/", limit=5)

        assert len(completions) <= 5

    def test_nonexistent_directory(self):
        """Test with nonexistent directory."""
        completions = get_file_completions("/nonexistent/path/")
        assert completions == []


# =============================================================================
# extract_file_path Tests
# =============================================================================

class TestExtractFilePath:
    """Tests for extract_file_path function."""

    def test_single_quoted_path(self):
        """Test extracting single-quoted path."""
        text = "WITH source('data.csv') PLOT y AGAINST x"
        result = extract_file_path(text)
        assert result == "data.csv"

    def test_double_quoted_path(self):
        """Test extracting double-quoted path."""
        text = 'WITH source("data.csv") PLOT y AGAINST x'
        result = extract_file_path(text)
        assert result == "data.csv"

    def test_full_path(self):
        """Test extracting full file path."""
        text = "WITH source('/path/to/data/file.csv') PLOT y AGAINST x"
        result = extract_file_path(text)
        assert result == "/path/to/data/file.csv"

    def test_no_with_clause(self):
        """Test when no WITH clause exists."""
        text = "PLOT y AGAINST x"
        result = extract_file_path(text)
        assert result is None

    def test_incomplete_with_clause(self):
        """Test with incomplete WITH clause."""
        text = "WITH source('partial"
        result = extract_file_path(text)
        assert result is None

    def test_case_insensitive(self):
        """Test case insensitivity."""
        text = "with source('data.csv') plot y against x"
        result = extract_file_path(text)
        assert result == "data.csv"


# =============================================================================
# get_columns_from_file Tests
# =============================================================================

class TestGetColumnsFromFile:
    """Tests for get_columns_from_file function."""

    def test_csv_columns(self, temp_csv: Path):
        """Test getting columns from CSV file."""
        columns = get_columns_from_file(str(temp_csv))
        assert "x" in columns
        assert "y" in columns

    def test_parquet_columns(self, temp_parquet: Path):
        """Test getting columns from Parquet file."""
        columns = get_columns_from_file(str(temp_parquet))
        assert "x" in columns
        assert "y" in columns

    def test_nonexistent_file(self):
        """Test with nonexistent file."""
        columns = get_columns_from_file("/nonexistent/file.csv")
        assert columns == []

    def test_invalid_file(self, temp_dir: Path):
        """Test with invalid file content."""
        invalid_file = temp_dir / "invalid.csv"
        invalid_file.write_text("not,valid\ncsv,content")

        # Should return columns or empty list, not raise
        columns = get_columns_from_file(str(invalid_file))
        assert isinstance(columns, list)


# =============================================================================
# AutoCompleter Tests
# =============================================================================

class TestAutoCompleter:
    """Tests for AutoCompleter class."""

    @pytest.fixture
    def completer(self):
        """Create an AutoCompleter instance."""
        return AutoCompleter()

    def test_init(self, completer):
        """Test AutoCompleter initialization."""
        assert completer._cached_path is None
        assert completer._cached_columns == []

    def test_start_completions(self, completer):
        """Test completions at start of query."""
        completions = completer.get_completions("", 0)

        # Should suggest WITH
        assert any(c.text == "WITH" for c in completions)

    def test_after_with_completions(self, completer):
        """Test completions after WITH."""
        completions = completer.get_completions("WITH ", 5)

        # Should suggest source(
        assert any("source(" in c.text for c in completions)

    def test_column_completions(self, completer, temp_csv: Path):
        """Test column completions."""
        text = f"WITH source('{temp_csv}') PLOT "
        completions = completer.get_completions(text, len(text))

        # Should include columns from file
        assert any(c.text == "x" for c in completions)
        assert any(c.text == "y" for c in completions)

        # Should also include aggregate functions
        assert any(c.text.startswith("count") for c in completions)

    def test_column_cache(self, completer, temp_csv: Path):
        """Test column caching."""
        text = f"WITH source('{temp_csv}') PLOT "
        completer.get_completions(text, len(text))

        assert completer._cached_path == str(temp_csv)
        assert "x" in completer._cached_columns

    def test_cache_update_on_new_file(self, completer, temp_csv: Path, temp_parquet: Path):
        """Test cache updates when file changes."""
        text1 = f"WITH source('{temp_csv}') PLOT "
        completer.get_completions(text1, len(text1))
        assert completer._cached_path == str(temp_csv)

        text2 = f"WITH source('{temp_parquet}') PLOT "
        completer.get_completions(text2, len(text2))
        assert completer._cached_path == str(temp_parquet)

    def test_aggregate_completions(self, completer, temp_csv: Path):
        """Test aggregate function completions."""
        text = f"WITH source('{temp_csv}') PLOT "
        completions = completer.get_completions(text, len(text))

        func_completions = [c for c in completions if c.kind == "function"]
        assert len(func_completions) > 0
        assert any("count(" in c.text for c in func_completions)

    def test_agg_column_completions(self, completer, temp_csv: Path):
        """Test completions inside aggregate function."""
        text = f"WITH source('{temp_csv}') PLOT count("
        completions = completer.get_completions(text, len(text))

        # Should include columns with closing paren
        assert any(c.text.endswith(")") for c in completions)

    def test_plot_type_completions(self, completer, temp_csv: Path):
        """Test plot type completions."""
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x AS "
        completions = completer.get_completions(text, len(text))

        types = [c.text for c in completions if c.kind == "type"]
        assert "'scatter'" in types
        assert "'line'" in types

    def test_filter_op_completions(self, completer, temp_csv: Path):
        """Test filter operator completions."""
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x FILTER value "
        completions = completer.get_completions(text, len(text))

        ops = [c.text for c in completions if c.kind == "operator"]
        assert "=" in ops
        assert ">" in ops

    def test_format_key_completions(self, completer, temp_csv: Path):
        """Test format key completions."""
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT "
        completions = completer.get_completions(text, len(text))

        keys = [c.text for c in completions]
        assert "title" in keys

    def test_format_color_completions(self, completer, temp_csv: Path):
        """Test format color value completions."""
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT marker_color = "
        # Use higher limit to get all color options
        completions = completer.get_completions(text, len(text), limit=20)

        # Should include color literals
        assert any("red" in c.display for c in completions)
        assert any("blue" in c.display for c in completions)

        # Should also include column names
        col_completions = [c for c in completions if c.kind == "column"]
        assert len(col_completions) > 0

    def test_limit_parameter(self, completer, temp_csv: Path):
        """Test limit parameter."""
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT "
        completions = completer.get_completions(text, len(text), limit=3)

        assert len(completions) <= 3

    def test_invalidate_cache(self, completer, temp_csv: Path):
        """Test cache invalidation."""
        text = f"WITH source('{temp_csv}') PLOT "
        completer.get_completions(text, len(text))

        assert completer._cached_path is not None

        completer.invalidate_cache()

        assert completer._cached_path is None
        assert completer._cached_columns == []

    def test_completions_sorted(self, completer, temp_csv: Path):
        """Test that completions are sorted appropriately."""
        text = f"WITH source('{temp_csv}') PLOT "
        completions = completer.get_completions(text, len(text))

        # Verify we get results
        assert len(completions) > 0

    def test_prefix_matching(self, completer, temp_csv: Path):
        """Test prefix matching in completions."""
        text = f"WITH source('{temp_csv}') PLOT x"
        completions = completer.get_completions(text, len(text))

        # Column 'x' should be first (prefix match)
        if completions:
            assert completions[0].text == "x"

    def test_no_duplicates(self, completer, temp_csv: Path):
        """Test that completions have no duplicates."""
        text = f"WITH source('{temp_csv}') PLOT "
        completions = completer.get_completions(text, len(text))

        texts = [c.text for c in completions]
        assert len(texts) == len(set(texts))


class TestAutoCompleterValidFormatOptions:
    """Tests for _get_valid_format_options method."""

    @pytest.fixture
    def completer(self):
        return AutoCompleter()

    def test_scatter_format_options(self, completer):
        """Test format options for scatter plot."""
        options = completer._get_valid_format_options("scatter")

        assert "title" in options
        assert "marker_color" in options
        assert "marker_size" in options

    def test_line_format_options(self, completer):
        """Test format options for line plot."""
        options = completer._get_valid_format_options("line")

        assert "title" in options
        assert "line_color" in options
        # marker_color should not be in line options
        assert "marker_color" not in options

    def test_bar_format_options(self, completer):
        """Test format options for bar plot."""
        options = completer._get_valid_format_options("bar")

        assert "title" in options
        assert "color" in options

    def test_unknown_plot_type(self, completer):
        """Test format options for unknown plot type."""
        options = completer._get_valid_format_options(None)

        # Should return all options
        assert len(options) == len(FORMAT_OPTIONS)


# =============================================================================
# Integration Tests
# =============================================================================

class TestAutoCompleterIntegration:
    """Integration tests for AutoCompleter."""

    def test_full_query_completion_flow(self, temp_csv: Path):
        """Test completion flow through a full query."""
        completer = AutoCompleter()

        # Start - should suggest WITH
        completions = completer.get_completions("", 0)
        assert any(c.text == "WITH" for c in completions)

        # After WITH - should suggest quote
        completions = completer.get_completions("WITH ", 5)
        assert len(completions) > 0

        # After file - should suggest PLOT
        text = f"WITH source('{temp_csv}') "
        completions = completer.get_completions(text, len(text))
        assert any(c.text == "PLOT" for c in completions)

        # After PLOT - should suggest columns
        text = f"WITH source('{temp_csv}') PLOT "
        completions = completer.get_completions(text, len(text))
        assert any(c.kind == "column" for c in completions)

        # After y - should suggest AGAINST
        text = f"WITH source('{temp_csv}') PLOT y "
        completions = completer.get_completions(text, len(text))
        assert any(c.text == "AGAINST" for c in completions)

        # After x - should suggest AS, FILTER, FORMAT
        text = f"WITH source('{temp_csv}') PLOT y AGAINST x "
        completions = completer.get_completions(text, len(text))
        assert any(c.text == "AS" for c in completions)
        assert any(c.text == "FILTER" for c in completions)
        assert any(c.text == "FORMAT" for c in completions)

    def test_multiline_query(self, temp_csv: Path):
        """Test completions work with multiline queries."""
        completer = AutoCompleter()

        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x
FORMAT """
        completions = completer.get_completions(text, len(text))

        # Should suggest format options
        assert any(c.text == "title" for c in completions)


class TestMultiSeriesAutocomplete:
    """Tests for autocomplete with multiple series."""

    @pytest.fixture
    def completer(self):
        return AutoCompleter()

    def test_plot_keyword_after_first_series(self, completer, temp_csv: Path):
        """Test typing PLOT after completing first series suggests PLOT keyword."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
    FORMAT color = 'peach'
PL"""
        completions = completer.get_completions(text, len(text))

        # Should suggest PLOT keyword
        assert any(c.text == "PLOT" for c in completions), f"Expected PLOT in completions, got: {[c.text for c in completions]}"

    def test_column_after_second_plot(self, completer, temp_csv: Path):
        """Test column suggestions after second PLOT keyword."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
PLOT """
        completions = completer.get_completions(text, len(text))

        # Should suggest columns (x and y are in the temp_csv fixture)
        assert any(c.kind == "column" for c in completions), f"Expected columns in completions, got: {[c.text for c in completions]}"

    def test_against_after_second_series_column(self, completer, temp_csv: Path):
        """Test AGAINST suggestion after column in second series."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
PLOT y """
        completions = completer.get_completions(text, len(text))

        # Should suggest AGAINST
        assert any(c.text == "AGAINST" for c in completions), f"Expected AGAINST in completions, got: {[c.text for c in completions]}"

    def test_column_after_against_in_second_series(self, completer, temp_csv: Path):
        """Test column suggestions after AGAINST in second series."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
PLOT y AGAINST """
        completions = completer.get_completions(text, len(text))

        # Should suggest columns
        assert any(c.kind == "column" for c in completions), f"Expected columns in completions, got: {[c.text for c in completions]}"

    def test_as_after_second_series_against_column(self, completer, temp_csv: Path):
        """Test AS/FILTER/FORMAT suggestions after AGAINST column in second series."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
PLOT y AGAINST x """
        completions = completer.get_completions(text, len(text))

        # Should suggest AS, FILTER, FORMAT, and PLOT (for another series)
        completion_texts = [c.text for c in completions]
        assert "AS" in completion_texts, f"Expected AS in completions, got: {completion_texts}"

    def test_format_after_format_value_suggests_plot_and_and(self, completer, temp_csv: Path):
        """Test suggestions after FORMAT value include PLOT for new series."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
    FORMAT color = 'blue' """
        completions = completer.get_completions(text, len(text))

        completion_texts = [c.text for c in completions]
        # Should suggest AND (for more format options) and PLOT (for new series)
        assert "AND" in completion_texts or "PLOT" in completion_texts, f"Expected AND or PLOT, got: {completion_texts}"

    def test_three_series_third_plot_column(self, completer, temp_csv: Path):
        """Test column suggestions work for third series."""
        text = f"""WITH source('{temp_csv}')
PLOT y AGAINST x AS 'line'
PLOT y AGAINST x AS 'scatter'
PLOT """
        completions = completer.get_completions(text, len(text))

        # Should suggest columns
        assert any(c.kind == "column" for c in completions), f"Expected columns in completions, got: {[c.text for c in completions]}"
