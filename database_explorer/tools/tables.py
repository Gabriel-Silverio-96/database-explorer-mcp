"""MCP tools for discovering PostgreSQL tables and columns."""

from typing import Any

from database_explorer.database import get_connection


def list_tables() -> dict[str, list[str]]:
    """List tables and views accessible in the public schema."""
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type IN ('BASE TABLE', 'VIEW')
        ORDER BY table_name
    """
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(query)
        return {"tables": [row[0] for row in cursor.fetchall()]}


def describe_table(table_name: str) -> dict[str, Any]:
    """Show the names, types, and nullability of a table or view's columns in public."""
    if not table_name or len(table_name) > 63:
        raise ValueError("Invalid table name.")
    query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
    if not columns:
        raise ValueError(f"Table or view not found in the public schema: {table_name}")
    return {
        "table": table_name,
        "columns": [
            {"name": name, "type": data_type, "nullable": nullable == "YES"}
            for name, data_type, nullable in columns
        ],
    }
