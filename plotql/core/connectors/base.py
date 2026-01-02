"""
Base connector interface for PlotQL data sources.

Connectors abstract data loading from various sources (files, databases, etc.)
into a common interface that returns Polars DataFrames.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

import polars as pl

if TYPE_CHECKING:
    from plotql.core.ast import WhereClause


class ConnectorError(Exception):
    """Base exception for connector-related errors."""
    pass


class ConfigError(ConnectorError):
    """Raised when connector configuration is invalid or missing."""
    pass


class ConnectionError(ConnectorError):
    """Raised when connection to a data source fails."""
    pass


class Connector(ABC):
    """
    Abstract base class for data connectors.

    Each connector implementation knows how to load data from a specific
    source type (files, databases, APIs, etc.) and return a Polars DataFrame.
    """

    # Whether this connector supports filter pushdown
    supports_filter_pushdown: bool = False

    @abstractmethod
    def load(
        self,
        config: dict,
        filters: Optional[List["WhereClause"]] = None,
    ) -> pl.DataFrame:
        """
        Load data from the source and return a DataFrame.

        Args:
            config: Configuration dict with source-specific parameters.
                   For file connectors: {"path": "/path/to/file.csv"}
                   For database connectors: {"host": "...", "query": "...", etc.}
            filters: Optional list of WhereClause filters to push down.
                     Only used if supports_filter_pushdown is True.
                     The connector is responsible for combining them (typically OR).

        Returns:
            A Polars DataFrame containing the loaded data.

        Raises:
            ConfigError: If required configuration is missing or invalid.
            ConnectionError: If connection to the source fails.
            ConnectorError: For other connector-related errors.
        """
        pass

    @abstractmethod
    def validate_config(self, config: dict) -> None:
        """
        Validate connector configuration.

        Args:
            config: Configuration dict to validate.

        Raises:
            ConfigError: If configuration is invalid.
        """
        pass
