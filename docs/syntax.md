# PlotQL Syntax & Python API

PlotQL is a declarative query language for creating plots. This document covers the complete language syntax and Python API.

## Query Structure

A PlotQL query follows this structure:

```
WITH <source>
PLOT <y_column> AGAINST <x_column> [AS <plot_type>]
[FILTER <conditions>]
[FORMAT <options>]
```

Multiple `PLOT` clauses can be added to layer series on the same chart.

## Data Sources

### Literal File Paths

Reference files directly with quoted strings inside `source()`:

```sql
WITH source('data.csv') PLOT price AGAINST time
WITH source('/path/to/trades.parquet') PLOT volume AGAINST timestamp
```

Supported formats: CSV, Parquet, JSON, NDJSON

### Named Sources

Use configured aliases from `~/.config/plotql/sources.toml`:

```sql
WITH source(trades) PLOT price AGAINST time
```

See [Connectors](connectors.md) for configuration details.

### Database Sources

Query database tables:

```sql
WITH source(my_database, trades) PLOT price AGAINST time
```

### Folder Sources

Navigate directory structures:

```sql
WITH source(local_data, 2024, jan, trades.csv) PLOT price AGAINST time
```

## Plot Types

Specify with `AS '<type>'`:

| Type | Description |
|------|-------------|
| `'scatter'` | Scatter plot (default) |
| `'line'` | Line chart |
| `'bar'` | Bar chart |
| `'hist'` | Histogram |

```sql
WITH source('data.csv') PLOT price AGAINST time AS 'line'
WITH source('data.csv') PLOT count AGAINST category AS 'bar'
```

## Columns

### Simple Columns

Reference columns by name:

```sql
PLOT price AGAINST time
PLOT close_price AGAINST trade_date
```

### Aggregations

Apply aggregate functions:

| Function | Description |
|----------|-------------|
| `count(col)` | Count of values |
| `sum(col)` | Sum of values |
| `avg(col)` | Average |
| `min(col)` | Minimum |
| `max(col)` | Maximum |
| `median(col)` | Median |

```sql
-- Total sales per region
WITH source('orders.csv') PLOT sum(amount) AGAINST region AS 'bar'

-- Average price over time
WITH source('stocks.csv') PLOT avg(price) AGAINST date AS 'line'

-- Count events per hour
WITH source('logs.csv') PLOT count(event) AGAINST hour AS 'bar'
```

When using aggregations, data is automatically grouped by the non-aggregated column.

## Filtering

Use `FILTER` to subset data:

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `<=` | Less or equal |
| `>` | Greater than |
| `>=` | Greater or equal |

### Logical Operators

Combine conditions with `AND` and `OR`:

```sql
-- Single condition
WITH source('trades.csv') PLOT price AGAINST time
FILTER symbol = 'AAPL'

-- Multiple conditions with AND
WITH source('trades.csv') PLOT price AGAINST time
FILTER symbol = 'AAPL' AND volume > 1000

-- OR conditions
WITH source('sensors.csv') PLOT temperature AGAINST time
FILTER location = 'warehouse' OR location = 'office'

-- Complex combinations
WITH source('trades.csv') PLOT price AGAINST time
FILTER symbol = 'AAPL' AND volume > 1000 OR symbol = 'GOOGL'
```

### Value Types

- Strings: `'quoted'` or `"double-quoted"`
- Numbers: `100`, `-50`, `3.14`
- NULL: `NULL`

## Formatting

Use `FORMAT` to customize appearance:

### Chart Labels

```sql
WITH source('data.csv') PLOT price AGAINST time
FORMAT title = 'Price Over Time' AND xlabel = 'Date' AND ylabel = 'USD'
```

| Option | Description |
|--------|-------------|
| `title` | Chart title |
| `xlabel` | X-axis label |
| `ylabel` | Y-axis label |

### Colors

```sql
-- Line color
WITH source('data.csv') PLOT price AGAINST time AS 'line'
FORMAT line_color = 'red'

-- Marker color for scatter
WITH source('data.csv') PLOT price AGAINST time AS 'scatter'
FORMAT marker_color = 'blue'
```

Available colors: `red`, `blue`, `green`, `yellow`, `purple`, `cyan`, `orange`, `pink`, `white`

### Dynamic Formatting

Map visual properties to column values:

```sql
-- Color by category (categorical)
WITH source('data.csv') PLOT price AGAINST time AS 'scatter'
FORMAT marker_color = category

-- Size by value (continuous)
WITH source('data.csv') PLOT price AGAINST time AS 'scatter'
FORMAT marker_size = volume

-- Both color and size
WITH source('data.csv') PLOT price AGAINST time AS 'scatter'
FORMAT marker_color = sector AND marker_size = market_cap
```

