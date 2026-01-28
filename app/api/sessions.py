from app.models.sessions import SessionCreate
from app.services.sessions import (
    create_session,
    delete_session,
    get_session,
    get_sessions_for_docid,
)


from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("")
async def create_session_endpoint(session: SessionCreate):
    return await create_session(session)


@router.delete("/{ses_id}")
async def delete_session_endpoint(ses_id: str):
    return await delete_session(ses_id)


@router.get("/{ses_id}")
async def get_session_endpoint(ses_id: str):
    return await get_session(ses_id)

@router.get("/doctor/{doc_id}")
async def get_sessions_for_doctor_endpoint(doc_id: str):
    return await get_sessions_for_docid(doc_id)

