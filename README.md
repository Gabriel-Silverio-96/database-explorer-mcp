<h1 align="center">Database Explorer MCP</h1>

<p align="center">
<img width="1000" alt="Image" src="https://github.com/user-attachments/assets/afc98086-2cb6-4e39-89ec-ae63d7800de7" />
</p>

Explore databases with natural language

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

Create `.env` and add your PostgreSQL connection URL.

```
DATABASE_URL=postgresql://mcp_reader:replace_me@localhost:5432/app_db
```

## MCP tools

- `list_tables()` lists tables and views accessible in the `public` schema.
- `describe_table(table_name)` returns a table's columns, types, and nullability.
- `execute_readonly_query(sql, limit=100)` accepts a read-only SQL query and returns up to 500 rows.

Tool implementations live in `database_explorer/tools/`, grouped by responsibility. `server.py` registers them with the MCP server. Data access should be controlled through PostgreSQL permissions and, where needed, approved views or schemas.

## Run the MCP Inspector

With the virtual environment activated and `.env` configured, run:

```bash
mcp dev server.py
```

The Inspector starts the local server and lets you call its tools. The server loads `DATABASE_URL` from `.env`.

## Connect a local LLM client

An LLM model does not connect to an MCP server by itself. The application or CLI you use with the model must support MCP, including local `stdio` servers. Keep this project on the same computer as that client. The client starts the server process when it needs the tools.

Before configuring a client, complete the setup above and make sure `.env` contains a valid `DATABASE_URL`. Do not put the database URL or password in the MCP client configuration file.

### Gemini CLI

Gemini CLI reads MCP server definitions from `~/.gemini/settings.json`. Add a `mcpServers` entry, preserving any other settings already in that file. Replace `/absolute/path/to/database_explorer_mcp` with the full path to this project directory:

```json
{
  "mcpServers": {
    "database-explorer": {
      "command": "/absolute/path/to/database_explorer_mcp/.venv/bin/python",
      "args": ["/absolute/path/to/database_explorer_mcp/server.py"],
      "cwd": "/absolute/path/to/database_explorer_mcp"
    }
  }
}
```

### Other MCP clients

For another local client, add an MCP server using the `stdio` transport with these settings:

- **Command:** the absolute path to `.venv/bin/python` in this project
- **Arguments:** the absolute path to this project's `server.py`
- **Working directory:** this project's root directory

For example, the command and arguments can be tested from a terminal in the project directory:

```bash
.venv/bin/python server.py
```
