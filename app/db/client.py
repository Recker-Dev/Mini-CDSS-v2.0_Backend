from pymongo import AsyncMongoClient
from app.core.config import MONGO_URI

_client: AsyncMongoClient | None = None


def get_client():
    global _client
    if _client is None:
        if not MONGO_URI:
            raise Exception("MONGO_URI is not set in environment")
        _client = AsyncMongoClient(MONGO_URI)
    return _client

async def close_connection():
    global _client
    try:
        if _client is not None:
            await _client.close()
            _client = None
            print("Closing DB connection")
    except Exception as e:
        print("Ran into error with closing DB connection: ", e)
