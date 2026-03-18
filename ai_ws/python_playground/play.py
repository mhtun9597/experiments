import asyncio
from pathlib import Path
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Generator,
    Iterator,
    Optional,
    Type,
    TypeVar,
    cast,
    overload,
)
import logging
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


class C1:
    def __init__(self, name: str = "default") -> None:
        self.name = name


def t(**kwargs: Any) -> None:
    print(C1(**kwargs).name)


from datetime import datetime as _datetime

import datetime


class Address(BaseModel):
    name: str


class Person(BaseModel):
    name: str
    address: list[Address]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

import os
import shutil


async def run():
    # import json

    # json_string = '{"name": "John Doe", "id": "123456789", "verified": true}'
    # my_dict = json.loads(json_string)

    # print(my_dict)
    ttt(name="test", address=1)


def ttt(**kwargs: Any):
    print(kwargs)


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
