# Database Explorer MCP

A Python MCP server for discovering tables and running read-only PostgreSQL queries.

## Requirements

- Python 3.11 or newer
- PostgreSQL accessible from the machine running the MCP server
- A dedicated PostgreSQL user with read-only permissions

## Set up the environment

From the project directory, run:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and replace the example URL with the URL for your database and read-only user. Do not use administrator credentials. Git ignores this file.

## PostgreSQL permissions

Create a dedicated user and grant access only to the required database, schema, and tables. For example, run the following as a PostgreSQL administrator in `psql` (adjust the names and password):

```sql
CREATE ROLE mcp_reader LOGIN PASSWORD 'replace-this-password';
GRANT CONNECT ON DATABASE app_db TO mcp_reader;
GRANT USAGE ON SCHEMA public TO mcp_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO mcp_reader;
```

`ALTER DEFAULT PRIVILEGES` applies to objects created by the user who ran the command. For production, grant `SELECT` explicitly only on approved tables and review access to sensitive data.

## MCP tools

- `list_tables()` lists tables and views accessible in the `public` schema.
- `describe_table(table_name)` returns a table's columns, types, and nullability.
- `execute_readonly_query(sql, limit=100)` accepts a read-only SQL query and returns up to 500 rows.

## Run the MCP Inspector

With the virtual environment activated and `.env` configured, run:

```bash
mcp dev server.py
```

The Inspector starts the local server and lets you call its tools. To connect another MCP client, configure it to run the absolute path to the Python executable in `.venv/bin/python` and the absolute path to this `server.py`. The server loads `DATABASE_URL` from `.env`.
