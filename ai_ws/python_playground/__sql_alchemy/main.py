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
        query = "SELECT balance, id from test where id = 1;"
        result = await session.execute(text(query))
        print(list(result.keys()))
        res = list(result.fetchall())
        print(res)


if __name__ == "__main__":
    asyncio.run(run())
