"""Application entry point for the Database Explorer MCP server."""

from mcp.server import MCPServer
from database_explorer.tools.queries import execute_readonly_query
from database_explorer.tools.tables import describe_table, list_tables

mcp = MCPServer("Database Explorer")
mcp.tool()(list_tables)
mcp.tool()(describe_table)
mcp.tool()(execute_readonly_query)

if __name__ == "__main__":
    mcp.run()
