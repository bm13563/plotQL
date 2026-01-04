# Connectors

Connectors abstract data loading from various sources. PlotQL includes connectors for files, directories, and databases.

## Overview

Data sources are specified in the `WITH` clause:

```sql
-- Literal file path
WITH 'data.csv' PLOT y AGAINST x

-- Named source from config
WITH source(trades) PLOT y AGAINST x

-- Database table
WITH source(my_db, trades) PLOT y AGAINST x

-- Folder path
WITH source(local_data, 2024, jan, trades.csv) PLOT y AGAINST x
```

## Configuration

Named sources are configured in `~/.config/plotql/sources.toml`:

```toml
# File alias
[trades]
type = "file"
path = "/data/trades.csv"

# Folder root
[local_data]
type = "folder"
path = "/data/market"

# ClickHouse database
[pump_fun]
type = "clickhouse"
host = "localhost"
port = 8123
database = "pump_fun"
limit = 10000
```

## Built-in Connectors

### Literal Connector

Direct file paths without configuration:

```sql
WITH 'path/to/file.csv' PLOT price AGAINST time
WITH '/absolute/path/data.parquet' PLOT price AGAINST time
```

Supported formats:
- CSV (`.csv`)
- Parquet (`.parquet`)
- JSON (`.json`)
- NDJSON (`.ndjson`)

### File Connector

Aliased file paths from config:

```toml
# sources.toml
[trades]
type = "file"
path = "/data/trades.csv"
```

```sql
WITH source(trades) PLOT price AGAINST time
```

### Folder Connector

Navigate directory structures with path segments:

```toml
# sources.toml
[local_data]
type = "folder"
path = "/data/market"
```

```sql
-- Single file
WITH source(local_data, trades.csv) PLOT price AGAINST time

-- Nested path
WITH source(local_data, 2024, jan, trades.csv) PLOT price AGAINST time
-- Resolves to: /data/market/2024/jan/trades.csv
```

Path segments are joined to form the full path. Supports the same file formats as the literal connector.

Security: Path traversal (e.g., `..`) is blocked — paths must stay within the configured root directory.

### ClickHouse Connector

Query ClickHouse databases:

```toml
# sources.toml
[pump_fun]
type = "clickhouse"
host = "localhost"
port = 8123          # Optional, default: 8123
username = "user"    # Optional
password = "pass"    # Optional
database = "pump_fun"
limit = 10000        # Optional row limit, default: 10000
```

```sql
WITH source(pump_fun, trades) PLOT price AGAINST time
```

The second argument is the table name.

#### Installation

ClickHouse support requires an extra dependency:

```bash
pip install plotql[clickhouse]
# or
pip install clickhouse-connect
```

#### Filter Pushdown

The ClickHouse connector pushes `FILTER` clauses to SQL for efficient querying:

```sql
WITH source(pump_fun, trades)
PLOT price AGAINST time
FILTER symbol = 'AAPL' AND volume > 1000
```

Generates SQL:
```sql
SELECT * FROM trades WHERE symbol = 'AAPL' AND volume > 1000 LIMIT 10000
```

This minimizes data transfer by filtering at the database level.

## How Connectors Work

1. **Literal paths** (quoted strings): Routed to LiteralConnector
2. **Single argument** `source(alias)`: Looks up config, routes based on `type`
3. **Multiple arguments** `source(alias, ...)`:
   - For `clickhouse`: Second arg is table name
   - For `folder`: Remaining args are path segments

## Error Handling

```python
from plotql.core.connectors.base import ConfigError, ConnectionError, ConnectorError

try:
    data = execute(query)
except ConfigError as e:
    # Missing or invalid configuration
    print(f"Config error: {e}")
except ConnectionError as e:
    # Failed to connect to data source
    print(f"Connection error: {e}")
except ConnectorError as e:
    # Other connector issues (file not found, etc.)
    print(f"Connector error: {e}")
```

## Adding Custom Connectors

Extend the `Connector` base class:

```python
from plotql.core.connectors.base import Connector, ConfigError
import polars as pl

class MyConnector(Connector):
    def validate_config(self, config: dict) -> None:
        if "url" not in config:
            raise ConfigError("MyConnector requires 'url' in config")

    def load(self, config: dict, filters=None) -> pl.DataFrame:
        # Load data and return a Polars DataFrame
        url = config["url"]
        # ... fetch and process data ...
        return pl.DataFrame(data)
```

Connectors must:
- Implement `validate_config()` to check required configuration
- Implement `load()` to return a Polars DataFrame
- Optionally set `supports_filter_pushdown = True` and handle the `filters` parameter
