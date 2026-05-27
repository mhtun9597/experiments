from typing import Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy import text
import asyncio


async def run():
    connection = "postgresql+asyncpg://admin:admin@localhost:5432/test"
    _engine = create_async_engine(connection)
    Session = async_sessionmaker(
        _engine,
        expire_on_commit=False,
    )
    async with Session() as session:
        query = "SELECT * from test where balance > 1;"
        result = await session.execute(text(query))
        print(list(result.keys()))
        res = list(result.fetchall())
        _res: list[list[Any]] = [list(r) for r in res]
        print(_res)


if __name__ == "__main__":
    asyncio.run(run())
