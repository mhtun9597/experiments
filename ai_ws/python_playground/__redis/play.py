import redis.asyncio as aioredis
import asyncio

pool: aioredis.ConnectionPool = aioredis.ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)  # type: ignore


async def main():
    # from hmap import run
    from fifo import run

    await run(pool)


if __name__ == "__main__":
    asyncio.run(main())
