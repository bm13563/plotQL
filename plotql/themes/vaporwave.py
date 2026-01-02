"""
Vaporwave/Pastel theme for PlotQL.

A warm retro aesthetic with soft pink undertones, inspired by vaporwave
and terminal aesthetics. Syntax colors are chosen for high contrast
against the dark background while maintaining the vaporwave aesthetic.
"""
from plotql.themes.base import PlotQLTheme


# Vaporwave/Pastel Theme
# Warm dark base with soft pink undertones
# Syntax highlighting prioritizes readability with vibrant vaporwave colors
THEME = PlotQLTheme(
    name="vaporwave",

    # Base colors - warm dark purple-grey with pink undertone
    background="#1f1d2e",
    background_alt="#26233a",
    text="#e0def4",
    text_muted="#6e6a86",
    border="#6e6a86",

    # Plot styling
    grid="#3e3a52",
    axes="#6e6a86",

    # Syntax highlighting - frequency-based color assignment
    # Colors chosen to contrast against pink-purple background (cool tones pop)
    # HIGH FREQUENCY - soft but visible against the warm background
    syntax_identifier="#cba6f7",   # Soft mint - cool green contrasts warm bg
    syntax_string="#f9e2af",       # Soft butter yellow - warm but light enough
    syntax_keyword="#94e2d5",      # Soft seafoam - cool tone stands out

    # MEDIUM FREQUENCY - subtle accents
    syntax_number="#89dceb",       # Soft sky blue - cool, distinct from strings
    syntax_operator="#cba6f7",     # Soft mauve - visible but not dominant

    # LOW FREQUENCY - vibrant accents for emphasis (draws eye to special elements)
    syntax_keyword_op="#fab387",   # Soft peach - AND/OR/NOT pop out
    syntax_function="#f5c2e7",     # Soft pink - functions are special
    syntax_comment="#6e6a86",      # Same as muted - comments fade away

    # UI accents
    cursor="#ebbcba",
    selection="#403d52",
    highlight="#f6c177",

    # Chart color palette
    chart_colors={
        "primary": "#ebbcba",     # Soft pink - default line color
        "secondary": "#9ccfd8",   # Soft teal - markers, second series
        "tertiary": "#c4a7e7",    # Soft lavender
        "quaternary": "#f6c177",  # Warm amber
        "accent": "#eb6f92",      # Soft coral-red
    },

    # Gradient for continuous color scales
    gradient=["#9ccfd8", "#f6c177"],  # Teal -> Amber (vaporwave feel)

    # User color name mappings
    color_map={
        "blue": "#9ccfd8",
        "red": "#eb6f92",
        "green": "#a6da95",
        "yellow": "#f6c177",
        "orange": "#f6c177",
        "pink": "#ebbcba",
        "purple": "#c4a7e7",
        "cyan": "#9ccfd8",
        "teal": "#9ccfd8",
        "magenta": "#ebbcba",
        "white": "#e0def4",
        "gray": "#6e6a86",
        "grey": "#6e6a86",
        "lavender": "#c4a7e7",
        "coral": "#eb6f92",
        "amber": "#f6c177",
        "mint": "#a6da95",
        "rose": "#ebbcba",
    },

    # Font configuration - blocky monospace for retro terminal aesthetic
    font_family="monospace",
    font_stack=["PxPlus IBM VGA8", "Terminus", "Fixedsys", "DejaVu Sans Mono", "Consolas"],
)
