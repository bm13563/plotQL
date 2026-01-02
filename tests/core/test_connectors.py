"""
Unit tests for PlotQL connectors.

Tests connector base class, config loading, and connector implementations.
"""
import polars as pl
import pytest

from plotql.core.config import (
    ConfigError,
    get_connector_config,
    list_aliases,
    list_all_aliases,
    load_config,
)
from plotql.core.connectors import (
    CONNECTORS,
    ConnectorError,
    FileConnector,
    LiteralConnector,
    get_connector,
)
from plotql.core.ast import ConnectorSource, LiteralSource
from plotql.core.parser import parse


# =============================================================================
# Config Tests
# =============================================================================


class TestLoadConfig:
    """Tests for config loading."""

    def test_load_nonexistent_config(self, monkeypatch, tmp_path):
        """Test loading when config file doesn't exist."""
        fake_path = tmp_path / "nonexistent" / "connectors.toml"
        monkeypatch.setattr("plotql.core.config.CONFIG_PATH", fake_path)

        config = load_config()
        assert config == {}

    def test_load_valid_config(self, monkeypatch, tmp_path):
        """Test loading a valid config file."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("""
[file.trades]
path = "/data/trades.csv"

[clickhouse.production]
host = "localhost"
port = 8123
query = "SELECT * FROM trades"
""")
        config = load_config(config_path)

        assert "file" in config
        assert "trades" in config["file"]
        assert config["file"]["trades"]["path"] == "/data/trades.csv"

        assert "clickhouse" in config
        assert "production" in config["clickhouse"]
        assert config["clickhouse"]["production"]["host"] == "localhost"

    def test_load_invalid_toml(self, tmp_path):
        """Test loading invalid TOML raises error."""
        config_path = tmp_path / "bad.toml"
        config_path.write_text("this is not valid toml [[[")

        with pytest.raises(ConfigError) as exc_info:
            load_config(config_path)
        assert "Invalid TOML" in str(exc_info.value)


class TestGetConnectorConfig:
    """Tests for get_connector_config."""

    def test_get_existing_config(self, tmp_path):
        """Test getting config for existing connector/alias."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("""
[file.trades]
path = "/data/trades.csv"
""")
        config = get_connector_config("file", "trades", config_path)
        assert config["path"] == "/data/trades.csv"

    def test_get_missing_connector_type(self, tmp_path):
        """Test error when connector type not configured."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("[file.trades]\npath = '/data/trades.csv'")

        with pytest.raises(ConfigError) as exc_info:
            get_connector_config("clickhouse", "trades", config_path)
        assert "clickhouse" in str(exc_info.value).lower()

    def test_get_missing_alias(self, tmp_path):
        """Test error when alias not found."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("[file.trades]\npath = '/data/trades.csv'")

        with pytest.raises(ConfigError) as exc_info:
            get_connector_config("file", "unknown", config_path)
        assert "unknown" in str(exc_info.value)


class TestListAliases:
    """Tests for list_aliases."""

    def test_list_existing_aliases(self, tmp_path):
        """Test listing aliases for connector type."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("""
[file.trades]
path = "/data/trades.csv"

[file.orders]
path = "/data/orders.csv"
""")
        aliases = list_aliases("file", config_path)
        assert set(aliases) == {"trades", "orders"}

    def test_list_empty_aliases(self, tmp_path):
        """Test listing aliases when none configured."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("[file.trades]\npath = '/data/trades.csv'")

        aliases = list_aliases("clickhouse", config_path)
        assert aliases == []


class TestListAllAliases:
    """Tests for list_all_aliases."""

    def test_list_all(self, tmp_path):
        """Test listing all aliases grouped by connector."""
        config_path = tmp_path / "connectors.toml"
        config_path.write_text("""
[file.trades]
path = "/data/trades.csv"

[clickhouse.production]
host = "localhost"
query = "SELECT 1"
""")
        all_aliases = list_all_aliases(config_path)
        assert "file" in all_aliases
        assert "trades" in all_aliases["file"]
        assert "clickhouse" in all_aliases
        assert "production" in all_aliases["clickhouse"]


