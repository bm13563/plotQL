"""
Configuration management for PlotQL connectors.

Handles loading and parsing the connectors.toml config file.
"""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Optional

from plotql.core.connectors.base import ConfigError


# Default config file location
CONFIG_PATH = Path.home() / ".config" / "plotql" / "connectors.toml"


def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load and parse the connectors config file.

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


def get_connector_config(
    connector_type: str,
    alias: str,
    config_path: Optional[Path] = None
) -> dict:
    """
    Get configuration for a specific connector and alias.

    Args:
        connector_type: The connector type (e.g., "file", "clickhouse")
        alias: The alias name defined in config
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        Configuration dict for the specified connector/alias.

    Raises:
        ConfigError: If connector type or alias is not found in config.
    """
    config = load_config(config_path)

    if connector_type not in config:
        raise ConfigError(
            f"No '{connector_type}' connectors configured. "
            f"Add [{connector_type}.{alias}] section to {config_path or CONFIG_PATH}"
        )

    connector_configs = config[connector_type]

    if alias not in connector_configs:
        available = list(connector_configs.keys())
        raise ConfigError(
            f"Alias '{alias}' not found for connector '{connector_type}'. "
            f"Available: {', '.join(available) if available else 'none'}"
        )

    return connector_configs[alias]


def list_aliases(
    connector_type: str,
    config_path: Optional[Path] = None
) -> list[str]:
    """
    List all configured aliases for a connector type.

    Args:
        connector_type: The connector type (e.g., "file", "clickhouse")
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        List of alias names. Empty list if connector type not configured.
    """
    config = load_config(config_path)

    if connector_type not in config:
        return []

    return list(config[connector_type].keys())


def list_all_aliases(config_path: Optional[Path] = None) -> dict[str, list[str]]:
    """
    List all configured aliases grouped by connector type.

    Args:
        config_path: Path to config file. Uses CONFIG_PATH if not specified.

    Returns:
        Dict mapping connector types to lists of alias names.
    """
    config = load_config(config_path)
    result = {}

    for connector_type, aliases in config.items():
        if isinstance(aliases, dict):
            result[connector_type] = list(aliases.keys())

    return result
