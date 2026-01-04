"""
ClickHouse connector for PlotQL.

Handles ClickHouse database queries: WITH source(pump_fun, trades)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import polars as pl

from plotql.core.connectors.base import Connector, ConfigError, ConnectionError

if TYPE_CHECKING:
    from plotql.core.ast import WhereClause


class ClickHouseConnector(Connector):
    """
    Connector for ClickHouse databases.

    Used when a source with type="clickhouse" is specified:
        WITH source(pump_fun, trades)

    Where pump_fun is configured in sources.toml as:
        [pump_fun]
        type = "clickhouse"
        host = "localhost"
        database = "pump_fun"
        limit = 10000

    And trades is the table name passed at query time.

    Requires clickhouse-connect package: pip install plotql[clickhouse]

    Supports filter pushdown: PlotQL FILTER clauses are converted to SQL
    WHERE clauses for efficient filtering at the database level.
    """

    supports_filter_pushdown: bool = True

    def validate_config(self, config: dict) -> None:
        """Validate ClickHouse configuration."""
        required = ["host", "table"]
        missing = [key for key in required if key not in config]

        if missing:
            raise ConfigError(
                f"ClickHouse connector requires: {', '.join(missing)}. "
                "Ensure host is in config and table is provided in query."
            )

    def load(
        self,
        config: dict,
        filters: Optional[List["WhereClause"]] = None,
    ) -> pl.DataFrame:
        """
        Load data from ClickHouse.

        Args:
            config: Must contain:
                - host: ClickHouse server hostname
                - table: Table name to query (passed from source args)
                Optional:
                - port: Server port (default: 8123)
                - username: Authentication username
                - password: Authentication password
                - database: Database name
                - limit: Row limit (default: 10000)
            filters: Optional list of WhereClause filters to push down.
                     Multiple filters are combined with OR (since each
                     series needs its subset of data).

        Returns:
            Polars DataFrame with query results.

        Raises:
            ConfigError: If required config is missing.
            ConnectionError: If connection or query fails.
        """
        self.validate_config(config)

        try:
            import clickhouse_connect
        except ImportError:
            raise ConfigError(
                "ClickHouse connector requires clickhouse-connect package. "
                "Install with: pip install plotql[clickhouse] "
                "or: pip install clickhouse-connect"
            )

        host = config["host"]
        port = config.get("port", 8123)
        username = config.get("username")
        password = config.get("password")
        database = config.get("database")
        table = config["table"]
        limit = config.get("limit", 10000)

        # Build the query
        query = self._build_query(table, filters, limit)

        try:
            client = clickhouse_connect.get_client(
                host=host,
                port=port,
                username=username,
                password=password,
                database=database,
            )

            result = client.query(query)

            # Convert to Polars DataFrame
            # clickhouse-connect returns column_names and result_set
            data = {
                col: [row[i] for row in result.result_set]
                for i, col in enumerate(result.column_names)
            }

            return pl.DataFrame(data)

        except Exception as e:
            raise ConnectionError(f"ClickHouse query failed: {e}")

    def _build_query(
        self,
        table: str,
        filters: Optional[List["WhereClause"]],
        limit: int,
    ) -> str:
        """
        Build SQL query from table name, filters, and limit.

        Generates: SELECT * FROM {table} [WHERE ...] LIMIT {limit}
        """
        query = f"SELECT * FROM {table}"

        if filters:
            where_clause = self._build_where_clause(filters)
            query += f" WHERE {where_clause}"

        query += f" LIMIT {limit}"
        return query

    def _build_where_clause(self, filters: List["WhereClause"]) -> str:
        """
        Build WHERE clause from filters.

        Multiple filters are combined with OR (each filter represents
        a different series that needs its data subset).
        """
        filter_sqls = [self._where_to_sql(where) for where in filters]

        if len(filter_sqls) == 1:
            return filter_sqls[0]
        else:
            # Wrap each in parens and OR together
            return " OR ".join(f"({sql})" for sql in filter_sqls)

    def _where_to_sql(self, where: "WhereClause") -> str:
        """Convert a WhereClause to SQL condition string."""
        from plotql.core.ast import ComparisonOp, LogicalOp

        conditions = []
        for i, cond in enumerate(where.conditions):
            # Format value for SQL
            if isinstance(cond.value, str):
                sql_value = f"'{cond.value}'"
            else:
                sql_value = str(cond.value)

            # Map comparison operator
            op_map = {
                ComparisonOp.EQ: "=",
                ComparisonOp.NE: "!=",
                ComparisonOp.LT: "<",
                ComparisonOp.LE: "<=",
                ComparisonOp.GT: ">",
                ComparisonOp.GE: ">=",
            }
            sql_op = op_map.get(cond.op, "=")

            conditions.append(f"{cond.column} {sql_op} {sql_value}")

            # Add logical operator if there's a next condition
            if i < len(where.operators):
                op = where.operators[i]
                conditions.append("AND" if op == LogicalOp.AND else "OR")

        return " ".join(conditions)
