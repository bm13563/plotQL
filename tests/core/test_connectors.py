"""
Unit tests for PlotQL connectors.

Tests connector base class, config loading, and connector implementations.
"""
import polars as pl
import pytest

from plotql.core.config import (
    ConfigError,
    get_source_config,
    list_sources,
    list_sources_by_type,
    load_config,
)
from plotql.core.connectors import (
    CONNECTORS,
    ConnectorError,
    FileConnector,
    FolderConnector,
    LiteralConnector,
    get_connector,
)
from plotql.core.ast import SourceRef
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
        config_path = tmp_path / "sources.toml"
        config_path.write_text("""
[trades]
type = "file"
path = "/data/trades.csv"

[production]
type = "clickhouse"
host = "localhost"
port = 8123
database = "mydb"
limit = 10000
""")
        config = load_config(config_path)

        assert "trades" in config
        assert config["trades"]["type"] == "file"
        assert config["trades"]["path"] == "/data/trades.csv"

        assert "production" in config
        assert config["production"]["type"] == "clickhouse"
        assert config["production"]["host"] == "localhost"

    def test_load_invalid_toml(self, tmp_path):
        """Test loading invalid TOML raises error."""
        config_path = tmp_path / "bad.toml"
        config_path.write_text("this is not valid toml [[[")

        with pytest.raises(ConfigError) as exc_info:
            load_config(config_path)
        assert "Invalid TOML" in str(exc_info.value)


class TestGetSourceConfig:
    """Tests for get_source_config."""

    def test_get_existing_config(self, tmp_path):
        """Test getting config for existing source alias."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("""
[trades]
type = "file"
path = "/data/trades.csv"
""")
        source_config = get_source_config("trades", config_path)
        assert source_config.type == "file"
        assert source_config.config["path"] == "/data/trades.csv"

    def test_get_missing_alias(self, tmp_path):
        """Test error when alias not found."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("[trades]\ntype = 'file'\npath = '/data/trades.csv'")

        with pytest.raises(ConfigError) as exc_info:
            get_source_config("unknown", config_path)
        assert "unknown" in str(exc_info.value)

    def test_get_missing_type(self, tmp_path):
        """Test error when type is missing."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("[trades]\npath = '/data/trades.csv'")

        with pytest.raises(ConfigError) as exc_info:
            get_source_config("trades", config_path)
        assert "type" in str(exc_info.value).lower()


class TestListSources:
    """Tests for list_sources."""

    def test_list_existing_sources(self, tmp_path):
        """Test listing all source aliases."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("""
[trades]
type = "file"
path = "/data/trades.csv"

[orders]
type = "file"
path = "/data/orders.csv"
""")
        sources = list_sources(config_path)
        assert set(sources) == {"trades", "orders"}

    def test_list_empty_sources(self, tmp_path):
        """Test listing sources when none configured."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("")

        sources = list_sources(config_path)
        assert sources == []


class TestListSourcesByType:
    """Tests for list_sources_by_type."""

    def test_list_by_type(self, tmp_path):
        """Test listing sources grouped by type."""
        config_path = tmp_path / "sources.toml"
        config_path.write_text("""
[trades]
type = "file"
path = "/data/trades.csv"

[production]
type = "clickhouse"
host = "localhost"
database = "mydb"
limit = 10000
""")
        by_type = list_sources_by_type(config_path)
        assert "file" in by_type
        assert "trades" in by_type["file"]
        assert "clickhouse" in by_type
        assert "production" in by_type["clickhouse"]


# =============================================================================
# Connector Registry Tests
# =============================================================================


class TestConnectorRegistry:
    """Tests for connector registry."""

    def test_registry_has_file(self):
        """Test file connector is registered."""
        assert "file" in CONNECTORS
        assert CONNECTORS["file"] == FileConnector

    def test_registry_has_folder(self):
        """Test folder connector is registered."""
        assert "folder" in CONNECTORS
        assert CONNECTORS["folder"] == FolderConnector

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
# FolderConnector Tests
# =============================================================================


