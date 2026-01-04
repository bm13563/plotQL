# PlotQL

A SQL-like query language for creating plots. No Python boilerplate, no remembering matplotlib syntax — just describe what you want to plot.

![PlotQL TUI](examples/tui_screenshot.png)

## Why PlotQL?

Data visualization shouldn't require hunting through documentation or writing boilerplate. PlotQL lets you express plots declaratively:

```sql
WITH 'trades.csv' PLOT price AGAINST time AS line
FILTER symbol = 'AAPL' AND volume > 1000
FORMAT title = 'AAPL Price'
```

### Design Philosophy

**The core library is completely independent of any UI.** PlotQL's parsing and rendering engine is a standalone Python library that can be embedded anywhere:

- **Scripts** — parse queries and save plots programmatically
- **Jupyter notebooks** — inline display with `result.show()`
- **Web applications** — render to bytes and serve
- **The included TUI** — interactive terminal interface (just one possible frontend)

This separation means you can use PlotQL's query language in whatever context makes sense for your workflow.

## Quick Example

```python
from plotql.core import parse, execute, render

query = parse("WITH 'data.csv' PLOT revenue AGAINST month AS bar")
data = execute(query)
result = render(data)

result.save("chart.png")     # Save to file
result.show()                # Display in Jupyter
result.figure                # Access matplotlib figure for customization
```

## Installation

```bash
# Clone and setup (requires uv)
git clone https://github.com/your-username/plotql.git
cd plotql
./ctl.sh setup

# Activate environment
source .venv/bin/activate

# Run the TUI
plotql
```

If you don't have `uv`, install it from [astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

## Documentation

- **[Syntax & Python API](docs/syntax.md)** — Full language reference, operators, aggregations, and Python usage
- **[Connectors](docs/connectors.md)** — Data sources: files, folders, ClickHouse databases
- **[Engines](docs/engines.md)** — Rendering backends and customization
- **[TUI](docs/ui.md)** — Interactive terminal interface

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:

- Development setup
- Architecture overview (core/engines/connectors/UI separation)
- Theme system
- Tree-sitter grammar workflow
- Feature checklist

## License

MIT
