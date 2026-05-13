import asyncio
from typing import Any
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["server.py"],
)

transport = StdioTransport(
    command="python",
    args=["server.py", "--verbose"],
    cwd="__mcp",
)


async def get_tools() -> list[Any]:
    result: list[Any] = []
    try:
        async with Client("http://localhost:1111/mcp") as client:
            tools = await client.list_tools()
            print(tools)

            # client
            print("Calling")
            try:
                res = await client.call_tool(name="test", arguments=None)
                print("Result ", res)
            except Exception as e:

                print(
                    f"Exception {e}",
                )

            # result = await client.list_tools()

        # async with stdio_client(server_params) as (read, write):
        #     async with ClientSession(read, write) as session:
        #         # Initialize the connection
        #         await session.initialize()

        #         # Get tools
        #         tools = await load_mcp_tools(session)

        #         print("Langchain load tools ", tools)

    except Exception as e:
        print(e)
    finally:
        # if client:
        #     await client.close()
        return result


async def run():
    await get_tools()
    # while True:
    #
    #     await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(run())
