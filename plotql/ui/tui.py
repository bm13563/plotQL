"""
Textual TUI for interactive PlotQL queries.

A harlequin-inspired interface with:
- Multi-line query editor
- Live plot preview
- Error display
- Syntax highlighting
- Autocomplete
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import List, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, TextArea
from textual.widgets.text_area import TextAreaTheme
# Force Sixel rendering for HD quality in supported terminals (VSCode, iTerm2, etc)
from textual_image.widget import SixelImage as TextualImage
from rich.style import Style
from PIL import Image as PILImage
from io import BytesIO

from plotql.ui.autocomplete import AutoCompleter
from plotql.ui.config_editor import ConfigEditorScreen
from plotql.ui.state import get_last_query, save_last_query
from plotql.core import (
    execute,
    get_engine,
    parse,
    ExecutionError,
    ParseError,
    PlotData,
)
from plotql.themes import THEME

# Build TextArea theme from centralized theme
PLOTQL_THEME = TextAreaTheme(
    name=f"plotql-{THEME.name}",
    base_style=Style(color=THEME.text, bgcolor=THEME.background),
    gutter_style=Style(color=THEME.text_muted, bgcolor=THEME.background),
    cursor_style=Style(color=THEME.background, bgcolor=THEME.cursor),
    cursor_line_style=Style(bgcolor=THEME.background_alt),
    bracket_matching_style=Style(color=THEME.highlight, bgcolor=THEME.background, bold=True),
    selection_style=Style(color=THEME.text, bgcolor=THEME.selection),
    syntax_styles={
        # Keywords - muted purple-grey (WITH, PLOT, AGAINST, AS, FILTER, FORMAT)
        # These are very common, so use a calm color
        "keyword": Style(color=THEME.syntax_keyword),
        # Logical operators - warm amber (AND, OR, NOT)
        # Less common, so use a vibrant accent
        "keyword.operator": Style(color=THEME.syntax_keyword_op, bold=True),
        # Functions - soft coral-red (count, sum, avg, etc.)
        # Rare, so use a distinctive accent
        "function": Style(color=THEME.syntax_function, bold=True),
        # Strings - soft rose (file paths, values)
        # Very common
        "string": Style(color=THEME.syntax_string),
        # Numbers - soft teal
        # Medium frequency
        "number": Style(color=THEME.syntax_number),
        # Identifiers/columns - soft lavender
        # Very common, calm color
        "variable": Style(color=THEME.syntax_identifier),
        # Operators - muted purple-grey (=, <, >, etc.)
        # Medium frequency
        "operator": Style(color=THEME.syntax_operator),
        # Comments - muted
        "comment": Style(color=THEME.syntax_comment, italic=True),
    },
)

# Load PlotQL tree-sitter language for syntax highlighting
_TS_DIR = Path(__file__).parent.parent.parent / "tree-sitter-plotql"
_HIGHLIGHTS_SCM = _TS_DIR / "queries" / "highlights.scm"

PLOTQL_LANGUAGE = None
PLOTQL_HIGHLIGHTS = ""

try:
    from tree_sitter import Language
    # Add tree-sitter-plotql to path and import
    sys.path.insert(0, str(_TS_DIR))
    import tree_sitter_plotql as tsplotql
    PLOTQL_LANGUAGE = Language(tsplotql.language())
    PLOTQL_HIGHLIGHTS = _HIGHLIGHTS_SCM.read_text() if _HIGHLIGHTS_SCM.exists() else ""
except Exception as e:
    logging.warning(f"Could not load PlotQL syntax highlighting: {e}")

# Set up logging to file
logging.basicConfig(
    filename="plotql.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


EXAMPLE_QUERY = """\
WITH 'examples/trades.csv'
PLOT price AGAINST received_at AS 'line'
  FORMAT color = 'peach'
PLOT price AGAINST received_at AS 'scatter'
  FILTER tx_sol_amount >= 3
  FORMAT marker_size = 3 AND marker_color = 'teal'