# =============================================================================
# Connector Registry Tests
# =============================================================================


class TestConnectorRegistry:
    """Tests for connector registry."""

    def test_registry_has_file(self):
        """Test file connector is registered."""
        assert "file" in CONNECTORS
        assert CONNECTORS["file"] == FileConnector

    def test_registry_has_clickhouse(self):
        """Test clickhouse connector is registered."""
        from plotql.core.connectors.clickhouse import ClickHouseConnector
        assert "clickhouse" in CONNECTORS
        assert CONNECTORS["clickhouse"] == ClickHouseConnector

    def test_get_connector_file(self):
        """Test getting file connector."""
        connector = get_connector("file")
        assert isinstance(connector, FileConnector)

    def test_get_connector_unknown(self):
        """Test error for unknown connector."""
        with pytest.raises(ConfigError) as exc_info:
            get_connector("unknown")
        assert "unknown" in str(exc_info.value).lower()


# =============================================================================
# LiteralConnector Tests
# =============================================================================


class TestLiteralConnector:
    """Tests for LiteralConnector."""

    def test_load_csv(self, temp_csv):
        """Test loading a CSV file."""
        connector = LiteralConnector()
        df = connector.load({"path": str(temp_csv)})
        assert isinstance(df, pl.DataFrame)
        assert len(df) > 0

    def test_load_missing_path(self):
        """Test error when path missing from config."""
        connector = LiteralConnector()
        with pytest.raises(ConfigError):
            connector.load({})

    def test_load_nonexistent_file(self, tmp_path):
        """Test error for nonexistent file."""
        connector = LiteralConnector()
        with pytest.raises(ConnectorError) as exc_info:
            connector.load({"path": str(tmp_path / "missing.csv")})
        assert "not found" in str(exc_info.value).lower()


# =============================================================================
# FileConnector Tests
# =============================================================================


class TestFileConnector:
    """Tests for FileConnector."""

    def test_load_csv(self, temp_csv):
        """Test loading a CSV file."""
        connector = FileConnector()
        df = connector.load({"path": str(temp_csv)})
        assert isinstance(df, pl.DataFrame)
        assert len(df) > 0

    def test_load_missing_path_config(self):
        """Test error when path missing from config."""
        connector = FileConnector()
        with pytest.raises(ConfigError):
            connector.load({})


# =============================================================================
# Parser Connector Syntax Tests
# =============================================================================


class TestParserConnectorSyntax:
    """Tests for parsing connector syntax."""

    def test_parse_file_connector(self):
        """Test parsing file(alias) syntax."""
        result = parse("WITH file(trades) PLOT price AGAINST time")
        assert isinstance(result.source, ConnectorSource)
        assert result.source.connector == "file"
        assert result.source.alias == "trades"

    def test_parse_clickhouse_connector(self):
        """Test parsing clickhouse(alias) syntax."""
        result = parse("WITH clickhouse(production) PLOT price AGAINST time")
        assert isinstance(result.source, ConnectorSource)
        assert result.source.connector == "clickhouse"
        assert result.source.alias == "production"

    def test_parse_literal_path(self):
        """Test parsing literal file path (backward compat)."""
        result = parse("WITH 'data.csv' PLOT price AGAINST time")
        assert isinstance(result.source, LiteralSource)
        assert result.source.path == "data.csv"

    def test_parse_connector_case_insensitive(self):
        """Test connector names are case-insensitive."""
        result = parse("WITH FILE(trades) PLOT price AGAINST time")
        assert isinstance(result.source, ConnectorSource)
        assert result.source.connector == "file"

    def test_parse_connector_with_filter(self):
        """Test connector syntax with FILTER clause."""
        result = parse(
            "WITH file(trades) PLOT price AGAINST time FILTER price > 100"
        )
        assert isinstance(result.source, ConnectorSource)
        assert result.series[0].filter is not None

    def test_parse_connector_with_format(self):
        """Test connector syntax with FORMAT clause."""
        result = parse(
            "WITH clickhouse(prod) PLOT price AGAINST time FORMAT title = 'Chart'"
        )
        assert isinstance(result.source, ConnectorSource)
        assert result.series[0].format.title == "Chart"


