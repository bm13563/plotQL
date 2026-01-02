"""
PlotQL Themes - Centralized color definitions.

All colors for the application should be defined here and imported elsewhere.
No colors should be hardcoded in core or ui modules.
"""
from plotql.themes.base import PlotQLTheme
from plotql.themes.vaporwave import THEME

# Re-export the active theme and base class for easy access
__all__ = ["PlotQLTheme", "THEME"]
