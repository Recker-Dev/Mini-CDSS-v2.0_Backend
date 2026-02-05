import redis
from redis import Redis
from app.core.config import REDIS_URI

_client: Redis | None = None


def get_client():
    global _client

    if _client is None:
        if not REDIS_URI:
            raise Exception("REDIS_URI is not set in environment")

        _client = redis.from_url(REDIS_URI, decode_responses=True)

    return _client


def close_connection():
    global _client
    try:
        if _client is not None:
            _client.close()
            _client = None
            print("Closing Redis Connection")
    except Exception as e:
        print("Ran into error with closing Redis connection: ", e)
