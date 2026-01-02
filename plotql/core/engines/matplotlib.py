"""
Matplotlib-based rendering engine for PlotQL.

Generates high-quality plot images using matplotlib that can be displayed
in the terminal via textual-image or saved to files.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Union

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend - must be before pyplot import
# Disable antialiasing for crisp pixel-perfect rendering
matplotlib.rcParams['lines.antialiased'] = False
matplotlib.rcParams['patch.antialiased'] = False
matplotlib.rcParams['text.antialiased'] = True  # Keep text antialiased for readability
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from plotql.core.ast import PlotType  # noqa: E402
from plotql.core.executor import PlotData  # noqa: E402
from plotql.core.engines.base import Engine  # noqa: E402
from plotql.core.result import PlotResult  # noqa: E402


class MatplotlibEngine(Engine):
    """Matplotlib-based rendering engine with Catppuccin-inspired dark theme."""

    # Catppuccin Mocha-inspired pastel color palette
    _COLORS: Dict[str, str] = {
        "background": "#1e1e2e",      # Dark blue-grey base
        "paper": "#1e1e2e",           # Same as background for seamless look
        "text": "#cdd6f4",            # Soft grey text
        "grid": "#313244",            # Subtle grid lines
        "blue": "#89b4fa",            # Soft blue (primary)
        "teal": "#94e2d5",            # Soft teal
        "green": "#a6e3a1",           # Soft mint green
        "yellow": "#f9e2af",          # Soft yellow
        "peach": "#fab387",           # Soft peach/orange
        "pink": "#f5c2e7",            # Soft pink
        "mauve": "#cba6f7",           # Soft purple
        "red": "#f38ba8",             # Soft red
        "sky": "#89dceb",             # Soft sky blue
        "lavender": "#b4befe",        # Soft lavender
    }

    # Map user color names to our pastel palette
    _COLOR_MAP: Dict[str, str] = {
        "blue": _COLORS["blue"],
        "red": _COLORS["red"],
        "green": _COLORS["green"],
        "yellow": _COLORS["yellow"],
        "orange": _COLORS["peach"],
        "pink": _COLORS["pink"],
        "purple": _COLORS["mauve"],
        "cyan": _COLORS["sky"],
        "teal": _COLORS["teal"],
        "magenta": _COLORS["pink"],
        "white": _COLORS["text"],
        "gray": "#6c7086",
        "grey": "#6c7086",
    }

    @property
    def COLORS(self) -> Dict[str, str]:
        """Color palette used by this engine."""
        return self._COLORS

    def get_color(self, color_name: Optional[str]) -> str:
        """Convert a color name to our pastel palette color."""
        if not color_name:
            return self._COLORS["blue"]
        return self._COLOR_MAP.get(color_name.lower(), self._COLORS["blue"])

    def _create_figure(
        self,
        data: PlotData,
        width: int,
        height: int,
    ) -> Figure:
        """
        Create a matplotlib figure from PlotData.

        Args:
            data: The plot data from query execution
            width: Width in pixels
            height: Height in pixels

        Returns:
            A configured matplotlib Figure
        """
        query = data.query
        fmt = query.format

        # Labels
        x_label = str(query.x_column)
        y_label = str(query.y_column)
        title = fmt.title or f"{y_label} vs {x_label}"
        xlabel = fmt.xlabel or x_label
        ylabel = fmt.ylabel or y_label

        # Color
        line_color = self.get_color(fmt.line_color)
        marker_color = self.get_color(fmt.marker_color) if fmt.marker_color else line_color

        # Convert pixels to inches (matplotlib uses inches with DPI)
        # Use 100 DPI for cleaner 1:1 pixel mapping
        dpi = 100
        fig_width = width / dpi
        fig_height = height / dpi

        # Create figure with dark theme
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

        # Apply dark theme styling
        fig.patch.set_facecolor(self._COLORS["background"])
        ax.set_facecolor(self._COLORS["background"])

        # Font sizes for terminal rendering
        TITLE_SIZE = 12
        LABEL_SIZE = 10
        TICK_SIZE = 8

        # Style axes
        ax.spines['bottom'].set_color(self._COLORS["grid"])
        ax.spines['top'].set_color(self._COLORS["grid"])
        ax.spines['left'].set_color(self._COLORS["grid"])
        ax.spines['right'].set_color(self._COLORS["grid"])
        ax.tick_params(colors=self._COLORS["text"], which='both', labelsize=TICK_SIZE)
        ax.xaxis.label.set_color(self._COLORS["text"])
        ax.yaxis.label.set_color(self._COLORS["text"])
        ax.title.set_color(self._COLORS["text"])

        # Grid - thin lines for crisp rendering
        ax.grid(True, color=self._COLORS["grid"], linestyle='-', linewidth=0.5, alpha=0.5)
        ax.set_axisbelow(True)

        # Add plot based on type
        if query.plot_type == PlotType.SCATTER:
            # Handle per-point colors if available
            colors: Union[str, List[str]] = marker_color
            if data.marker_colors:
                colors = [self.get_color(c) for c in data.marker_colors]

            # Handle marker sizes
            sizes = None
            if data.marker_sizes:
                sizes = [max(10, min(20, s * 15)) for s in data.marker_sizes]

            scatter = ax.scatter(
                data.x,
                data.y,
                c=colors,
                s=sizes if sizes else 10,
                alpha=1.0,
                edgecolors='none',
                marker='s',  # Square marker - no antialiasing needed for straight edges
                linewidths=0,
            )
            scatter.set_antialiased(False)

        elif query.plot_type == PlotType.LINE:
            ax.plot(
                data.x,
                data.y,
                color=line_color,
                linewidth=1.5,  # Clean line width for terminal rendering
                alpha=1.0,  # Full opacity for crisp line
                solid_capstyle='round',
                solid_joinstyle='round',
                antialiased=False,  # Crisp lines
            )

        elif query.plot_type == PlotType.BAR:
            ax.bar(
                data.x,
                data.y,
                color=line_color,
                alpha=0.8,
                edgecolor='none',
            )

        elif query.plot_type == PlotType.HIST:
            ax.hist(
                data.y,
                color=line_color,
                alpha=0.8,
                edgecolor=self._COLORS["background"],
                linewidth=0.5,
            )

        # Set labels and title
        ax.set_xlabel(xlabel, fontsize=LABEL_SIZE, color=self._COLORS["text"])
        ax.set_ylabel(ylabel, fontsize=LABEL_SIZE, color=self._COLORS["text"])
        ax.set_title(title, fontsize=TITLE_SIZE, color=self._COLORS["text"], pad=10)

        # Limit x-axis ticks to max 5 for cleaner look
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6))

        # Format tick labels - truncate to max 10 chars with ellipsis
        def truncate_label(text, max_len=10):
            """Truncate label to max length with ellipsis."""
            text = str(text)
            # For timestamps, try to extract just the time portion first
            if ' ' in text and ':' in text:
                parts = text.split(' ')
                if len(parts) >= 2:
                    time_part = parts[1].split('.')[0]  # Remove microseconds
                    time_parts = time_part.split(':')
                    if len(time_parts) >= 2:
                        text = f"{time_parts[0]}:{time_parts[1]}"
            # Truncate if still too long
            if len(text) > max_len:
                text = text[:max_len - 1] + "..."
            return text

        # Apply formatting after drawing
        fig.canvas.draw()
        x_labels = ax.get_xticklabels()
        if x_labels:
            new_labels = [truncate_label(label.get_text()) for label in x_labels]
            ax.set_xticklabels(new_labels, rotation=0, ha='center')

        # Maximize plot area - minimal margins
        fig.tight_layout(pad=0.5)
        fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.12)

        return fig

    def render(
        self,
        data: PlotData,
        width: int,
        height: int,
    ) -> PlotResult:
        """
        Render PlotData to a PlotResult wrapper.

        Args:
            data: The plot data from query execution
            width: Width in pixels
            height: Height in pixels

        Returns:
            PlotResult wrapper providing multiple output formats
        """
        fig = self._create_figure(data, width, height)
        bg_color = self._COLORS["background"]

        return PlotResult(
            figure=fig,
            save_func=lambda f, path, fmt: f.savefig(
                path, format=fmt, facecolor=bg_color, edgecolor='none'
            ),
            to_bytes_func=lambda f, fmt: self._figure_to_bytes(f, fmt, bg_color),
            show_func=lambda f: plt.show(),
            close_func=lambda f: plt.close(f),
        )

    @staticmethod
    def _figure_to_bytes(fig: Figure, format: str, bg_color: str) -> bytes:
        """Convert a matplotlib figure to bytes."""
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format=format, facecolor=bg_color, edgecolor='none')
        buf.seek(0)
        return buf.read()

    @staticmethod
    def get_terminal_pixel_size(
        char_width: int,
        char_height: int,
        cell_width_px: int = 8,
        cell_height_px: int = 16,
    ) -> tuple[int, int]:
        """
        Estimate pixel dimensions from terminal character dimensions.

        Most terminals use roughly 8x16 pixel cells, but this can vary.
        We use conservative estimates to ensure the image fits.

        Args:
            char_width: Width in terminal characters
            char_height: Height in terminal characters
            cell_width_px: Estimated pixels per character width
            cell_height_px: Estimated pixels per character height

        Returns:
            (width_px, height_px) tuple
        """
        return (char_width * cell_width_px, char_height * cell_height_px)
