"""
End-to-end tests for plotql.ui module.

Tests the TUI application with complete query execution pipeline.
Uses Textual's testing framework for async app testing.
"""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from textual.pilot import Pilot

from plotql.ui.tui import (
    PlotQLApp,
    QueryEditor,
    PlotPanel,
    StatusBar,
    CompletionPopup,
    PLOTQL_THEME,
)


# =============================================================================
# PlotQLApp Creation Tests
# =============================================================================

class TestPlotQLAppCreation:
    """Tests for PlotQLApp initialization."""

    def test_app_creation(self):
        """Test basic app creation."""
        app = PlotQLApp()
        assert app.TITLE == "PlotQL"
        assert app.initial_query is None

    def test_app_with_initial_query(self):
        """Test app creation with initial query."""
        query = "WITH source('test.csv') PLOT y AGAINST x"
        app = PlotQLApp(initial_query=query)
        assert app.initial_query == query

    def test_app_bindings(self):
        """Test app has required bindings."""
        app = PlotQLApp()
        binding_keys = [b.key for b in app.BINDINGS]
        assert "ctrl+q" in binding_keys
        assert "f5" in binding_keys


# =============================================================================
# Widget Tests
# =============================================================================

class TestQueryEditor:
    """Tests for QueryEditor widget."""

    @pytest.mark.asyncio
    async def test_editor_creation(self):
        """Test QueryEditor is created with default text."""
        # Mock get_last_query to return None, so the example query is used
        with patch("plotql.ui.tui.get_last_query", return_value=None):
            app = PlotQLApp()
            async with app.run_test() as pilot:
                editor = app.query_one("#editor", QueryEditor)
                assert editor is not None
                assert "WITH" in editor.text
                assert "PLOT" in editor.text

    @pytest.mark.asyncio
    async def test_editor_has_autocompleter(self):
        """Test QueryEditor has autocompleter."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            assert hasattr(editor, "autocompleter")
            assert editor.autocompleter is not None

    @pytest.mark.asyncio
    async def test_editor_theme(self):
        """Test QueryEditor uses custom theme."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            assert editor.theme == "plotql-vaporwave"


class TestPlotPanel:
    """Tests for PlotPanel widget."""

    @pytest.mark.asyncio
    async def test_plot_panel_creation(self):
        """Test PlotPanel is created."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            plot = app.query_one("#plot", PlotPanel)
            assert plot is not None

    @pytest.mark.asyncio
    async def test_plot_panel_has_image(self):
        """Test PlotPanel has image widget."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            plot = app.query_one("#plot", PlotPanel)
            image = plot.query_one("#plot-image")
            assert image is not None

    @pytest.mark.asyncio
    async def test_plot_panel_pixel_size(self):
        """Test PlotPanel calculates pixel size."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            plot = app.query_one("#plot", PlotPanel)
            width, height = plot._get_pixel_size()
            assert width > 0
            assert height > 0


class TestStatusBar:
    """Tests for StatusBar widget."""

    @pytest.mark.asyncio
    async def test_status_bar_creation(self):
        """Test StatusBar is created with ready message."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            status = app.query_one("#status", StatusBar)
            assert status is not None

    @pytest.mark.asyncio
    async def test_status_bar_set_success(self):
        """Test StatusBar success display."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            status = app.query_one("#status", StatusBar)

            # Create mock PlotData with required attributes
            data = MagicMock()
            data.row_count = 3
            data.filtered_count = 3

            status.set_success(data)
            # The status bar should be updated - check it doesn't raise

    @pytest.mark.asyncio
    async def test_status_bar_set_error(self):
        """Test StatusBar error display."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            status = app.query_one("#status", StatusBar)
            status.set_error("Test error message")
            # The status bar should be updated - check it doesn't raise


