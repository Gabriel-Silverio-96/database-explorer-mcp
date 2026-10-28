"""MCP tool for executing validated, read-only SQL queries."""

import json
from typing import Any

from database_explorer.config import (
    DEFAULT_ROW_LIMIT,
    MAX_ROW_LIMIT,
    STATEMENT_TIMEOUT_MS,
)
from database_explorer.database import get_connection
from database_explorer.sql_validation import validate_readonly_query


def execute_readonly_query(sql: str, limit: int = DEFAULT_ROW_LIMIT) -> dict[str, Any]:
    """Run a single SELECT query in a read-only transaction (maximum 500 rows)."""
    if not 1 <= limit <= MAX_ROW_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_ROW_LIMIT}.")
    safe_query = validate_readonly_query(sql)
    wrapped_query = f"SELECT * FROM ({safe_query}) AS mcp_result LIMIT %s"

    with get_connection() as conn:
        with conn.transaction():
            with conn.cursor() as cursor:
                cursor.execute("SET TRANSACTION READ ONLY")
                cursor.execute(
                    "SELECT set_config('statement_timeout', %s, true)",
                    (f"{STATEMENT_TIMEOUT_MS}ms",),
                )
                cursor.execute(wrapped_query, (limit + 1,))
                rows = cursor.fetchall()
                columns = [description.name for description in cursor.description or []]

    visible_rows = rows[:limit]
    # Convert types such as Decimal, date, and UUID to JSON-compatible values.
    json_rows = json.loads(json.dumps(visible_rows, default=str))
    return {
        "columns": columns,
        "rows": json_rows,
        "row_count": len(visible_rows),
        "truncated": len(rows) > limit,
    }
