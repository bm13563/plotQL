"""Abstract base class for PlotQL rendering engines."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from plotql.core.executor import PlotData
    from plotql.core.result import PlotResult


class Engine(ABC):
    """
    Abstract base class for rendering engines.

    Engines are responsible for converting PlotData into visual output.
    This abstraction allows swapping between different rendering backends
    (matplotlib, plotly, etc.) without changing the TUI or executor code.

    Subclasses must implement:
    - COLORS property: Color palette dict
    - render(): Returns a PlotResult wrapper
    - get_color(): Converts color names to hex values
    """

    @property
    @abstractmethod
    def COLORS(self) -> Dict[str, str]:
        """
        Color palette used by this engine.

        Should include at minimum:
        - "background": Background color
        - "text": Text color
        - "grid": Grid line color
        - "blue", "red", "green", etc.: Named colors for plots
        """
        pass

    @abstractmethod
    def render(
        self,
        data: "PlotData",
        width: int,
        height: int,
    ) -> "PlotResult":
        """
        Render PlotData to a PlotResult wrapper.

        Args:
            data: The plot data from query execution
            width: Width in pixels
            height: Height in pixels

        Returns:
            PlotResult wrapper providing multiple output formats
        """
        pass

    @abstractmethod
    def get_color(self, color_name: Optional[str]) -> str:
        """
        Convert a user-facing color name to a hex color value.

        Args:
            color_name: Color name (e.g., "blue", "red") or None

        Returns:
            Hex color string (e.g., "#89b4fa")
        """
        pass

    def render_to_bytes(
        self,
        data: "PlotData",
        width: int,
        height: int,
        scale: float = 1.0,
    ) -> bytes:
        """
        Convenience method: Render PlotData directly to PNG bytes.

        This is a shorthand for render().to_bytes().

        Args:
            data: The plot data from query execution
            width: Width in pixels
            height: Height in pixels
            scale: Scale factor (default 1.0 for 1:1 pixel mapping)

        Returns:
            PNG image as bytes
        """
        result = self.render(data, int(width * scale), int(height * scale))
        return result.to_bytes()