When mapping to columns:
- **Categorical columns**: Each unique value gets a distinct color
- **Numeric columns**: Values are mapped to a gradient (colors) or size range (1-5)

### All Format Options

| Option | Values | Applies to |
|--------|--------|------------|
| `title` | String | All |
| `xlabel` | String | All |
| `ylabel` | String | All |
| `line_color` | Color name or column | Line |
| `marker_color` | Color name or column | Scatter |
| `marker_size` | 1-5 or column | Scatter |
| `marker` | `default`, `NULL` | Line (show/hide markers) |
| `line_style` | `solid`, `dashed`, `dotted` | Line |

## Multiple Series

Layer multiple plots on the same chart:

```sql
-- Overlay filtered subset
WITH source('trades.csv')
PLOT price AGAINST time
PLOT price AGAINST time
    FILTER user_id = 'vip'
    FORMAT marker_size = 5 AND marker_color = 'red'

-- Compare metrics
WITH source('stocks.csv')
PLOT open AGAINST date AS 'line'
PLOT close AGAINST date AS 'line'
    FORMAT line_color = 'red'
```

Later series render on top of earlier ones. Each `PLOT` clause can have its own `FILTER` and `FORMAT`.

---

# Python API

## Basic Usage

```python
from plotql.core import parse, execute, render

# Parse a query string into an AST
query = parse("WITH source('data.csv') PLOT price AGAINST time")

# Execute the query to get plot data
data = execute(query)

# Render to a PlotResult
result = render(data)
```

## PlotResult

The `render()` function returns a `PlotResult` with multiple output options:

```python
result = render(data)

# Save to file (format inferred from extension)
result.save("plot.png")
result.save("plot.svg")
result.save("plot.pdf")

# Get raw bytes
png_bytes = result.to_bytes("png")
svg_bytes = result.to_bytes("svg")

# Convert to PIL Image
image = result.to_image()

# Display in Jupyter (automatic via _repr_png_)
result.show()

# Access underlying matplotlib figure for customization
fig = result.figure
fig.axes[0].set_xlim(0, 100)
result.save("customized.png")

# Free resources when done
result.close()
```

### Jupyter Integration

PlotResult automatically displays in Jupyter notebooks:

```python
from plotql.core import parse, execute, render

# Just return the result - displays inline
render(execute(parse("WITH source('data.csv') PLOT y AGAINST x")))
```

## Render Options

```python
# Custom dimensions (default: 800x600)
result = render(data, width=1200, height=800)
```

## Engine Management

```python
from plotql.core import get_engine, set_engine, MatplotlibEngine

# Get current engine
engine = get_engine()

# Create custom engine instance
custom_engine = MatplotlibEngine()

# Set as default
set_engine(custom_engine)

# Render directly with engine
result = engine.render(data, width=800, height=600)
```

## Error Handling

```python
from plotql.core import parse, execute, ParseError, ExecutionError

try:
    query = parse("INVALID QUERY")
except ParseError as e:
    print(f"Syntax error: {e}")

try:
    data = execute(query)
except ExecutionError as e:
    print(f"Execution error: {e}")
```

## AST Types

For programmatic query construction:

```python
from plotql.core import (
    PlotQuery,
    PlotType,
    ColumnRef,
    AggregateFunc,
    WhereClause,
    Condition,
    ComparisonOp,
    LogicalOp,
    FormatOptions,
)
from plotql.core.ast import SourceRef, PlotSeries

# Build a query programmatically
query = PlotQuery(
    source=SourceRef(args=["data.csv"], is_literal=True),
    series=[
        PlotSeries(
            x_column=ColumnRef(name="time"),
            y_column=ColumnRef(name="price", aggregate=AggregateFunc.AVG),
            plot_type=PlotType.LINE,
            filter=WhereClause(
                conditions=[Condition("symbol", ComparisonOp.EQ, "AAPL")],
                operators=[]
            ),
            format=FormatOptions(title="Average AAPL Price")
        )
    ]
)

data = execute(query)
result = render(data)
```

## Complete Example

```python
from plotql.core import parse, execute, render

# Multi-series plot with filtering and formatting
query = parse("""
    WITH source('trades.csv')
    PLOT price AGAINST timestamp AS 'scatter'
    PLOT price AGAINST timestamp AS 'scatter'
        FILTER symbol = 'AAPL'
        FORMAT marker_color = 'red' AND marker_size = 4
""")

data = execute(query)
result = render(data, width=1000, height=600)

# Customize and save
result.figure.suptitle("Trade Prices", fontsize=14)
result.save("trades.png")
result.close()
```
