"""Read-only SQL validation helpers."""

import sqlglot
from sqlglot import exp


def validate_readonly_query(sql: str) -> str:
    """Validate one read-only PostgreSQL query and return normalized SQL."""
    statements = sqlglot.parse(sql, read="postgres")
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Provide exactly one SQL statement.")
    statement = statements[0]
    if not isinstance(statement, exp.Query):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden = (exp.Insert, exp.Update, exp.Delete, exp.Create, exp.Drop, exp.Command)
    if any(isinstance(node, forbidden) for node in statement.walk()):
        raise ValueError("The query contains a disallowed operation.")
    if any(isinstance(node, exp.Lock) for node in statement.walk()):
        raise ValueError("SELECT ... FOR UPDATE/SHARE is not allowed.")

    # Enforce the PostgreSQL dialect and restrict access to the public schema.
    for table in statement.find_all(exp.Table):
        if table.db and table.db.lower() != "public":
            raise ValueError("Queries can only access the public schema.")
    return statement.sql(dialect="postgres")
