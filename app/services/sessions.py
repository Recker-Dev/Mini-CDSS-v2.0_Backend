from typing import List

from bson import ObjectId
from app.models.sessions import SessionCreate, SessionPublic, SessionInDB
from app.models.patients import PatientCreate, PatientInDB
from app.repositories.sessions import (
    delete_session_by_id,
    find_session_by_id,
    find_sessions_by_docid,
    insert_sesion,
)
from app.repositories.doctors import find_doctor_by_id
from app.repositories.patients import insert_patient
from app.db.client import get_client


async def create_session(data: SessionCreate) -> SessionPublic:

    ## Verify that doc_id exist as a valid entry
    if await find_doctor_by_id(data.doc_id) is None:
        raise ValueError(f"{data.doc_id} doctor not found")

    ## (Later to be reformed when working towards a centralized patient collection -> for now trigger new patient creation)
    new_patient_id = str(ObjectId())
    new_session_id = str(ObjectId())

    patient_obj = PatientInDB(
        _id=new_patient_id,
        name=data.pat_name,
        age=data.pat_age,
        gender=data.pat_gender,
    )

    ## Proceed with insertion of a new session
    session_obj = SessionInDB(
        _id=new_session_id, pat_id=new_patient_id, **data.model_dump()
    )

    ## Commence transaction
    async with get_client().start_session() as s:
        async with await s.start_transaction():
            await insert_patient(patient_obj, session=s)
            await insert_sesion(session_obj, session=s)

    return SessionPublic.model_validate(session_obj, from_attributes=True)


async def get_session(ses_id: str) -> SessionPublic:
    existing = await find_session_by_id(ses_id)

    if existing is None:
        raise ValueError(f"{ses_id} session not found")

    return SessionPublic.model_validate(existing.model_dump())


async def get_sessions_for_docid(doc_id: str) -> List[SessionPublic]:
    exising_sessions = await find_sessions_by_docid(doc_id)
    if exising_sessions is None:
        raise ValueError(f"No sessions found")

    return [
        SessionPublic.model_validate(session, from_attributes=True)
        for session in exising_sessions
    ]


async def delete_session(ses_id: str) -> SessionPublic:
    deleted_session = await delete_session_by_id(ses_id)

    if deleted_session is None:
        raise ValueError(f"{ses_id} session not found")

    return SessionPublic.model_validate(deleted_session.model_dump())