class TestFolderConnector:
    """Tests for FolderConnector."""

    def test_load_csv_single_segment(self, tmp_path):
        """Test loading a file with single path segment."""
        # Create a CSV file in the folder
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("x,y\n1,10\n2,20\n")

        connector = FolderConnector()
        df = connector.load({"path": str(tmp_path), "segments": ["data.csv"]})
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["x", "y"]

    def test_load_csv_multiple_segments(self, tmp_path):
        """Test loading a file with multiple path segments (subdirs)."""
        # Create nested directories
        subdir = tmp_path / "2024" / "jan"
        subdir.mkdir(parents=True)
        csv_file = subdir / "trades.csv"
        csv_file.write_text("price,volume\n100,50\n200,100\n300,150\n")

        connector = FolderConnector()
        df = connector.load({
            "path": str(tmp_path),
            "segments": ["2024", "jan", "trades.csv"]
        })
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["price", "volume"]

    def test_load_parquet(self, tmp_path):
        """Test loading a parquet file."""
        # Create a parquet file
        df_orig = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        parquet_file = tmp_path / "data.parquet"
        df_orig.write_parquet(parquet_file)

        connector = FolderConnector()
        df = connector.load({"path": str(tmp_path), "segments": ["data.parquet"]})
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 3

    def test_load_missing_path_config(self):
        """Test error when path missing from config."""
        connector = FolderConnector()
        with pytest.raises(ConfigError) as exc_info:
            connector.load({"segments": ["data.csv"]})
        assert "path" in str(exc_info.value).lower()

    def test_load_missing_segments(self, tmp_path):
        """Test error when segments missing from config."""
        connector = FolderConnector()
        with pytest.raises(ConfigError) as exc_info:
            connector.load({"path": str(tmp_path)})
        assert "segments" in str(exc_info.value).lower()

    def test_load_empty_segments(self, tmp_path):
        """Test error when segments list is empty."""
        connector = FolderConnector()
        with pytest.raises(ConfigError) as exc_info:
            connector.load({"path": str(tmp_path), "segments": []})
        assert "segments" in str(exc_info.value).lower()

    def test_load_nonexistent_file(self, tmp_path):
        """Test error for nonexistent file."""
        connector = FolderConnector()
        with pytest.raises(ConnectorError) as exc_info:
            connector.load({"path": str(tmp_path), "segments": ["missing.csv"]})
        assert "not found" in str(exc_info.value).lower()

    def test_path_traversal_blocked(self, tmp_path):
        """Test that path traversal is blocked."""
        # Create a file outside the root
        outside_file = tmp_path.parent / "secret.csv"
        outside_file.write_text("secret,data\n1,2\n")

        connector = FolderConnector()
        with pytest.raises(ConnectorError) as exc_info:
            connector.load({"path": str(tmp_path), "segments": ["..", "secret.csv"]})
        assert "traversal" in str(exc_info.value).lower()

        # Clean up
        outside_file.unlink()

    def test_supports_filter_pushdown_disabled(self):
        """Test that folder connector has pushdown disabled."""
        connector = FolderConnector()
        assert connector.supports_filter_pushdown is False


# =============================================================================
# Parser Connector Syntax Tests
# =============================================================================


