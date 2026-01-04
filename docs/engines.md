# Rendering Engines

PlotQL uses a pluggable engine architecture for rendering plots. This allows different visualization backends while keeping the query language consistent.

## Overview

Engines convert `PlotData` (the result of query execution) into visual output. The engine abstraction means you can:

- Swap backends without changing queries
- Create custom engines for specific needs
- Use the same queries in different environments

## Built-in Engines

### MatplotlibEngine

The default engine uses matplotlib with a dark theme optimized for terminal display.

```python
from plotql.core import get_engine, MatplotlibEngine

# Get the default engine
engine = get_engine()

# Or create explicitly
engine = MatplotlibEngine()
```

Features:
- Dark theme with vaporwave-inspired colors
- Crisp, pixel-perfect rendering (antialiasing disabled for lines)
- Automatic colorbar for continuous color mappings
- Legend for categorical color mappings
- Datetime axis detection and formatting
- Output formats: PNG, SVG, PDF

## Using Engines

### Default Engine

```python
from plotql.core import parse, execute, render

data = execute(parse("WITH source('data.csv') PLOT y AGAINST x"))
result = render(data)  # Uses default engine
```

### Direct Engine Usage

```python
from plotql.core import parse, execute, get_engine

query = parse("WITH source('data.csv') PLOT y AGAINST x")
data = execute(query)

engine = get_engine()
result = engine.render(data, width=800, height=600)
```

### Setting a Different Default

```python
from plotql.core import set_engine, MatplotlibEngine

custom = MatplotlibEngine()
set_engine(custom)

# All subsequent render() calls use this engine
```

## Output Options

All engines produce a `PlotResult` that provides multiple output formats:

```python
result = engine.render(data, width=800, height=600)

# File output
result.save("plot.png")
result.save("plot.svg")
result.save("plot.pdf")

# Bytes
png_bytes = result.to_bytes("png")

# PIL Image
image = result.to_image()

# Jupyter display
result.show()

# Underlying figure (for customization)
fig = result.figure
```

## Render Options

```python
# Standard dimensions
result = engine.render(data, width=800, height=600)

# High resolution
result = engine.render(data, width=1920, height=1080)

# Convenience method for PNG bytes
png_bytes = engine.render_to_bytes(data, width=800, height=600)

# With scale factor
png_bytes = engine.render_to_bytes(data, width=800, height=600, scale=2.0)
```

## Color Palette

The MatplotlibEngine uses theme-defined colors:

| Name | Used for |
|------|----------|
| `background` | Chart background |
| `text` | Labels and titles |
| `grid` | Grid lines |
| `axes` | Axis spines |
| `primary` | First series |
| `secondary` | Second series |
| `tertiary` | Third series |

User-facing color names (`red`, `blue`, etc.) are mapped to theme colors:

```python
engine = get_engine()

# Get a color from the theme
hex_color = engine.get_color("blue")  # Returns theme blue, e.g., "#89b4fa"
```

## Creating Custom Engines

Extend the `Engine` base class:

```python
from plotql.core.engines.base import Engine
from plotql.core.result import PlotResult

class CustomEngine(Engine):
    @property
    def COLORS(self):
        return {
            "background": "#ffffff",
            "text": "#000000",
            "primary": "#0066cc",
            # ...
        }

    def get_color(self, color_name):
        # Map user color names to hex values
        color_map = {"blue": "#0066cc", "red": "#cc0000"}
        return color_map.get(color_name, self.COLORS["primary"])

    def render(self, data, width, height):
        # Create your visualization
        figure = self._create_figure(data, width, height)

        return PlotResult(
            figure=figure,
            save_func=lambda f, path, fmt: ...,
            to_bytes_func=lambda f, fmt: ...,
            show_func=lambda f: ...,
            close_func=lambda f: ...,
        )
```

The `PlotResult` wrapper handles:
- Multiple output formats from a single render
- Jupyter integration (`_repr_png_`, `_repr_svg_`)
- Resource cleanup

## Terminal Rendering

The TUI uses matplotlib's Agg backend for non-interactive rendering, then displays via Sixel or other terminal image protocols.

For terminal pixel estimation:

```python
from plotql.core.engines import MatplotlibEngine

# Convert terminal character dimensions to pixels
width_px, height_px = MatplotlibEngine.get_terminal_pixel_size(
    char_width=80,
    char_height=24,
    cell_width_px=8,   # Default terminal cell width
    cell_height_px=16  # Default terminal cell height
)
```
