import asyncio
from app.db.health import check_mongo_connect


async def main():

    await check_mongo_connect()


if __name__ == "__main__":
    asyncio.run(main())