class TestParserSourceSyntax:
    """Tests for parsing source() syntax."""

    def test_parse_source_literal(self):
        """Test parsing source('path') syntax."""
        result = parse("WITH source('data.csv') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.is_literal is True
        assert result.source.args == ["data.csv"]

    def test_parse_source_alias(self):
        """Test parsing source('alias') syntax."""
        result = parse("WITH source('trades') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        # Single arg is considered literal (file path)
        assert result.source.is_literal is True
        assert result.source.args == ["trades"]

    def test_parse_source_with_table(self):
        """Test parsing source('alias', 'table') syntax for databases."""
        result = parse("WITH source('pump_fun', 'trades') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.alias == "pump_fun"
        assert result.source.table == "trades"
        assert result.source.args == ["pump_fun", "trades"]

    def test_parse_source_multiple_segments(self):
        """Test parsing source('alias', 'dir', 'file') for folder connector."""
        result = parse("WITH source('local_data', 'subdir', 'data.csv') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.alias == "local_data"
        assert result.source.args == ["local_data", "subdir", "data.csv"]

    def test_parse_source_many_segments(self):
        """Test parsing source with many path segments."""
        result = parse("WITH source('data', 'y2024', 'jan', 'week1', 'trades.csv') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.alias == "data"
        assert result.source.args == ["data", "y2024", "jan", "week1", "trades.csv"]

    def test_parse_source_all_strings(self):
        """Test parsing source requires all string literals."""
        result = parse("WITH source('data', 'subdir.name', 'file') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.args == ["data", "subdir.name", "file"]

    def test_parse_source_case_insensitive(self):
        """Test SOURCE keyword is case-insensitive."""
        result = parse("WITH SOURCE('trades') PLOT price AGAINST time")
        assert isinstance(result.source, SourceRef)
        assert result.source.args == ["trades"]

    def test_parse_source_with_filter(self):
        """Test source syntax with FILTER clause."""
        result = parse(
            "WITH source('trades') PLOT price AGAINST time FILTER price > 100"
        )
        assert isinstance(result.source, SourceRef)
        assert result.series[0].filter is not None

    def test_parse_source_with_format(self):
        """Test source syntax with FORMAT clause."""
        result = parse(
            "WITH source('prod') PLOT price AGAINST time FORMAT title = 'Chart'"
        )
        assert isinstance(result.source, SourceRef)
        assert result.series[0].format.title == "Chart"

    def test_parse_source_rejects_unquoted_args(self):
        """Test that unquoted identifiers are rejected."""
        from plotql.core.parser import ParseError
        with pytest.raises(ParseError) as exc_info:
            parse("WITH source(trades) PLOT price AGAINST time")
        assert "string literal" in str(exc_info.value).lower()


# =============================================================================
# Integration Tests
# =============================================================================


class TestConnectorIntegration:
    """Integration tests for connector system."""

    def test_execute_with_source_alias(self, tmp_path, temp_csv, monkeypatch):
        """Test executing query with source('alias')."""
        # Create config
        config_path = tmp_path / "sources.toml"
        config_path.write_text(f"""
[testdata]
type = "file"
path = "{temp_csv}"
""")
        monkeypatch.setattr("plotql.core.config.CONFIG_PATH", config_path)

        from plotql.core.executor import execute

        ast = parse("WITH source('testdata') PLOT y AGAINST x")
        results = execute(ast)

        assert len(results) == 1
        assert len(results[0].x) == 5  # temp_csv has 5 rows

    def test_execute_with_folder_source(self, tmp_path, monkeypatch):
        """Test executing query with folder source('alias', 'file')."""
        # Create data directory and file
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        csv_file = data_dir / "trades.csv"
        csv_file.write_text("x,y\n1,10\n2,20\n3,30\n")

        # Create config
        config_path = tmp_path / "sources.toml"
        config_path.write_text(f"""
[local]
type = "folder"
path = "{data_dir}"
""")
        monkeypatch.setattr("plotql.core.config.CONFIG_PATH", config_path)

        from plotql.core.executor import execute

        ast = parse("WITH source('local', 'trades.csv') PLOT y AGAINST x")
        results = execute(ast)

        assert len(results) == 1
        assert len(results[0].x) == 3

    def test_execute_with_folder_source_nested(self, tmp_path, monkeypatch):
        """Test executing query with folder source and nested path."""
        # Create nested data directory and file
        data_dir = tmp_path / "data"
        nested_dir = data_dir / "2024" / "jan"
        nested_dir.mkdir(parents=True)
        csv_file = nested_dir / "trades.csv"
        csv_file.write_text("price,volume\n100,50\n200,100\n")

        # Create config
        config_path = tmp_path / "sources.toml"
        config_path.write_text(f"""
[local]
type = "folder"
path = "{data_dir}"
""")
        monkeypatch.setattr("plotql.core.config.CONFIG_PATH", config_path)

        from plotql.core.executor import execute

        ast = parse("WITH source('local', '2024', 'jan', 'trades.csv') PLOT volume AGAINST price")
        results = execute(ast)

        assert len(results) == 1
        assert len(results[0].x) == 2
        assert list(results[0].x) == [100, 200]
        assert list(results[0].y) == [50, 100]


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

    def test_build_query_no_filters(self):
        """Test building query without filters."""
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        result = connector._build_query("trades", None, 10000)
        assert result == "SELECT * FROM trades LIMIT 10000"

    def test_build_query_with_filter(self):
        """Test building query with single filter."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            )
        ]

        result = connector._build_query("trades", filters, 10000)
        assert result == "SELECT * FROM trades WHERE price > 100 LIMIT 10000"

    def test_build_query_with_custom_limit(self):
        """Test building query with custom limit."""
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        result = connector._build_query("trades", None, 5000)
        assert result == "SELECT * FROM trades LIMIT 5000"

    def test_build_query_multiple_filters_or(self):
        """Test building query with multiple filters combined with OR."""
        from plotql.core.ast import Condition, ComparisonOp, WhereClause
        from plotql.core.connectors.clickhouse import ClickHouseConnector

        connector = ClickHouseConnector()

        filters = [
            WhereClause(
                conditions=[Condition(column="price", op=ComparisonOp.GT, value=100)]
            ),
            WhereClause(
                conditions=[Condition(column="volume", op=ComparisonOp.GT, value=1000)]
            ),
        ]

        result = connector._build_query("trades", filters, 10000)
        assert result == "SELECT * FROM trades WHERE (price > 100) OR (volume > 1000) LIMIT 10000"

    def test_supports_filter_pushdown_flag(self):
        """Test that ClickHouse connector has pushdown enabled."""
        from plotql.core.connectors.clickhouse import ClickHouseConnector
        from plotql.core.connectors.file import FileConnector
        from plotql.core.connectors.literal import LiteralConnector

        assert ClickHouseConnector().supports_filter_pushdown is True
        assert FileConnector().supports_filter_pushdown is False
        assert LiteralConnector().supports_filter_pushdown is False
