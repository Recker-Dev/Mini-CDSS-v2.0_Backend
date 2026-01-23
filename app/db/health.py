from app.db.client import get_client


async def check_mongo_connect() -> bool:
    client = get_client()
    try:
        await client.admin.command("ping")
        print(" Database Connection successful")
        return True
    except Exception as e:
        print("Database Connection failed: ", e)
        return False
