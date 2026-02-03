import asyncio
from typing import Any, Callable
import inspect


def set_time_out(sec: int, func: Callable[..., Any]):
    async def __inner():
        await asyncio.sleep(sec)
        return await func() if inspect.iscoroutinefunction(func) else func()

    asyncio.create_task(__inner())


async def main():
    # print("main executed")

    # fut = asyncio.get_event_loop().create_future()

    # print("executing")

    # async def my_func():
    #     await asyncio.sleep(3)
    #     print("my function executed")

    # try:
    #     set_time_out(5, my_func)
    # except:
    #     print("inside exception")
    # finally:
    #     print("fut finished")
    # print("Loweset")
    # while True:
    #     print("Running for another task")
    #     await asyncio.sleep(3)
    t()


def t():
    from pathlib import Path

    path = Path("./__langchain/knowledges")

    print("Exists:", path.exists())
    print("Is file:", path.is_file())
    print("Is directory:", path.is_dir())


async def worker():
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
