from typing import cast
from pydantic import BaseModel, ValidationError
import redis.asyncio as aioredis
import asyncio


class Msg(BaseModel):
    id: str


async def run(pool: aioredis.ConnectionPool):
    workers: list[int] = [1, 2]
    msgs: list[Msg] = [
        Msg(id="A"),
        Msg(id="B"),
        Msg(id="C"),
        Msg(id="D"),
    ]
    channel: str = "TEST1"

    client1 = aioredis.Redis.from_pool(pool)
    client2 = aioredis.Redis.from_pool(pool)
    # await pool.disconnect(True)
    # await client1.aclose()
    # try:
    #     pong = await client1.ping()  # type: ignore
    # except Exception as e:
    #     print(e)
    # asyncio.create_task(publisher(channel, msgs, client2))

    for w in workers:
        asyncio.create_task(consumer(channel, client1, w))

    # await asyncio.sleep(2)
    # asyncio.create_task(publisher(channel, msgs, client2))
    while True:
        await asyncio.sleep(5)


async def publisher(key: str, messages: list[Msg], r: aioredis.Redis) -> None:

    for msg in messages:
        await r.rpush(key, msg.model_dump_json())  # type: ignore

        print("broadcasted msg ", msg, "__repr__ ", msg.model_dump_json())


async def consumer(key: str, r: aioredis.Redis, wokerId: int) -> None:
    print(f"worker {wokerId} has started.")
    while True:
        try:
            result = await r.lpop(key)  # type: ignore
            # msg: Msg = Msg.model_validate_json(cast(bytes, result[1]))
            # msgOrm: MsgORM = msg.to_orm()
            print(f"worker {wokerId} working for msg {result}")
            await asyncio.sleep(3)
            print(f"worker {wokerId} done msg {result}")
        except ValidationError as e:
            print("Validation Error occurs", e)
