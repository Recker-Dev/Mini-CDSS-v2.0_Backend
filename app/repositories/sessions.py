from typing import List
import pymongo
from app.db.collections import get_session_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.models.sessions import SessionBase, SessionInDB, SessionCreate


async def find_session_by_id(ses_id: str) -> SessionInDB | None:
    ## Validates the objectId
    try:
        oid = ObjectId(ses_id)
    except InvalidId:
        return None

    collection = get_session_collection()
    result = await collection.find_one({"id": oid})

    return SessionInDB.model_validate(result) if result else None


async def find_sessions_by_docid(doc_id: str) -> List[SessionInDB] | None:
    ## Validates the objectId
    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        return None

    collection = get_session_collection()

    cursor = collection.find({"doc_id": oid}).sort("last_activity", pymongo.DESCENDING)

    results = await cursor.to_list(length=1000)

    ## Parse the results
    sessions = [SessionInDB.model_validate(ses) for ses in results]

    return sessions if len(sessions) != 0 else None


async def insert_sesion(session: SessionInDB, session_ctx=None) -> str:
    collection = get_session_collection()

    doc = session.model_dump(exclude_none=True)

    result = await collection.insert_one(doc)

    return str(result.inserted_id)


async def delete_session_by_id(ses_id: str) -> SessionInDB | None:

    try:
        oid = ObjectId(ses_id)
    except InvalidId:
        return None

    collection = get_session_collection()
    result = await collection.find_one_and_delete({"id": oid})

    return SessionInDB.model_validate(result) if result else None
