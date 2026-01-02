"""
State management for PlotQL UI.

Handles persisting UI state (like the last query) between sessions.
State is stored in the same directory as connector configs (~/.config/plotql/).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


# State file location (same directory as connectors.toml)
STATE_PATH = Path.home() / ".config" / "plotql" / "state.json"


def _ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    """
    Load application state from the state file.

    Returns:
        Parsed state dict. Empty dict if file doesn't exist.
    """
    if not STATE_PATH.exists():
        return {}

    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(state: dict) -> None:
    """
    Save application state to the state file.

    Args:
        state: State dict to save.
    """
    _ensure_config_dir()
    try:
        with open(STATE_PATH, "w") as f:
            json.dump(state, f, indent=2)
    except OSError:
        pass  # Silently fail if we can't write


def get_last_query() -> Optional[str]:
    """
    Get the last query from state.

    Returns:
        The last query string, or None if not found.
    """
    state = load_state()
    return state.get("last_query")


def save_last_query(query: str) -> None:
    """
    Save the current query to state.

    Args:
        query: The query string to save.
    """
    state = load_state()
    state["last_query"] = query
    save_state(state)
