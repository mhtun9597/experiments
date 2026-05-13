import asyncio
from pathlib import Path
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Generator,
    Generic,
    Iterator,
    Literal,
    Optional,
    Type,
    TypeVar,
    cast,
    overload,
)
import logging
from pydantic import BaseModel, ValidationError


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


class Speakable(ABC):
    @abstractmethod
    def speak(self) -> int: ...


class Flyable(ABC):
    @abstractmethod
    def fly(self) -> str: ...


S = TypeVar("S", bound=Speakable)
F = TypeVar("F", bound=Flyable)


class Animal(Generic[S, F]):
    def __int__(self):
        super().__init__()


class Speakable1(Speakable):

    def speak(self) -> int:
        return 1


class Flyable1(Flyable):
    def fly(self) -> str:
        return "Testing"


class Animal1(Animal[Speakable1, Flyable1]):
    def __init__(self) -> None:
        super().__init__()


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


class C1:
    def __init__(self, name: str = "default") -> None:
        self.name = name


def t(**kwargs: Any) -> None:
    print(C1(**kwargs).name)


from datetime import datetime, timedelta


class Address(BaseModel):
    name: str


class Person(BaseModel):
    name: str
    address: list[Address]


# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

import re

import ast

import help

logger = logging.getLogger(__name__)


async def request():
    import httpx

    try:
        async with httpx.AsyncClient() as client:

            res = await client.request(
                url="http://localhost:3333/register",
                method="POST",
                json={"name": "Facebook"},
            )
            return res.json()
    except Exception as e:
        logger.warning(f"http tool call failed {e}")
    return "Tool call failed"


async def kf(**kwargs: Any):
    url = "{test}"
    url = url.format(**kwargs)
    print(url)
    try:
        url = ast.literal_eval(url)
    except Exception as e:
        pass

    print(isinstance(url, str))


from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
# T = TypeVar("T")


class RequestContext:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


def wrapper_1(
    func: Callable[Concatenate[int, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Wrapper 1 see", args)
        print(kwargs)
        return await func(1, *args, **kwargs)

    return wrapper


def wrapper_2(
    func: Callable[Concatenate[int, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Wrapper 2 see", args)
        print(kwargs)
        return await func(2, *args, **kwargs)

    return wrapper


@wrapper_1
@wrapper_2
async def _t(one: int, two: int, test: str):
    print(
        "Test",
        one,
    )


def tt(t: list[Any]):
    pass


class A(BaseModel):
    a: Optional[dict[str, str]] = None


async def run():
    d = {"a": 1}
    del d["a"]
    print(d)
    # a = [1, 2]
    # a.append(3)
    # print(a)
    # await sleeper(2)
    # logger.critical("Testing")
    # import re

    # log: str = (
    #     "2026-04-23 10:39:42,443 - asyncio - DEBUG - Using proactor: IocpProactor"
    # )

    # pattern = (
    #     r"^(?P<timestamp>.*?) - (?P<service>.*?) - (?P<level>.*?) - (?P<message>.*)$"
    # )
    # match = re.match(pattern, log)
    # if match:
    #     data = match.groupdict()
    #     print(data["timestamp"])
    #     logger.info(data)
    # from datetime import datetime

    # s = "212312321"

    # dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S,%f")

    # print(dt)

    # a = [1, 2, 3]
    # print(a[3:])
    # print(a[:float[]-])


# import json
# chunk: bytes
# async with aiofiles.open(f"help.py", "rb") as out_file:
#     chunk = await out_file.read(1024 * 1024)
# print(b)
# s = b.decode()
# print(s)
# await kf(test="teterte")
# print(a)
# import ast

# res = await request()
# print(res)
# a = a.format(test="12312312")
# a = ast.literal_eval(a)
# print(a)
# print(isinstance(a, list))
# kf(test="1231232")

# json_string = '{"name": "John Doe", "id": "123456789", "verified": true}'
# my_dict = json.loads(json_string)

# print(my_dict)
# a = "12312"
# if a:
#     print("Triggered")
# current = datetime.now()
# future = current + timedelta(hours=1)
# print(current)

# print(future)

# sorted_items = sorted(d.items(), key=lambda x: x[1])

# print(sorted_items)


async def sleeper(sec: int):
    print("called")
    await asyncio.sleep(sec)
    print("waited")


async def start() -> None:
    t: asyncio.Task[None] = asyncio.create_task(sleeper(5))
    t1: asyncio.Task[None] = asyncio.create_task(sleeper(6))

    def cb(result: asyncio.Task[None]) -> None:
        print(f"Done ")

    t.add_done_callback(cb)
    t1.add_done_callback(cb)
    print("Done all")
    while True:
        await asyncio.sleep(3)


def ttt() -> str:
    a = ""
    return a or "Testinjg"


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


def sync_fn(x: int) -> int:
    import time

    time.sleep(x)
    return x * 2


async def async_fn(x: int) -> int:
    return await asyncio.to_thread(sync_fn, x)


if __name__ == "__main__":
    asyncio.run(run())
