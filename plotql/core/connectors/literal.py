"""
Literal file connector for PlotQL.

Handles raw file paths (the default case): WITH 'path/to/file.csv'
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

import polars as pl

from plotql.core.connectors.base import Connector, ConfigError, ConnectorError

if TYPE_CHECKING:
    from plotql.core.ast import WhereClause


class LiteralConnector(Connector):
    """
    Connector for literal file paths.

    This is the default connector used when a raw file path is specified
    in the WITH clause (e.g., WITH 'data.csv').
    """

    def validate_config(self, config: dict) -> None:
        """Validate that path is provided."""
        if "path" not in config:
            raise ConfigError("LiteralConnector requires 'path' in config")

    def load(
        self,
        config: dict,
        filters: Optional[List["WhereClause"]] = None,
    ) -> pl.DataFrame:
        """
        Load data from a file path.

        Args:
            config: Must contain "path" key with file path.

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