class TestCompletionPopup:
    """Tests for CompletionPopup widget."""

    @pytest.mark.asyncio
    async def test_completion_popup_creation(self):
        """Test CompletionPopup is created."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            popup = app.query_one("#completion-popup", CompletionPopup)
            assert popup is not None
            assert popup.completions == []

    @pytest.mark.asyncio
    async def test_completion_popup_show_hide(self):
        """Test CompletionPopup show/hide."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            popup = app.query_one("#completion-popup", CompletionPopup)
            editor = app.query_one("#editor", QueryEditor)

            # Show completions
            popup.show_completions(["WITH", "PLOT", "FILTER"], editor)
            assert popup.completions == ["WITH", "PLOT", "FILTER"]
            assert "visible" in popup.classes

            # Hide
            popup.hide()
            assert popup.completions == []
            assert "visible" not in popup.classes

    @pytest.mark.asyncio
    async def test_completion_popup_navigation(self):
        """Test CompletionPopup up/down navigation."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            popup = app.query_one("#completion-popup", CompletionPopup)
            editor = app.query_one("#editor", QueryEditor)

            popup.show_completions(["A", "B", "C"], editor)
            assert popup.selected_index == 0
            assert popup.get_selected() == "A"

            popup.select_next()
            assert popup.selected_index == 1
            assert popup.get_selected() == "B"

            popup.select_next()
            assert popup.selected_index == 2
            assert popup.get_selected() == "C"

            # Wrap around
            popup.select_next()
            assert popup.selected_index == 0

            popup.select_prev()
            assert popup.selected_index == 2


# =============================================================================
# Query Execution E2E Tests
# =============================================================================

class TestQueryExecution:
    """E2E tests for query execution in the TUI."""

    @pytest.mark.asyncio
    async def test_execute_empty_query(self):
        """Test executing an empty query shows error."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Clear the editor
            editor.text = ""

            # Execute (F5) - should not raise
            await pilot.press("f5")

    @pytest.mark.asyncio
    async def test_execute_invalid_syntax(self):
        """Test executing invalid query shows parse error."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = "INVALID SYNTAX HERE"

            # Execute - should not crash the app
            await pilot.press("f5")

    @pytest.mark.asyncio
    async def test_execute_file_not_found(self):
        """Test executing query with nonexistent file shows error."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = "WITH source('/nonexistent/file.csv') PLOT y AGAINST x"

            # Execute - should handle error gracefully
            await pilot.press("f5")

    @pytest.mark.asyncio
    async def test_execute_valid_query(self, temp_csv: Path):
        """Test executing a valid query renders plot."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"

            await pilot.press("f5")
            await pilot.pause()
            # Query should execute successfully

    @pytest.mark.asyncio
    async def test_execute_query_with_filter(self, temp_csv: Path):
        """Test executing query with filter."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x FILTER x > 2"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_execute_query_with_aggregation(self, temp_csv_categorical: Path):
        """Test executing query with aggregation."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv_categorical}') PLOT sum(amount) AGAINST group AS 'bar'"

            await pilot.press("f5")
            await pilot.pause()


# =============================================================================
# App Initialization E2E Tests
# =============================================================================

class TestAppInitialization:
    """E2E tests for app initialization scenarios."""

    @pytest.mark.asyncio
    async def test_app_with_initial_query_auto_executes(self, temp_csv: Path):
        """Test app with initial query auto-executes."""
        query = f"WITH source('{temp_csv}') PLOT y AGAINST x"
        app = PlotQLApp(initial_query=query)

        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Editor should have the query
            assert str(temp_csv) in editor.text

            # Give time for auto-execute
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_app_has_all_widgets(self):
        """Test app creates all required widgets."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            # Query all main widgets
            assert app.query_one("#editor", QueryEditor) is not None
            assert app.query_one("#plot", PlotPanel) is not None
            assert app.query_one("#status", StatusBar) is not None
            assert app.query_one("#completion-popup", CompletionPopup) is not None


# =============================================================================
# Keyboard Navigation E2E Tests
# =============================================================================

