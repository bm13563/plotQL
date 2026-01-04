# Terminal UI

PlotQL includes an interactive terminal interface built with [Textual](https://textual.textualize.io/). It provides a harlequin-inspired experience for writing and executing queries.

## Features

- **Multi-line query editor** with syntax highlighting
- **Live plot preview** using Sixel rendering
- **Autocomplete** for keywords, functions, and column names
- **Query persistence** between sessions
- **Connector configuration** editor

## Launching

```bash
# Interactive mode
plotql

# Execute a query directly
plotql -c "WITH source('data.csv') PLOT price AGAINST time"

# Run a .pql file
plotql query.pql

# Save output
plotql -c "..." -o chart.png
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F5` | Execute query |
| `F2` | Open connector config editor |
| `Ctrl+Q` | Quit |
| `Ctrl+Space` | Trigger autocomplete |
| `Tab` | Accept autocomplete suggestion |
| `Escape` | Dismiss autocomplete popup |
| `Ctrl+A` | Select all text |

## Interface Layout

```
┌─────────────────────────────────────┐
│ Header                              │
├─────────────────────────────────────┤
│                                     │
│ Query Editor (30%)                  │
│                                     │
├─────────────────────────────────────┤
│                                     │
│                                     │
│ Plot Preview (remaining space)      │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ Status Bar                          │
├─────────────────────────────────────┤
│ Footer (keybindings)                │
└─────────────────────────────────────┘
```

## Query Editor

The editor supports:
- PlotQL syntax highlighting via tree-sitter
- Auto-indentation (2 spaces)
- Autocomplete triggered by typing

### Autocomplete

Completions appear as you type:
- **Keywords**: `WITH`, `PLOT`, `AGAINST`, `AS`, `FILTER`, `FORMAT`, `AND`, `OR`
- **Functions**: `count`, `sum`, `avg`, `min`, `max`, `median`
- **Plot types**: `scatter`, `line`, `bar`, `hist`
- **Column names**: Loaded from the data source after `PLOT` or `FILTER`

Use `Tab` to accept a suggestion, `Up`/`Down` to navigate, `Escape` to dismiss.

## Plot Preview

Plots render using Sixel graphics for high-quality terminal display. Supported in:
- VS Code terminal
- iTerm2
- WezTerm
- Kitty
- mlterm

The plot auto-sizes to fill available space.

## Status Bar

Shows query status:
- **Ready**: Waiting for query
- **OK**: Successful execution with row counts
- **Error**: Parse or execution errors (truncated if long)

## Connector Configuration

Press `F2` to open the connector config editor. This edits `~/.config/plotql/sources.toml`.

Example configuration:

```toml
[trades]
type = "file"
path = "/data/trades.csv"

[local_data]
type = "folder"
path = "/data/market"

[my_database]
type = "clickhouse"
host = "localhost"
database = "analytics"
```

See [Connectors](connectors.md) for detailed configuration options.

## Session Persistence

The TUI automatically saves your query when you quit and restores it on next launch. State is stored in `~/.config/plotql/state.json`.

## Logging

Debug logs are written to `plotql.log` in the current directory. Useful for troubleshooting rendering or autocomplete issues.

## Theme

The TUI uses a dark vaporwave-inspired theme with:
- Dark background (`#0a0a0f`)
- Soft pastel syntax colors
- High contrast for readability

The theme is defined in `plotql/themes/` and applied consistently across the editor, plot rendering, and UI elements.
