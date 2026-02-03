import redis.asyncio as aioredis

# import asyncio


async def run(pool: aioredis.ConnectionPool):
    r_c = aioredis.Redis.from_pool(pool)
    await r_c.hset("a", "a", value="sdfdsfds", mapping={"userId": "12312", "sids": "sdfdsfds"})  # type: ignore

    result: str = await r_c.hget("a", "a")  # type: ignore
    if result:
        print(result)


