from typing import Annotated, Any, Literal, Optional

from fastmcp import FastMCP
from datetime import datetime

from pydantic import BaseModel, Field

mcp = FastMCP("My MCP Server")


class Tenant(BaseModel):
    name: Annotated[str, Field(description="name of the tenant")]


class RTenant(Tenant):
    id: str


# @mcp.tool
# def test_tool(data: str) -> Any:
#     id = datetime.now().isoformat()
#     raise Exception("Testing")


# t: tuple[str, str] = ("1", "2")
# test_tool(("1", "2"))

# @mcp.tool
# def register_tenant(name: str) -> Any:
#     id = datetime.now().isoformat()
#     return {"id": id, "name": name}

KYC: dict[int, bool] = {1: True, 2: False}


class A(BaseModel):
    a: str


class B(BaseModel):
    b: str
    parent: A


class C(BaseModel):
    c: str
    parent: B


class O(BaseModel):
    id: int
    name: Optional[str]
    parent: C = C(c="123", parent=B(b="sdfsd", parent=A(a="sdfdsfds")))


@mcp.tool
def check_kyc_status() -> O:
    # O(id=1, name="O", ages=["O"], child=[OC(id=123)])
    return O(id=1, name="O")


@mcp.tool
def test() -> dict[str, Any]:
    return {"a": "a"}


# @mcp.tool
# def greet1(name: str) -> str:
#     return f"Hello12312321321, {name}!"


if __name__ == "__main__":
    # mcp.run(transport="http", port=1111, host="localhost")
    mcp.run()
