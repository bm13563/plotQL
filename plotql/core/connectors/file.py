"""
File connector for PlotQL.

Handles aliased file paths: WITH file(trades)
Looks up the actual path from the config file.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

import polars as pl

from plotql.core.connectors.base import Connector, ConfigError, ConnectorError

if TYPE_CHECKING:
    from plotql.core.ast import WhereClause


class FileConnector(Connector):
    """
    Connector for aliased file paths.

    Used when file() function is specified in WITH clause (e.g., WITH file(trades)).
    Looks up the actual file path from the connectors.toml config.
    """

    def validate_config(self, config: dict) -> None:
        """Validate that path is provided in config."""
        if "path" not in config:
            raise ConfigError(
                "FileConnector requires 'path' in config. "
                "Add path = '/path/to/file.csv' to your connector config."
            )

    def load(
        self,
        config: dict,
        filters: Optional[List["WhereClause"]] = None,
    ) -> pl.DataFrame:
        """
        Load data from an aliased file path.

        Args:
            config: Must contain "path" key from config lookup.

        Returns:
            Polars DataFrame with loaded data.

        Raises:
            ConfigError: If path is missing from config.
            ConnectorError: If file doesn't exist or can't be loaded.
        """
        self.validate_config(config)

        path = config["path"]
        p = Path(path)

        if not p.exists():
            raise ConnectorError(f"File not found: {path}")

        suffix = p.suffix.lower()

        try:
            if suffix == ".csv":
                return pl.read_csv(path)
            elif suffix == ".parquet":
                return pl.read_parquet(path)
            elif suffix == ".json":
                return pl.read_json(path)
            elif suffix == ".ndjson":
                return pl.read_ndjson(path)
            else:
                # Try CSV as default
                return pl.read_csv(path)
        except Exception as e:
            raise ConnectorError(f"Failed to load {path}: {e}")
