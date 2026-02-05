from app.redis.client import get_client


async def check_redis_collection() -> bool:
    try:
        client = get_client()
        if client.ping():
            client.set("foo", "bar")
            if client.get("foo") == "bar":
                client.delete("foo")
                print("Redis Connection successful and Tested")
                return True
            else:
                print("Redis test key mismatch")
                return False
        else:
            print("Redis ping failed")
            return False

    except Exception as e:
        print("Redis Connection error: ", e)
        return False
