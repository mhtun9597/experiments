from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool
def private_greet(greet: str) -> str:
    return greet


# @mcp.tool
# def greet1(name: str) -> str:
#     return f"Hello12312321321, {name}!"


if __name__ == "__main__":
    mcp.run()