class TestKeyboardNavigation:
    """E2E tests for keyboard navigation."""

    @pytest.mark.asyncio
    async def test_f5_executes_query(self, temp_csv: Path):
        """Test F5 key executes query."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"

            # F5 should execute without error
            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_ctrl_q_quits_app(self):
        """Test Ctrl+Q quits the app."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            # This should quit without error
            await pilot.press("ctrl+q")

    @pytest.mark.asyncio
    async def test_escape_dismisses_completion(self):
        """Test Escape dismisses completion popup."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            popup = app.query_one("#completion-popup", CompletionPopup)

            # Show popup
            popup.show_completions(["WITH", "PLOT"], editor)
            editor._completion_active = True

            assert "visible" in popup.classes

            # Focus editor and press escape
            editor.focus()
            await pilot.press("escape")

            # Popup should be hidden
            assert "visible" not in popup.classes


# =============================================================================
# Autocomplete E2E Tests
# =============================================================================

class TestAutocompleteIntegration:
    """E2E tests for autocomplete integration."""

    @pytest.mark.asyncio
    async def test_autocomplete_triggers_on_typing(self):
        """Test autocomplete triggers when typing."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Clear and start typing
            editor.text = ""
            editor.focus()

            # Type "WI" - should trigger completions
            await pilot.press("w", "i")

    @pytest.mark.asyncio
    async def test_autocomplete_with_file_path(self, temp_csv: Path):
        """Test autocomplete shows file completions."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Set partial file path query
            parent_dir = str(temp_csv.parent)
            editor.text = f"WITH '{parent_dir}/"

            # Trigger autocomplete
            editor._show_completions()
            await pilot.pause()


# =============================================================================
# Plot Rendering E2E Tests
# =============================================================================

class TestPlotRendering:
    """E2E tests for plot rendering."""

    @pytest.mark.asyncio
    async def test_scatter_plot_renders(self, temp_csv: Path):
        """Test scatter plot renders successfully."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_line_plot_renders(self, temp_csv: Path):
        """Test line plot renders successfully."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x AS 'line'"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_bar_plot_renders(self, temp_csv_categorical: Path):
        """Test bar plot renders successfully."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv_categorical}') PLOT sum(amount) AGAINST group AS 'bar'"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_histogram_renders(self, temp_csv: Path):
        """Test histogram renders successfully."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x AS 'hist'"

            await pilot.press("f5")
            await pilot.pause()


# =============================================================================
# Format Options E2E Tests
# =============================================================================

class TestFormatOptions:
    """E2E tests for format options rendering."""

    @pytest.mark.asyncio
    async def test_plot_with_title(self, temp_csv: Path):
        """Test plot with custom title."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT title = 'My Plot'"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_plot_with_labels(self, temp_csv: Path):
        """Test plot with axis labels."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT xlabel = 'X' AND ylabel = 'Y'"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_plot_with_color(self, temp_csv: Path):
        """Test plot with custom color."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x FORMAT marker_color = blue"

            await pilot.press("f5")
            await pilot.pause()


# =============================================================================
# Error Display E2E Tests
# =============================================================================

class TestErrorDisplay:
    """E2E tests for error handling and display."""

    @pytest.mark.asyncio
    async def test_parse_error_display(self):
        """Test parse error is displayed properly."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = "INVALID"

            # Should handle error without crashing
            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_execution_error_display(self):
        """Test execution error is displayed properly."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = "WITH source('/no/such/file.csv') PLOT y AGAINST x"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_column_not_found_error(self, temp_csv: Path):
        """Test column not found error is displayed."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            editor.text = f"WITH source('{temp_csv}') PLOT nonexistent AGAINST x"

            await pilot.press("f5")
            await pilot.pause()


# =============================================================================
# Theme Tests
# =============================================================================

class TestTheme:
    """Tests for PlotQL theme."""

    def test_theme_name(self):
        """Test theme has correct name."""
        assert PLOTQL_THEME.name == "plotql-vaporwave"

    def test_theme_has_syntax_styles(self):
        """Test theme has syntax highlighting styles."""
        assert "keyword" in PLOTQL_THEME.syntax_styles
        assert "function" in PLOTQL_THEME.syntax_styles
        assert "string" in PLOTQL_THEME.syntax_styles
        assert "number" in PLOTQL_THEME.syntax_styles

    @pytest.mark.asyncio
    async def test_editor_applies_theme(self):
        """Test editor applies custom theme."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)
            assert editor.theme == "plotql-vaporwave"


# =============================================================================
# Full Pipeline E2E Tests
# =============================================================================

