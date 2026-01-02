"""PlotResult - Abstract wrapper for rendered plot output."""
from __future__ import annotations

from io import BytesIO
from typing import Any, Callable, Optional


class PlotResult:
    """
    Abstract wrapper for rendered plot output.

    Provides multiple output formats from a single render operation,
    enabling use in Jupyter notebooks, saving to files, or further
    customization of the underlying figure.

    This class is engine-agnostic - it receives callbacks from the engine
    to handle format-specific operations like saving and exporting.

    Example:
        from plotql.core import parse, execute, render

        result = render(execute(parse("WITH 'data.csv' PLOT y AGAINST x")))

        # Multiple output options:
        result.save("plot.png")           # Save to file
        result.figure.set_title("Custom") # Modify underlying figure
        result.show()                     # Display interactively
        png_bytes = result.to_bytes()     # Get raw bytes
    """

    def __init__(
        self,
        figure: Any,
        save_func: Callable[[Any, str, Optional[str]], None],
        to_bytes_func: Callable[[Any, str], bytes],
        show_func: Callable[[Any], None],
        close_func: Callable[[Any], None],
    ) -> None:
        """
        Initialize PlotResult.

        Args:
            figure: The underlying figure object (engine-specific)
            save_func: Function to save figure to file (figure, path, format) -> None
            to_bytes_func: Function to export figure to bytes (figure, format) -> bytes
            show_func: Function to display figure interactively (figure) -> None
            close_func: Function to close figure and free memory (figure) -> None
        """
        self._figure = figure
        self._save_func = save_func
        self._to_bytes_func = to_bytes_func
        self._show_func = show_func
        self._close_func = close_func

    @property
    def figure(self) -> Any:
        """
        Get the underlying figure object.

        The type depends on the engine (e.g., matplotlib.figure.Figure).
        Use this to further customize the plot before saving or displaying.
        """
        return self._figure

    def to_bytes(self, format: str = "png") -> bytes:
        """
        Export to image bytes.

        Args:
            format: Image format ('png', 'svg', 'pdf', etc.)

        Returns:
            Image data as bytes
        """
        return self._to_bytes_func(self._figure, format)

    def to_image(self) -> Any:
        """
        Convert to PIL Image.

        Returns:
            PIL Image object
        """
        from PIL import Image
        return Image.open(BytesIO(self.to_bytes("png")))

    def save(self, path: str, format: Optional[str] = None) -> None:
        """
        Save to file.

        Args:
            path: Output file path
            format: Image format (inferred from path if not specified)
        """
        self._save_func(self._figure, path, format)

    def show(self) -> None:
        """
        Display in Jupyter or interactive environment.

        In Jupyter notebooks, the plot will be displayed inline.
        In other environments, opens an interactive window.
        """
        self._show_func(self._figure)

    def close(self) -> None:
        """
        Close the figure and free memory.

        Call this when you're done with the result to release resources.
        """
        self._close_func(self._figure)

    def _repr_png_(self) -> bytes:
        """Jupyter notebook PNG display support."""
        return self.to_bytes("png")

    def _repr_svg_(self) -> str:
        """Jupyter notebook SVG display support."""
        return self.to_bytes("svg").decode("utf-8")

    def __repr__(self) -> str:
        return f"PlotResult({type(self._figure).__name__})"
