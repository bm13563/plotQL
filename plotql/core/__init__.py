"""
PlotQL Core - Language processing library.

This module provides the core functionality for parsing and executing
PlotQL queries, independent of any UI layer.

Usage:
    from plotql.core import parse, execute, render

    query = parse("WITH 'data.csv' PLOT price AGAINST time AS 'line'")
    data = execute(query)
    result = render(data)

    # Multiple output options:
    result.save("plot.png")           # Save to file
    result.figure.set_title("Custom") # Modify matplotlib figure
    result.show()                     # Display in Jupyter
    png_bytes = result.to_bytes()     # Get raw bytes
"""
from __future__ import annotations

from plotql.core.ast import (
    AggregateFunc,
    ColumnRef,
    Condition,
    ComparisonOp,
    FormatOptions,
    LogicalOp,
    PlotQuery,
    PlotType,
    WhereClause,
)
from plotql.core.config import CONFIG_PATH
from plotql.core.executor import execute, ExecutionError, PlotData
from plotql.core.parser import parse, ParseError
from plotql.core.result import PlotResult
from plotql.core.engines import get_engine, set_engine, Engine, MatplotlibEngine


def render(data: PlotData, width: int = 800, height: int = 600) -> PlotResult:
    """
    Render PlotData to a PlotResult using the default engine.

    This is a convenience function that uses the globally configured engine.

    Args:
        data: The plot data from query execution
        width: Width in pixels (default 800)
        height: Height in pixels (default 600)

    Returns:
        PlotResult wrapper providing multiple output formats

    Example:
        from plotql.core import parse, execute, render

        result = render(execute(parse("WITH 'data.csv' PLOT y AGAINST x")))
        result.save("output.png")
    """
    return get_engine().render(data, width, height)


__all__ = [
    # Main API
    "parse",
    "execute",
    "render",
    # Result types
    "PlotData",
    "PlotResult",
    "PlotQuery",
    # AST types
    "PlotType",
    "ColumnRef",
    "AggregateFunc",
    "FormatOptions",
    "WhereClause",
    "Condition",
    "ComparisonOp",
    "LogicalOp",
    # Errors
    "ParseError",
    "ExecutionError",
    # Engine management
    "get_engine",
    "set_engine",
    "Engine",
    "MatplotlibEngine",
    # Configuration
    "CONFIG_PATH",
]
