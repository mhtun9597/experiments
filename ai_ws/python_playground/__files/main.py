import aiofiles


async def read_file():
    async with aiofiles.open("example.txt", "r") as f:
        content = await f.read()

    print(content)


asyncio.run(read_file())
