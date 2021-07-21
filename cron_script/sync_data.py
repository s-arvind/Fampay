import asyncio
from clients import youtube_client, logger

async def do():
    logger.info("syncing records")
    await youtube_client.search()


if __name__ == "__main__":
    asyncio.run(do())
