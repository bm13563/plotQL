"""
PlotQL UI - Terminal User Interface.

This module provides the interactive TUI for PlotQL queries.

Usage:
    from plotql.ui import run_tui

    run_tui()  # Launch the interactive TUI
"""
from __future__ import annotations

from plotql.ui.tui import run_tui, PlotQLApp

__all__ = ["run_tui", "PlotQLApp"]
