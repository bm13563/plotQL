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
from plotql.core.engines import get_engine
from plotql.core.executor import ExecutionError, PlotData, execute
from plotql.core.parser import ParseError, parse

# Soft Pastel syntax highlighting theme - gentle colors, easy on the eyes
PLOTQL_THEME = TextAreaTheme(
    name="plotql-pastel",
    base_style=Style(color="#d4d4d4", bgcolor="#1e1e2e"),         # Soft grey on dark blue
    gutter_style=Style(color="#6c7086", bgcolor="#1e1e2e"),       # Muted gutter
    cursor_style=Style(color="#1e1e2e", bgcolor="#89dceb"),       # Soft cyan cursor
    cursor_line_style=Style(bgcolor="#262637"),                   # Subtle line highlight
    bracket_matching_style=Style(color="#f9e2af", bgcolor="#1e1e2e", bold=True),
    selection_style=Style(color="#d4d4d4", bgcolor="#45475a"),    # Selection
    syntax_styles={
        # Keywords - soft mint green (WITH, PLOT, AGAINST, AS, FILTER, FORMAT)
        "keyword": Style(color="#a6e3a1", bold=True),
        # Logical operators - soft teal (AND, OR, NOT)
        "keyword.operator": Style(color="#94e2d5"),
        # Functions - soft yellow (count, sum, avg, etc.)
        "function": Style(color="#f9e2af", bold=True),
        # Strings - soft pink/rose
        "string": Style(color="#f5c2e7"),
        # Numbers - soft sky blue
        "number": Style(color="#89dceb"),
        # Identifiers/columns - soft blue
        "variable": Style(color="#89b4fa"),
        # Operators - soft teal (=, <, >, etc.)
        "operator": Style(color="#94e2d5"),
        # Comments
        "comment": Style(color="#6c7086", italic=True),
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
PLOT price AGAINST received_at
"""


class CompletionPopup(Static):
    """Popup widget showing autocomplete suggestions - Soft Pastel style."""

    DEFAULT_CSS = """
    CompletionPopup {
        layer: popup;
        width: auto;
        height: auto;
        max-height: 8;
        background: #1e1e2e;
        color: #cdd6f4;
        border: none;
        padding: 0;
        display: none;
    }
    CompletionPopup.visible {
        display: block;
    }
    """

    # Soft Pastel palette - Catppuccin inspired
    HIGHLIGHT_BG = "#89dceb"   # Soft cyan - selected item
    HIGHLIGHT_FG = "#1e1e2e"   # Dark background for contrast
    NORMAL_BG = "#1e1e2e"      # Dark blue base
    NORMAL_FG = "#cdd6f4"      # Soft text

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
        # Alternative copy/paste that don't conflict with terminal
        Binding("ctrl+shift+c", "copy", "Copy", show=False),
        Binding("ctrl+shift+v", "paste", "Paste", show=False),
        Binding("ctrl+shift+x", "cut", "Cut", show=False),
    ]

    def __init__(self):
        # Start with default theme, we'll switch after registering ours
        super().__init__(
            EXAMPLE_QUERY,
            language=None,
            id="editor",
        )
        # Register and apply our custom pastel theme
        self.register_theme(PLOTQL_THEME)
        self.theme = "plotql-pastel"
        # Register and activate PlotQL language for syntax highlighting
        if PLOTQL_LANGUAGE and PLOTQL_HIGHLIGHTS:
            self.register_language("plotql", PLOTQL_LANGUAGE, PLOTQL_HIGHLIGHTS)
            self.language = "plotql"
        self.tab_size = 2
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

        # Check if we're in a file path context (inside quotes after WITH)
        file_path_match = re.search(r"WITH\s+['\"]([^'\"]*?)$", before, re.IGNORECASE)
        if file_path_match:
            # Replace only the path portion, keep the quote
            path_start = file_path_match.start(1)
            new_text = self.text[:path_start] + text + self.text[offset:]
            self.text = new_text
            new_offset = path_start + len(text)
            self._move_cursor_to_offset(new_offset)
            return

        # Find word boundary (include path characters for file paths)
        match = re.search(r"[a-zA-Z0-9_./'-]*$", before)
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

    def action_copy(self) -> None:
        """Copy selected text."""
        import pyperclip
        try:
            text = self.selected_text
            logger.debug(f"Copy action: selected_text = {text!r}")
            if text:
                pyperclip.copy(text)
                logger.debug("Copied to clipboard")
        except Exception as e:
            logger.error(f"Copy failed: {e}")

    def action_paste(self) -> None:
        """Paste from clipboard."""
        import pyperclip
        try:
            text = pyperclip.paste()
            if text:
                self.insert(text)
        except Exception:
            pass

    def action_cut(self) -> None:
        """Cut selected text."""
        if self.selected_text:
            self.action_copy()
            self.delete_selection()


class PlotPanel(Static):
    """Plot display panel using textual-image for HD rendering."""

    DEFAULT_CSS = """
    PlotPanel {
        width: 100%;
        height: 100%;
        background: #1e1e2e;
    }
    PlotPanel > Image {
        width: 100%;
        height: 100%;
    }
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

    def render_plot(self, data: PlotData) -> None:
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

    def set_success(self, data: PlotData) -> None:
        filtered = data.filtered_count
        total = data.row_count
        if filtered == total:
            self.update(f"[green]OK[/] - {total} rows")
        else:
            self.update(f"[green]OK[/] - {filtered}/{total} rows (filtered)")

    def set_error(self, message: str) -> None:
        # Truncate long errors
        if len(message) > 80:
            message = message[:77] + "..."
        self.update(f"[red]Error:[/] {message}")


class PlotQLApp(App):
    """PlotQL interactive TUI application."""

    TITLE = "PlotQL"
    CSS = """
    Screen {
        layers: base popup;
    }
    #editor {
        height: 30%;
        border: solid green;
    }
    #plot {
        height: 1fr;
        background: #1e1e2e;
    }
    #plot-image {
        width: 100%;
        height: 100%;
    }
    #status {
        height: 1;
        background: $surface;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("f5", "execute", "Execute", show=True),
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


def run_tui(query: Optional[str] = None) -> None:
    """Run the PlotQL TUI application."""
    app = PlotQLApp(initial_query=query)
    app.run()
