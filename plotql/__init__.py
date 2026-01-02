"""
PlotQL - SQL-like DSL for terminal plotting.

Usage:
    # Core library
    from plotql import parse, execute, render

    result = render(execute(parse("WITH 'data.csv' PLOT y AGAINST x")))
    result.save("plot.png")

    # TUI
    from plotql.ui import run_tui
    run_tui()
"""
from plotql.core import (
    # Main API
    parse,
    execute,
    render,
    # Result types
    PlotData,
    PlotResult,
    PlotQuery,
    PlotType,
    # Errors
    ParseError,
    ExecutionError,
    # Engine management
    get_engine,
    set_engine,
)

__all__ = [
    "parse",
    "execute",
    "render",
    "PlotData",
    "PlotResult",
    "PlotQuery",
    "PlotType",
    "ParseError",
    "ExecutionError",
    "get_engine",
    "set_engine",
]
__version__ = "0.1.0"
