from mcp.server.fastmcp import FastMCP
from src.vasthu_knowledge_mcp.tools import register_read_tools
from src.vasthu_knowledge_mcp.tools import register_write_tools
mcp = FastMCP("vasthu-knowledge-mcp", port=7001)
register_read_tools(mcp = mcp)
register_write_tools(mcp = mcp)


def mcp_run():
    mcp.run(transport="streamable-http")