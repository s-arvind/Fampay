import asyncio
from clients import youtube_client, logger

async def do():
    logger.info("syncing records")
    # sync youtube records to elasticsearch
    await youtube_client.search()


if __name__ == "__main__":
    asyncio.run(do())
