from app.db.client import get_client
from app.core.config import DB_NAME, COLLECTIONS


async def check_mongo_connect() -> bool:
    try:
        client = get_client()
        await client.admin.command("ping")
        print(" Database Connection successful")
        return True
    except Exception as e:
        print("Database Connection failed: ", e)
        return False


async def ensure_databases() -> None:
    try:
        client = get_client()
        existing_dbs = await client.list_database_names()
        if DB_NAME in existing_dbs:
            print("Database presence established")
            return

        # Create a dummy collections to force DB creation
        if DB_NAME is None:
            raise Exception("Database Name is None")

        # A dummy collection to force DB creation
        db = client[DB_NAME]
        await db["__dummy__"].insert_one({"created": True})

    except Exception as e:
        print("Error establishing database: ", e)


async def ensure_collections() -> None:
    try:
        client = get_client()
        if DB_NAME is None:
            raise Exception("Database Name is None")
        db = client[DB_NAME]

        existing = await db.list_collection_names()

        # Create missing collections
        for collection in COLLECTIONS:
            if collection not in existing:
                await db.create_collection(collection)

        # Re-collections to confirm
        existing = await db.list_collection_names()

        if all(collection in existing for collection in COLLECTIONS):
            print("Collections presence established")

    except Exception as e:
        print("Error establishing database collections: ", e)
