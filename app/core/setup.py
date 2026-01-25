from app.db.health import check_mongo_connect, ensure_databases, ensure_collections

async def database_setup_ops():
    await check_mongo_connect()
    await ensure_databases()
    await ensure_collections()