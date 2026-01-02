"""
ClickHouse connector for PlotQL.

Handles ClickHouse database queries: WITH clickhouse(trades)
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

    Used when clickhouse() function is specified in WITH clause
    (e.g., WITH clickhouse(trades)).

    Requires clickhouse-connect package: pip install plotql[clickhouse]

    Supports filter pushdown: PlotQL FILTER clauses are converted to SQL
    WHERE clauses and appended to the base query for efficient filtering
    at the database level.
    """

    supports_filter_pushdown: bool = True

    def validate_config(self, config: dict) -> None:
        """Validate ClickHouse configuration."""
        required = ["host", "query"]
        missing = [key for key in required if key not in config]

        if missing:
            raise ConfigError(
                f"ClickHouse connector requires: {', '.join(missing)}. "
                "Add these to your connector config."
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
                - query: SQL query to execute
                Optional:
                - port: Server port (default: 8123)
                - username: Authentication username
                - password: Authentication password
                - database: Database name
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
        query = config["query"]

        # Apply filter pushdown if we have filters
        if filters:
            query = self._apply_filters(query, filters)

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

    def _apply_filters(
        self,
        query: str,
        filters: List["WhereClause"],
    ) -> str:
        """
        Append WHERE clause conditions to the query.

        Multiple filters are combined with OR (each filter represents
        a different series that needs its data subset).

        If the query already has WHERE, appends with AND (...).
        Otherwise adds WHERE clause.
        """
        from plotql.core.ast import ComparisonOp, LogicalOp

        # Build SQL for each filter, then OR them together
        filter_sqls = []
        for where in filters:
            filter_sqls.append(self._where_to_sql(where))

        # Combine filters with OR
        if len(filter_sqls) == 1:
            combined_sql = filter_sqls[0]
        else:
            # Wrap each in parens and OR together
            combined_sql = " OR ".join(f"({sql})" for sql in filter_sqls)

        # Check if query already has WHERE (case-insensitive)
        query_upper = query.upper()
        if " WHERE " in query_upper:
            # Find the position and append with AND (...)
            where_pos = query_upper.find(" WHERE ") + 7

            # Find end of WHERE clause (before ORDER BY, LIMIT, GROUP BY)
            end_keywords = [" ORDER BY", " LIMIT", " GROUP BY", " HAVING"]
            end_pos = len(query)
            for kw in end_keywords:
                pos = query_upper.find(kw, where_pos)
                if pos != -1 and pos < end_pos:
                    end_pos = pos

            # Insert the additional conditions wrapped in parens
            new_query = (
                query[:end_pos]
                + " AND (" + combined_sql + ")"
                + query[end_pos:]
            )
            return new_query
        else:
            # No WHERE clause - need to add one
            # Find where to insert (before ORDER BY, LIMIT, GROUP BY)
            end_keywords = [" ORDER BY", " LIMIT", " GROUP BY", " HAVING"]
            insert_pos = len(query)
            for kw in end_keywords:
                pos = query_upper.find(kw)
                if pos != -1 and pos < insert_pos:
                    insert_pos = pos

            new_query = (
                query[:insert_pos]
                + " WHERE " + combined_sql
                + query[insert_pos:]
            )
            return new_query

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
