"""
Configuration management for PlotQL sources.

Handles loading and parsing the sources.toml config file.

Config format:
    [trades]
    type = "file"
    path = "/data/trades.csv"

    [local_data]
    type = "folder"
    path = "/data/market"

    [pump_fun]
    type = "clickhouse"
    host = "localhost"
    port = 8123
    database = "pump_fun"
    limit = 10000

Usage:
    WITH source(trades) PLOT ...              # file type
    WITH source(local_data, trades.csv) PLOT ...  # folder type
    WITH source(local_data, 2024, jan, trades.csv) PLOT ...  # folder with subdirs
    WITH source(pump_fun, trades) PLOT ...    # clickhouse type
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from plotql.core.connectors.base import ConfigError


# Default config file location
CONFIG_PATH = Path.home() / ".config" / "plotql" / "sources.toml"


@dataclass
class SourceConfig:
    """Resolved configuration for a source."""
    type: str  # "file" or "clickhouse"
    config: dict  # The raw config dict


def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load and parse the sources config file.

    Args:
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        Parsed config dict. Empty dict if file doesn't exist.

    Raises:
        ConfigError: If config file exists but cannot be parsed.
    """
    path = config_path or CONFIG_PATH

    if not path.exists():
        return {}

    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Invalid TOML in config file {path}: {e}")


def get_source_config(
    alias: str,
    config_path: Optional[Path] = None
) -> SourceConfig:
    """
    Get configuration for a source alias.

    Args:
        alias: The source alias name defined in config
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        SourceConfig with type and config dict.

    Raises:
        ConfigError: If alias is not found or has no type.
    """
    config = load_config(config_path)

    if alias not in config:
        available = list(config.keys())
        raise ConfigError(
            f"Source '{alias}' not found in config. "
            f"Available: {', '.join(available) if available else 'none'}. "
            f"Add [{alias}] section to {config_path or CONFIG_PATH}"
        )

    source_config = config[alias]

    if "type" not in source_config:
        raise ConfigError(
            f"Source '{alias}' has no 'type' field. "
            f"Add type = 'file' or type = 'clickhouse' to [{alias}] section."
        )

    return SourceConfig(
        type=source_config["type"],
        config=source_config,
    )


def list_sources(config_path: Optional[Path] = None) -> list[str]:
    """
    List all configured source aliases.

    Args:
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        List of source alias names.
    """
    config = load_config(config_path)
    return [k for k, v in config.items() if isinstance(v, dict)]


def list_sources_by_type(config_path: Optional[Path] = None) -> dict[str, list[str]]:
    """
    List all configured sources grouped by type.

    Args:
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        Dict mapping source types to lists of alias names.
    """
    config = load_config(config_path)
    result: dict[str, list[str]] = {}

    for alias, source_config in config.items():
        if isinstance(source_config, dict) and "type" in source_config:
            source_type = source_config["type"]
            if source_type not in result:
                result[source_type] = []
            result[source_type].append(alias)

    return result


# Backward compatibility aliases
def get_connector_config(
    connector_type: str,
    alias: str,
    config_path: Optional[Path] = None
) -> dict:
    """Deprecated: Use get_source_config instead."""
    # Try old-style config first for backward compat
    config = load_config(config_path)

    # Old style: [clickhouse.pft]
    if connector_type in config and alias in config[connector_type]:
        return config[connector_type][alias]

    # New style: [pft] with type = "clickhouse"
    if alias in config:
        source_config = config[alias]
        if source_config.get("type") == connector_type:
            return source_config

    raise ConfigError(
        f"Alias '{alias}' not found for connector '{connector_type}'."
    )


def list_aliases(
    connector_type: str,
    config_path: Optional[Path] = None
) -> list[str]:
    """Deprecated: Use list_sources_by_type instead."""
    by_type = list_sources_by_type(config_path)
    return by_type.get(connector_type, [])


def list_all_aliases(config_path: Optional[Path] = None) -> dict[str, list[str]]:
    """Deprecated: Use list_sources_by_type instead."""
    return list_sources_by_type(config_path)
