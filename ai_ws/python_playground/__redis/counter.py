import redis.asyncio as aioredis


async def run(pool: aioredis.ConnectionPool) -> None:
    rc = aioredis.Redis.from_pool(pool)
    ns = "testing"
    # await rc.hset(ns, "test", "1")  # type: ignore
    res = await rc.hget(ns, "test")  # type: ignore
    print(res)
    await rc.hset(ns, "test", str(int(res) + 1))  # type: ignore
    res = await rc.hget(ns, "test")  # type: ignore
    print(res)

    await rc.delete(ns)  # type: ignore
    res = await rc.hget(ns, "test")  # type: ignore
    print(res)