# =============================================================================
# Integration Tests
# =============================================================================


class TestConnectorIntegration:
    """Integration tests for connector system."""

    def test_execute_with_file_connector(self, tmp_path, temp_csv, monkeypatch):
        """Test executing query with file connector."""
        # Create config
        config_path = tmp_path / "connectors.toml"
        config_path.write_text(f"""
[file.testdata]
path = "{temp_csv}"
""")
        monkeypatch.setattr("plotql.core.config.CONFIG_PATH", config_path)

        from plotql.core.executor import execute

        ast = parse("WITH file(testdata) PLOT y AGAINST x")
        results = execute(ast)

        assert len(results) == 1
        assert len(results[0].x) == 5  # temp_csv has 5 rows


# =============================================================================
# Filter Pushdown Tests
# =============================================================================


class TestClickHouseFilterPushdown:
    """Tests for ClickHouse filter pushdown."""

    def test_where_to_sql_simple(self):
        """Test converting a simple WhereClause to SQL."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        where = WhereClause(
            conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
        )

        sql = connector._where_to_sql(where)
        assert sql == "price > 100"

    def test_where_to_sql_string_value(self):
        """Test SQL generation with string values."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        where = WhereClause(
            conditions=[Condition(column="symbol", op=ComparisonOp.EQ, value="AAPL")]
        )

        sql = connector._where_to_sql(where)
        assert sql == "symbol = 'AAPL'"

    def test_where_to_sql_compound(self):
        """Test SQL generation with AND/OR operators."""
        from plotql.core.ast import Condition, ComparisonOp, LogicalOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        where = WhereClause(
            conditions=[
                Condition(column="price", op=ComparisonOp.GT, value=100),
                Condition(column="volume", op=ComparisonOp.GE, value=1000),
            ],
            operators=[LogicalOp.AND],
        )

        sql = connector._where_to_sql(where)
        assert sql == "price > 100 AND volume >= 1000"

    def test_apply_filters_no_existing_where(self):
        """Test appending WHERE to query without existing WHERE clause."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        query = "SELECT * FROM trades"
        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            )
        ]

        result = connector._apply_filters(query, filters)
        assert result == "SELECT * FROM trades WHERE price > 100"

    def test_apply_filters_with_order_by(self):
        """Test inserting WHERE before ORDER BY."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        query = "SELECT * FROM trades ORDER BY time"
        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            )
        ]

        result = connector._apply_filters(query, filters)
        assert result == "SELECT * FROM trades WHERE price > 100 ORDER BY time"

    def test_apply_filters_existing_where(self):
        """Test appending to existing WHERE clause."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        query = "SELECT * FROM trades WHERE active = 1"
        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            )
        ]

        result = connector._apply_filters(query, filters)
        assert result == "SELECT * FROM trades WHERE active = 1 AND (price > 100)"

    def test_apply_filters_existing_where_with_order_by(self):
        """Test appending to WHERE before ORDER BY."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        query = "SELECT * FROM trades WHERE active = 1 ORDER BY time"
        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            )
        ]

        result = connector._apply_filters(query, filters)
        assert result == "SELECT * FROM trades WHERE active = 1 AND (price > 100) ORDER BY time"

    def test_apply_filters_multiple_filters_or(self):
        """Test combining multiple filters with OR."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        query = "SELECT * FROM trades"
        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            ),
            WhereClause(
                conditions=[Condition(column="volume", op=ComparisonOp.GT, value=1000)]
            ),
        ]

        result = connector._apply_filters(query, filters)
        assert result == "SELECT * FROM trades WHERE (price > 100) OR (volume > 1000)"

    def test_supports_filter_pushdown_flag(self):
        """Test that ClickHouse connector has pushdown enabled."""
        from plotql.core.connectors.clickhouse import ClickHouseConnector
        from plotql.core.connectors.file import FileConnector
        from plotql.core.connectors.literal import LiteralConnector

        assert ClickHouseConnector().supports_filter_pushdown is True
        assert FileConnector().supports_filter_pushdown is False
        assert LiteralConnector().supports_filter_pushdown is False
