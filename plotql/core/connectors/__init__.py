"""
PlotQL Connectors - Data source abstractions.

Connectors load data from various sources into Polars DataFrames.
"""
from __future__ import annotations

from typing import Type

from plotql.core.connectors.base import (
    Connector,
    ConnectorError,
    ConfigError,
    ConnectionError,
)
from plotql.core.connectors.literal import LiteralConnector
from plotql.core.connectors.file import FileConnector
from plotql.core.connectors.clickhouse import ClickHouseConnector


# Registry of available connector types
CONNECTORS: dict[str, Type[Connector]] = {
    "file": FileConnector,
    "clickhouse": ClickHouseConnector,
}


def get_connector(connector_type: str) -> Connector:
    """
    Get a connector instance by type name.

    Args:
        connector_type: The connector type (e.g., "file", "clickhouse")

    Returns:
        A new instance of the requested connector.

    Raises:
        ConfigError: If connector type is unknown.
    """
    if connector_type not in CONNECTORS:
        available = ", ".join(CONNECTORS.keys())
        raise ConfigError(
            f"Unknown connector type: '{connector_type}'. "
            f"Available: {available}"
        )

    return CONNECTORS[connector_type]()


__all__ = [
    # Base classes
    "Connector",
    "ConnectorError",
    "ConfigError",
    "ConnectionError",
    # Implementations
    "LiteralConnector",
    "FileConnector",
    "ClickHouseConnector",
    # Registry
    "CONNECTORS",
    "get_connector",
]
