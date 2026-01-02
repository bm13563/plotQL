"""
PlotQL rendering engines.

This module provides a clean abstraction for rendering backends, allowing
the TUI to remain agnostic of the specific plotting library used.

Usage:
    from plotql.core.engines import get_engine

    engine = get_engine()
    result = engine.render(plot_data, width, height)
    result.save("output.png")

To use a different engine:
    from plotql.core.engines import set_engine
    from plotql.core.engines.matplotlib import MatplotlibEngine

    set_engine(MatplotlibEngine())
"""
from __future__ import annotations

from typing import Optional

from plotql.core.engines.base import Engine
from plotql.core.engines.matplotlib import MatplotlibEngine

__all__ = ["Engine", "MatplotlibEngine", "get_engine", "set_engine"]

_default_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """
    Get the default rendering engine.

    Returns a cached singleton instance of the default engine
    (MatplotlibEngine unless changed via set_engine).
    """
    global _default_engine
    if _default_engine is None:
        _default_engine = MatplotlibEngine()
    return _default_engine


def set_engine(engine: Engine) -> None:
    """
    Set the default rendering engine.

    Use this to swap to a different rendering backend:

        from plotql.engines import set_engine
        from my_engines import PlotlyEngine

        set_engine(PlotlyEngine())
    """
    global _default_engine
    _default_engine = engine
