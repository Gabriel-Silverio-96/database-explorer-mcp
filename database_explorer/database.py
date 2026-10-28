"""PostgreSQL connection management."""

from typing import Any

import psycopg

from database_explorer.config import DATABASE_URL


def get_connection() -> psycopg.Connection[Any]:
    """Open a connection using the configured database URL."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured. Copy .env.example to .env.")
    return psycopg.connect(DATABASE_URL, connect_timeout=5)
