"""
Config editor screen for PlotQL connectors.

Provides a TUI interface for editing the connectors.toml configuration file.
"""
from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, TextArea

from plotql.core.config import CONFIG_PATH


DEFAULT_CONFIG = '''# PlotQL Connector Configuration
# Location: ~/.config/plotql/connectors.toml

# File connector aliases
# Usage: WITH file(trades) PLOT price AGAINST time
#
# [file.trades]
# path = "/path/to/trades.csv"

# ClickHouse connector
# Usage: WITH clickhouse(production) PLOT price AGAINST time
# Requires: pip install plotql[clickhouse]
#
# [clickhouse.production]
# host = "localhost"
# port = 8123
# username = "default"
# password = ""
# query = "SELECT * FROM trades"
'''


class ConfigEditorScreen(Screen):
    """Screen for editing connectors.toml configuration."""

    BINDINGS = [
        Binding("escape", "save_and_close", "Save & Close", show=True),
        Binding("ctrl+c", "cancel", "Cancel", show=True),
    ]

    CSS = """
    ConfigEditorScreen {
        background: $surface;
    }

    #config-header {
        height: 3;
        padding: 1;
        background: $primary-background;
        color: $text;
    }

    #config-editor {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"Editing: {CONFIG_PATH}\n"
            "Press [bold]Escape[/bold] to save and close, [bold]Ctrl+C[/bold] to cancel",
            id="config-header"
        )
        yield TextArea(id="config-editor")
        yield Footer()

    def on_mount(self) -> None:
        """Load config file content on mount."""
        editor = self.query_one("#config-editor", TextArea)

        if CONFIG_PATH.exists():
            try:
                content = CONFIG_PATH.read_text()
                editor.text = content
            except Exception as e:
                editor.text = f"# Error loading config: {e}\n\n{DEFAULT_CONFIG}"
        else:
            editor.text = DEFAULT_CONFIG

        editor.focus()

    def action_save_and_close(self) -> None:
        """Save the config and close the screen."""
        self._save_config()
        self.app.pop_screen()

    def action_cancel(self) -> None:
        """Close without saving."""
        self.app.pop_screen()

    def _save_config(self) -> None:
        """Save the config file."""
        editor = self.query_one("#config-editor", TextArea)
        content = editor.text

        # Ensure parent directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

        try:
            CONFIG_PATH.write_text(content)
        except Exception as e:
            self.notify(f"Error saving config: {e}", severity="error")
