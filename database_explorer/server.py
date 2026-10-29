"""MCP server registration and process entry point."""

from mcp.server import MCPServer

from database_explorer.tools.queries import execute_readonly_query
from database_explorer.tools.tables import describe_table, list_tables

mcp = MCPServer("Database Explorer")
mcp.tool()(list_tables)
mcp.tool()(describe_table)
mcp.tool()(execute_readonly_query)


def main() -> None:
    """Start the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
