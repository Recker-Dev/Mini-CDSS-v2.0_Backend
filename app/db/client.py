from pymongo import AsyncMongoClient
from app.core.config import MONGO_URI

client: AsyncMongoClient | None = None


def get_client():
    global client
    if client is None:
        client = AsyncMongoClient(MONGO_URI)
    return client
