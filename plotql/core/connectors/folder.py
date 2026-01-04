"""
Folder connector for PlotQL.

Handles directory-based file paths: WITH source(local_data, subdir, file.csv)
Config defines root directory, query args define path segments.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

import polars as pl

from plotql.core.connectors.base import Connector, ConfigError, ConnectorError

if TYPE_CHECKING:
    from plotql.core.ast import WhereClause


class FolderConnector(Connector):
    """
    Connector for directory-based file access.

    Used when a source with type="folder" is specified:
        WITH source(local_data, trades.csv)
        WITH source(local_data, 2024, jan, trades.csv)

    Where local_data is configured in sources.toml as:
        [local_data]
        type = "folder"
        path = "/data/market"

    The path segments after the alias are joined to form the full file path:
        /data/market/trades.csv
        /data/market/2024/jan/trades.csv
    """

    def validate_config(self, config: dict) -> None:
        """Validate that path and file segments are provided."""
        if "path" not in config:
            raise ConfigError(
                "FolderConnector requires 'path' in config. "
                "Add path = '/path/to/directory' to your connector config."
            )
        if "segments" not in config or not config["segments"]:
            raise ConfigError(
                "FolderConnector requires path segments in query. "
                "Use source(alias, file.csv) or source(alias, subdir, file.csv)"
            )

    def load(
        self,
        config: dict,
        filters: Optional[List["WhereClause"]] = None,
    ) -> pl.DataFrame:
        """
        Load data from a file within a configured directory.

        Args:
            config: Must contain:
                - path: Root directory path from config
                - segments: List of path segments (subdirs + filename) from query

        Returns:
            Polars DataFrame with loaded data.

        Raises:
            ConfigError: If path or segments are missing.
            ConnectorError: If file doesn't exist or can't be loaded.
        """
        self.validate_config(config)

        root = Path(config["path"])
        segments = config["segments"]

        # Join all segments to form the full path
        full_path = root.joinpath(*segments)

        if not full_path.exists():
            raise ConnectorError(f"File not found: {full_path}")

        # Ensure the resolved path is within the root (security)
        try:
            full_path.resolve().relative_to(root.resolve())
        except ValueError:
            raise ConnectorError(
                f"Path traversal not allowed: {'/'.join(segments)} "
                f"escapes root directory {root}"
            )

        suffix = full_path.suffix.lower()

        try:
            if suffix == ".csv":
                return pl.read_csv(full_path)
            elif suffix == ".parquet":
                return pl.read_parquet(full_path)
            elif suffix == ".json":
                return pl.read_json(full_path)
            elif suffix == ".ndjson":
                return pl.read_ndjson(full_path)
            else:
                # Try CSV as default
                return pl.read_csv(full_path)
        except Exception as e:
            raise ConnectorError(f"Failed to load {full_path}: {e}")
