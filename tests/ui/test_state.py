"""Tests for state management."""

import json
import pytest

from plotql.ui.state import (
    load_state,
    save_state,
    get_last_query,
    save_last_query,
)


@pytest.fixture
def temp_state_file(tmp_path, monkeypatch):
    """Use a temporary state file for testing."""
    state_file = tmp_path / "state.json"
    monkeypatch.setattr("plotql.ui.state.STATE_PATH", state_file)
    return state_file


class TestLoadState:
    def test_returns_empty_dict_when_file_missing(self, temp_state_file):
        assert load_state() == {}

    def test_loads_valid_json(self, temp_state_file):
        temp_state_file.write_text('{"key": "value"}')
        assert load_state() == {"key": "value"}

    def test_returns_empty_dict_on_invalid_json(self, temp_state_file):
        temp_state_file.write_text("not valid json")
        assert load_state() == {}


class TestSaveState:
    def test_saves_state(self, temp_state_file):
        save_state({"test": "data"})
        assert temp_state_file.exists()
        assert json.loads(temp_state_file.read_text()) == {"test": "data"}

    def test_creates_directory(self, tmp_path, monkeypatch):
        state_file = tmp_path / "subdir" / "state.json"
        monkeypatch.setattr("plotql.ui.state.STATE_PATH", state_file)
        save_state({"test": "data"})
        assert state_file.exists()


class TestGetLastQuery:
    def test_returns_none_when_no_state(self, temp_state_file):
        assert get_last_query() is None

    def test_returns_none_when_no_query_key(self, temp_state_file):
        temp_state_file.write_text('{"other": "data"}')
        assert get_last_query() is None

    def test_returns_saved_query(self, temp_state_file):
        query = "WITH source('test.csv') PLOT x AGAINST y"
        temp_state_file.write_text(json.dumps({"last_query": query}))
        assert get_last_query() == query


class TestSaveLastQuery:
    def test_saves_query(self, temp_state_file):
        save_last_query("WITH source('data.csv') PLOT a AGAINST b")
        state = json.loads(temp_state_file.read_text())
        assert state["last_query"] == "WITH source('data.csv') PLOT a AGAINST b"

    def test_preserves_other_state(self, temp_state_file):
        temp_state_file.write_text('{"other": "data"}')
        save_last_query("new query")
        state = json.loads(temp_state_file.read_text())
        assert state["other"] == "data"
        assert state["last_query"] == "new query"