"""


class CompletionPopup(Static):
    """Popup widget showing autocomplete suggestions."""

    DEFAULT_CSS = f"""
    CompletionPopup {{
        layer: popup;
        width: auto;
        height: auto;
        max-height: 8;
        background: {THEME.background};
        color: {THEME.text};
        border: heavy {THEME.border};
        padding: 0;
        display: none;
    }}
    CompletionPopup.visible {{
        display: block;
    }}
    """

    # Colors from theme
    HIGHLIGHT_BG = THEME.cursor        # Selected item background
    HIGHLIGHT_FG = THEME.background    # Selected item text
    NORMAL_BG = THEME.background       # Normal background
    NORMAL_FG = THEME.text             # Normal text

    def __init__(self):
        super().__init__("", id="completion-popup")
        self.completions: List[str] = []
        self.selected_index = 0

    def show_completions(self, completions: List[str], editor: "QueryEditor") -> None:
        """Display completion suggestions positioned relative to cursor."""
        self.completions = completions
        self.selected_index = 0
        if completions:
            self._render_list()
            # Position using cursor screen offset
            try:
                x, y = editor.cursor_screen_offset
                # Place dropdown below cursor, tight to the word
                self.styles.offset = (x, y + 1)
            except Exception:
                pass
            self.add_class("visible")
        else:
            self.hide()

    def hide(self) -> None:
        """Hide the popup."""
        self.remove_class("visible")
        self.completions = []

    def select_next(self) -> None:
        """Move selection down."""
        if self.completions:
            self.selected_index = (self.selected_index + 1) % len(self.completions)
            self._render_list()

    def select_prev(self) -> None:
        """Move selection up."""
        if self.completions:
            self.selected_index = (self.selected_index - 1) % len(self.completions)
            self._render_list()

    def get_selected(self) -> Optional[str]:
        """Get the currently selected completion."""
        if self.completions and 0 <= self.selected_index < len(self.completions):
            return self.completions[self.selected_index]
        return None

    def _render_list(self) -> None:
        """Render the completion list with Harlequin-style formatting."""
        lines = []
        for i, comp in enumerate(self.completions[:8]):  # Max 8 items
            if i == self.selected_index:
                # Selected: pastel cyan/teal background with dark text
                lines.append(f"[{self.HIGHLIGHT_FG} on {self.HIGHLIGHT_BG}] {comp} [/]")
            else:
                # Normal: dark bg with light text
                lines.append(f"[{self.NORMAL_FG} on {self.NORMAL_BG}] {comp} [/]")
        self.update("\n".join(lines))


class QueryEditor(TextArea):
    """Multi-line query editor with PlotQL syntax highlighting and autocomplete."""

    BINDINGS = [
        Binding("ctrl+a", "select_all", "Select All", show=False),
        Binding("ctrl+space", "autocomplete", "Autocomplete", show=False),
        Binding("escape", "dismiss_completion", "Dismiss", show=False),
    ]

    def __init__(self):
        # Load saved query or fall back to example
        initial_query = get_last_query() or EXAMPLE_QUERY
        # Start with default theme, we'll switch after registering ours
        super().__init__(
            initial_query,
            language=None,
            id="editor",
        )
        # Register and apply our custom theme
        self.register_theme(PLOTQL_THEME)
        self.theme = PLOTQL_THEME.name
        # Register and activate PlotQL language for syntax highlighting
        if PLOTQL_LANGUAGE and PLOTQL_HIGHLIGHTS:
            self.register_language("plotql", PLOTQL_LANGUAGE, PLOTQL_HIGHLIGHTS)
            self.language = "plotql"
        self.tab_behavior = "indent"
        self.indent_width = 2
        self.autocompleter = AutoCompleter()
        self._completion_active = False

    def on_text_area_changed(self, _event) -> None:
        """Auto-trigger completions as user types."""
        text = self.text
        if not text:
            return

        # Get character before cursor
        offset = self._get_cursor_offset()
        if offset > 0:
            char = text[offset - 1] if offset <= len(text) else ""
            # Trigger on quote (for file paths), open paren, space, newline, or alphanumeric
            if char in ("'", '"', " ", "/", "(", "\n") or char.isalnum():
                self._show_completions()

    def _get_cursor_offset(self) -> int:
        """Convert cursor location to character offset."""
        row, col = self.cursor_location
        lines = self.text.split("\n")
        offset = sum(len(lines[i]) + 1 for i in range(row))
        offset += col
        return offset

    def action_select_all(self) -> None:
        """Select all text."""
        self.select_all()

    def action_autocomplete(self) -> None:
        """Trigger autocomplete."""
        self._show_completions()

    def action_dismiss_completion(self) -> None:
        """Dismiss the completion popup."""
        popup = self.app.query_one("#completion-popup", CompletionPopup)
        popup.hide()
        self._completion_active = False

    def _show_completions(self) -> None:
        """Show autocomplete suggestions."""
        try:
            popup = self.app.query_one("#completion-popup", CompletionPopup)
            offset = self._get_cursor_offset()
            completions = self.autocompleter.get_completions(self.text, offset)

            if completions:
                # Extract display text
                display_items = [c.display for c in completions]
                # Pass editor for cursor positioning
                popup.show_completions(display_items, self)
                # Store full completions for insertion
                popup._full_completions = completions
                self._completion_active = True
            else:
                popup.hide()
                self._completion_active = False
        except Exception as e:
            logger.error(f"Autocomplete error: {e}")

    def on_key(self, event) -> None:
        """Handle key events for autocomplete navigation."""
        if not self._completion_active:
            return

        try:
            popup = self.app.query_one("#completion-popup", CompletionPopup)

            if event.key == "down":
                popup.select_next()
                event.prevent_default()
                event.stop()
            elif event.key == "up":
                popup.select_prev()
                event.prevent_default()
                event.stop()
            elif event.key == "tab":
                # Only Tab accepts completion, Enter should still insert newline
                self._accept_completion()
                event.prevent_default()
                event.stop()
            elif event.key == "escape" or event.key == "enter":
                # Escape or Enter dismisses popup (Enter will then insert newline)
                popup.hide()
                self._completion_active = False
                # Don't prevent default for Enter - let it insert newline
        except Exception:
            pass

    def _accept_completion(self) -> None:
        """Accept the selected completion."""
        try:
            popup = self.app.query_one("#completion-popup", CompletionPopup)
            if hasattr(popup, "_full_completions") and popup._full_completions:
                idx = popup.selected_index
                if 0 <= idx < len(popup._full_completions):
                    completion = popup._full_completions[idx]
                    # Insert the completion text
                    self._insert_completion(completion.text)

            popup.hide()
            self._completion_active = False
        except Exception as e:
            logger.error(f"Accept completion error: {e}")

    def _insert_completion(self, text: str) -> None:
        """Insert completion text, replacing the partial word."""
        import re

        offset = self._get_cursor_offset()
        before = self.text[:offset]

        # Check if we're in a file path context (inside quotes in source() or after WITH)
        # Matches: source('path, source("path, WITH 'path, WITH "path
        file_path_match = re.search(r"(?:source\(\s*|WITH\s+)['\"]([^'\"]*?)$", before, re.IGNORECASE)
        if file_path_match:
            # Replace only the path portion, keep the quote
            path_start = file_path_match.start(1)
            new_text = self.text[:path_start] + text + self.text[offset:]
            self.text = new_text
            new_offset = path_start + len(text)
            self._move_cursor_to_offset(new_offset)
            return

        # Check if completion is a quoted value (like 'line') and user already typed opening quote
        # This handles: AS 'l -> completing with 'line' should replace 'l with 'line'
        if text and text[0] in ("'", '"') and text[-1] == text[0]:
            # Completion is a quoted string - check if there's a matching opening quote
            quote_char = text[0]
            # Find if there's an unmatched opening quote before cursor
            quote_match = re.search(rf"{quote_char}([^{quote_char}]*)$", before)
            if quote_match:
                # User typed quote + partial, replace from the quote
                quote_start = quote_match.start()
                new_text = self.text[:quote_start] + text + self.text[offset:]
                self.text = new_text
                new_offset = quote_start + len(text)
                self._move_cursor_to_offset(new_offset)
                return

        # Find word boundary (include path characters for file paths, but NOT quotes)
        match = re.search(r"[a-zA-Z0-9_./-]*$", before)
        if match:
            word_start = match.start()
            # Replace the partial word with completion
            new_text = self.text[:word_start] + text + self.text[offset:]
            self.text = new_text
            # Move cursor to end of inserted text
            new_offset = word_start + len(text)
            self._move_cursor_to_offset(new_offset)
        else:
            self.insert(text)

    def _move_cursor_to_offset(self, offset: int) -> None:
        """Move cursor to a character offset."""
        lines = self.text.split("\n")
        current = 0
        for row, line in enumerate(lines):
            line_len = len(line) + 1  # +1 for newline
            if current + line_len > offset:
                col = offset - current
                self.cursor_location = (row, min(col, len(line)))
                return
            current += line_len
        # End of text
        if lines:
            self.cursor_location = (len(lines) - 1, len(lines[-1]))


class PlotPanel(Static):
    """Plot display panel using textual-image for HD rendering."""

    DEFAULT_CSS = f"""
    PlotPanel {{
        width: 100%;
        height: 100%;
        background: {THEME.background};
        align: center middle;
    }}
    PlotPanel > Image {{
        width: auto;
        height: 1fr;
    }}
    """

    # Default cell size in pixels (common terminal default)
    CELL_WIDTH = 9.0
    CELL_HEIGHT = 18.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_size = (0, 0)

    def compose(self) -> ComposeResult:
        """Create the image widget."""
        placeholder = self._create_placeholder()
        yield TextualImage(placeholder, id="plot-image")

    def _create_placeholder(self) -> PILImage.Image:
        """Create a placeholder image matching the terminal background."""
        engine = get_engine()
        img = PILImage.new("RGB", (400, 300), color=engine.COLORS["background"])
        return img

    def _get_pixel_size(self) -> tuple[int, int]:
        """Calculate pixel dimensions based on widget size."""
        # Get widget size in terminal cells
        cell_width = self.size.width
        cell_height = self.size.height

        if cell_width <= 0 or cell_height <= 0:
            return (800, 600)  # Default fallback

        px_width = int(cell_width * self.CELL_WIDTH)
        px_height = int(cell_height * self.CELL_HEIGHT)

        return (px_width, px_height)

    def render_plot(self, data: List[PlotData]) -> None:
        """Render plot from query results using the configured engine."""
        try:
            # Get current widget size in pixels
            width, height = self._get_pixel_size()

            # Render to PNG bytes using the engine at 1:1 scale (no downsampling)
            engine = get_engine()
            img_bytes = engine.render_to_bytes(data, width, height, scale=1.0)

            # Save to file for debugging
            with open("debug_plot.png", "wb") as f:
                f.write(img_bytes)
            logger.info(f"Saved debug_plot.png ({width}x{height})")

            # Load as PIL Image
            img = PILImage.open(BytesIO(img_bytes))

            # Update the image widget by querying for it
            try:
                image_widget = self.query_one("#plot-image", TextualImage)
                image_widget.image = img
                self._last_size = (width, height)
                logger.info(f"Plot rendered: {width}x{height}")
            except Exception as e:
                logger.error(f"Could not find image widget: {e}")

        except Exception as e:
            logger.error(f"Plot render error: {e}")
            self.show_error(str(e))

    def show_error(self, message: str) -> None:
        """Display error state."""
        try:
            image_widget = self.query_one("#plot-image", TextualImage)
            image_widget.image = self._create_placeholder()
        except Exception:
            pass


class StatusBar(Static):
    """Shows query status and row counts."""

    def __init__(self):
        super().__init__("Ready - Press F5 to execute", id="status")

    def set_success(self, data_list: List[PlotData]) -> None:
        # Use first series for row counts (all series share same base data)
        first = data_list[0]
        filtered = first.filtered_count
        total = first.row_count
        series_count = len(data_list)

        if series_count == 1:
            if filtered == total:
                self.update(f"[green]OK[/] - {total} rows")
            else:
                self.update(f"[green]OK[/] - {filtered}/{total} rows (filtered)")
        else:
            # Show series count for multi-series queries
            self.update(f"[green]OK[/] - {total} rows, {series_count} series")

    def set_error(self, message: str) -> None:
        # Truncate long errors
        if len(message) > 80:
            message = message[:77] + "..."
        self.update(f"[red]Error:[/] {message}")


class PlotQLApp(App):
    """PlotQL interactive TUI application."""

    TITLE = "PlotQL"
    CSS = f"""
    Screen {{
        layers: base popup;
        background: {THEME.background};
    }}
    #editor {{
        height: 30%;
        border: heavy {THEME.border};
    }}
    #plot {{
        height: 1fr;
        background: {THEME.background};
        align: center middle;
    }}
    #plot-image {{
        width: auto;
        height: 1fr;
    }}
    #status {{
        height: 1;
        background: {THEME.background_alt};
        color: {THEME.text};
        padding: 0 1;
    }}
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("f5", "execute", "Execute", show=True),
        Binding("f2", "edit_config", "Connectors", show=True),
    ]

    def __init__(self, initial_query: Optional[str] = None):
        super().__init__()
        self.initial_query = initial_query
        logger.info("PlotQLApp initialized")

    def on_key(self, event) -> None:
        """Log all key events for debugging."""
        logger.debug(f"Key pressed: {event.key}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            QueryEditor(),
            PlotPanel(id="plot"),
            StatusBar(),
            id="main",
        )
        yield CompletionPopup()
        yield Footer()

    def on_mount(self) -> None:
        if self.initial_query:
            editor = self.query_one("#editor", TextArea)
            editor.text = self.initial_query
            # Auto-execute if query provided
            self.action_execute()

    def action_execute(self) -> None:
        """Execute the current query."""
        logger.info("action_execute called!")
        editor = self.query_one("#editor", TextArea)
        plot = self.query_one("#plot", PlotPanel)
        status = self.query_one("#status", StatusBar)

        query_text = editor.text.strip()
        if not query_text:
            status.set_error("Empty query")
            return

        try:
            # Parse
            ast = parse(query_text)
            # Execute
            data = execute(ast)
            # Render
            plot.render_plot(data)
            status.set_success(data)

        except ParseError as e:
            status.set_error(f"Parse: {e.message}")
            plot.show_error(str(e))

        except ExecutionError as e:
            status.set_error(str(e))
            plot.show_error(str(e))

        except Exception as e:
            status.set_error(str(e))
            plot.show_error(str(e))

    def action_edit_config(self) -> None:
        """Open the config editor screen."""
        self.push_screen(ConfigEditorScreen())

    def _save_state(self) -> None:
        """Save current query to state file."""
        try:
            editor = self.query_one("#editor", TextArea)
            query_text = editor.text.strip()
            if query_text:
                save_last_query(query_text)
        except Exception:
            pass  # Silently fail if we can't save

    def action_quit(self) -> None:
        """Save state and quit."""
        self._save_state()
        self.exit()


def run_tui(query: Optional[str] = None) -> None:
    """Run the PlotQL TUI application."""
    app = PlotQLApp(initial_query=query)
    app.run()