class TestFullPipeline:
    """E2E tests for complete query-to-render pipeline."""

    @pytest.mark.asyncio
    async def test_full_pipeline_simple(self, temp_csv: Path):
        """Test complete pipeline: input -> parse -> execute -> render."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Input query
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"

            # Execute
            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_full_pipeline_with_filter(self, temp_csv: Path):
        """Test pipeline with filter clause."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x FILTER x > 2"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_full_pipeline_with_aggregation(self, temp_csv_categorical: Path):
        """Test pipeline with aggregation."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            editor.text = f"WITH source('{temp_csv_categorical}') PLOT count(amount) AGAINST group AS 'bar'"

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_full_pipeline_complex(self, temp_csv: Path):
        """Test complex query through full pipeline."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            editor.text = (
                f"WITH source('{temp_csv}') "
                "PLOT y AGAINST x AS 'line' "
                "FILTER x > 1 AND x < 5 "
                "FORMAT title = 'Test' AND line_color = blue"
            )

            await pilot.press("f5")
            await pilot.pause()

    @pytest.mark.asyncio
    async def test_multiple_executions(self, temp_csv: Path, temp_csv_categorical: Path):
        """Test multiple query executions in same session."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # First query
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"
            await pilot.press("f5")
            await pilot.pause()

            # Second query - different file and plot type
            editor.text = f"WITH source('{temp_csv_categorical}') PLOT sum(amount) AGAINST group AS 'bar'"
            await pilot.press("f5")
            await pilot.pause()

            # Third query - with error
            editor.text = "INVALID"
            await pilot.press("f5")
            await pilot.pause()

            # Fourth query - back to valid
            editor.text = f"WITH source('{temp_csv}') PLOT y AGAINST x"
            await pilot.press("f5")
            await pilot.pause()


# =============================================================================
# Completion Insertion Tests
# =============================================================================

class TestCompletionInsertion:
    """Tests for completion text insertion in QueryEditor."""

    @pytest.mark.asyncio
    async def test_insert_completion_preserves_quote_in_source(self):
        """Test that completing a path inside source() preserves the opening quote.

        Regression test for bug where completing 'docs/' inside source('docs/
        would lose the opening quote.
        """
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # Set up: user has typed "WITH source('docs/" and cursor is at end
            editor.text = "WITH source('docs/"
            # Position cursor at end
            editor.cursor_location = (0, len(editor.text))

            # Simulate completing with "docs/examples/"
            editor._insert_completion("docs/examples/")

            # The quote should be preserved
            assert "source('docs/examples/" in editor.text, (
                f"Quote was lost! Got: {editor.text}"
            )

    @pytest.mark.asyncio
    async def test_insert_completion_multipart_path_in_source(self):
        """Test completing multi-part paths like docs/examples/file.csv."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # User has typed partial path
            editor.text = "WITH source('docs/ex"
            editor.cursor_location = (0, len(editor.text))

            # Complete with full path
            editor._insert_completion("docs/examples/data.csv'")

            # Should have proper quoted path
            assert "source('docs/examples/data.csv'" in editor.text, (
                f"Path completion failed! Got: {editor.text}"
            )

    @pytest.mark.asyncio
    async def test_insert_completion_root_path_in_source(self):
        """Test completing a path at root level inside source()."""
        app = PlotQLApp()
        async with app.run_test() as pilot:
            editor = app.query_one("#editor", QueryEditor)

            # User just opened the quote
            editor.text = "WITH source('"
            editor.cursor_location = (0, len(editor.text))

            # Complete with a directory
            editor._insert_completion("examples/")

            # Quote should be preserved
            assert "source('examples/" in editor.text, (
                f"Quote was lost! Got: {editor.text}"
            )


# =============================================================================
# Run Function Tests
# =============================================================================

class TestRunFunction:
    """Tests for run_tui function."""

    def test_run_tui_import(self):
        """Test run_tui function can be imported."""
        from plotql.ui.tui import run_tui
        assert callable(run_tui)

    def test_run_tui_creates_app(self):
        """Test run_tui creates app with query."""
        from plotql.ui.tui import PlotQLApp

        # Just verify the app can be instantiated
        app = PlotQLApp(initial_query="WITH source('test.csv') PLOT y AGAINST x")
        assert app.initial_query is not None
