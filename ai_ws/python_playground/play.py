import asyncio
from pathlib import Path
from typing import Any, AsyncGenerator, AsyncIterator, Generator, Iterator, Optional

from pydantic import BaseModel


class HandoffEevnt(BaseModel):
    h_id: str


class ConvEvent(BaseModel):
    id: str
    msg: str


class Event(BaseModel):
    type: str
    payload: Any


var = "124"


class IWS(BaseModel):
    sid: str


class WS(BaseModel):
    id: int
    sids: list[IWS]


from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self) -> AsyncIterator[int]: ...


class Duck(Animal):

    async def speak(self) -> AsyncIterator[int]:
        print("waiting ")
        await asyncio.sleep(2)
        yield 1


_str = "Hello {World}"


async def _itr(r: int) -> AsyncIterator[int]:
    print("called _itr")
    for i in range(r):
        await asyncio.sleep(2)
        yield i


async def itr(r: int) -> AsyncIterator[int]:
    print("called itr")
    async for i in _itr(r):
        yield i


class C:

    def __init__(self, a: str, b: str) -> None:
        print(a, b)


def t(**kwargs: Any) -> None:
    C(**kwargs)


async def f() -> int:
    await asyncio.sleep(2)
    raise Exception("testing")


def cb(result: asyncio.Task[int]) -> None:
    async def __acb() -> None:
        print("result ", result.result())
        await asyncio.sleep(2)

    asyncio.create_task(__acb())


async def run():

    task: asyncio.Task[int] = asyncio.create_task(f())
    task.add_done_callback(cb)

    while True:
        await asyncio.sleep(2)

    # async for val in generator():
    #     print(val)
    # func_str = """async def hello():
    #                 import asyncio
    #                 print("sleeping now")
    #                 await asyncio.sleep(3)
    #                 a = "hello world12321312"
    #                 print(a)

    #            """
    # namespace: dict[str, Any] = {}
    # exec(func_str, namespace)
    # await namespace["hello"]()

    # sys.stdout.flush()
    # path = Path("__langchain")
    # all_files: list[str] = [str(p) for p in path.rglob("*") if p.is_file()]


# async def hello():
#     await asyncio.sleep(3)
#     a = "hello world12321312"
#     print(a)


def trim_api_version(path: str) -> str:
    import re

    return re.sub(r"/v\d+(?=/)", "", path)


# tests
paths = [
    "api/v2/admin",
    "api/v10/admin",
    "api/admin",
    "api/v3/users/123",
]


def b(*args: Any) -> None:
    print(args)


if __name__ == "__main__":
    asyncio.run(run())
