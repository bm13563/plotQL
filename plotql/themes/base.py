"""
Base theme definition for PlotQL.

This module defines the PlotQLTheme dataclass that all themes must implement.
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class PlotQLTheme:
    """Complete theme definition for PlotQL."""

    name: str

    # Base colors
    background: str          # Main background color
    background_alt: str      # Alternate background (line highlight, panels)
    text: str                # Primary text color
    text_muted: str          # Muted text (gutters, comments)
    border: str              # Border color for panels

    # Plot colors - used for chart rendering
    grid: str                # Grid lines
    axes: str                # Axis spines and ticks

    # Syntax highlighting colors
    # Ordered roughly by frequency (most common -> least common)
    syntax_identifier: str   # Column names, format options (VERY common)
    syntax_string: str       # File paths, values (VERY common)
    syntax_keyword: str      # WITH, PLOT, AGAINST, AS, FILTER, FORMAT (common)
    syntax_number: str       # Numeric values (medium)
    syntax_operator: str     # =, <, >, etc. (medium)
    syntax_keyword_op: str   # AND, OR, NOT (less common - accent)
    syntax_function: str     # count, sum, avg, etc. (rare - accent)
    syntax_comment: str      # Comments (rare)

    # UI accent colors
    cursor: str              # Cursor color
    selection: str           # Selection background
    highlight: str           # Bracket matching, search highlight

    # Chart palette - colors for plot lines, markers, bars
    chart_colors: Dict[str, str] = field(default_factory=dict)

    # Gradient for continuous color scales (colorbars)
    gradient: List[str] = field(default_factory=list)

    # Named color mappings for user-specified colors
    color_map: Dict[str, str] = field(default_factory=dict)

    # Font configuration (for matplotlib plots)
    # font_family: general category (e.g., 'monospace', 'sans-serif', 'serif')
    # font_stack: ordered list of specific fonts to try
    font_family: str = "monospace"
    font_stack: List[str] = field(default_factory=lambda: ["DejaVu Sans Mono"])
