from typing import List

from bson import ObjectId
from app.models.sessions import (
    SessionInDB,
    SessionCreate,
    SessionPublicDeep,
    SessionPublicSparse,
)
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
from app.ai.sessions import validate_content_before_session_creation
from app.models.error import UserFacingError


async def create_session(data: SessionCreate) -> SessionPublicDeep:

    ## Verify that doc_id exist as a valid entry
    if await find_doctor_by_id(data.doc_id) is None:
        raise UserFacingError(f"{data.doc_id} doctor not found")

    ## (Later to be reformed when working towards a centralized patient collection -> for now trigger new patient creation)
    doc_obj_id = ObjectId(data.doc_id)
    new_patient_id = ObjectId()
    new_session_id = ObjectId()

    patient_obj = PatientInDB(
        id=new_patient_id,
        name=data.pat_name,
        age=data.pat_age,
        gender=data.pat_gender,
    )

    decision = validate_content_before_session_creation(
        data.pat_age, data.pat_gender, data.pat_note
    )
    if not decision.eligible:
        raise UserFacingError(decision.reasoning)

    ## Proceed with insertion of a new session
    session_db = SessionInDB(
        id=new_session_id,
        doc_id=doc_obj_id,
        pat_id=new_patient_id,
        **data.model_dump(exclude={"doc_id"}),
    )

    ## Commence transaction
    async with get_client().start_session() as s:
        async with await s.start_transaction():
            # A. Insert Patient
            await insert_patient(
                patient_obj, session_ctx=s
            )  ## It is imp that only the TRUE DB object with all the fileds is inserted here.
            # B. Insert Session (using the raw IDs)
            await insert_sesion(  ## It is imp that only the TRUE DB object with all the fileds is inserted here.
                session_db, session_ctx=s
            )
            # C. Construct and Validate the Return Object INSIDE the transaction (if fail; transaction rollback!)
            return SessionPublicDeep.model_validate(session_db, from_attributes=True)


async def get_session(ses_id: str) -> SessionPublicDeep:
    existing = await find_session_by_id(ses_id)

    if existing is None:
        raise ValueError(f"{ses_id} session not found")

    return SessionPublicDeep.model_validate(existing, from_attributes=True)


async def get_sessions_for_docid(doc_id: str) -> List[SessionPublicSparse]:
    exising_sessions = await find_sessions_by_docid(doc_id)
    if exising_sessions is None:
        raise ValueError(f"No sessions found")

    return [
        SessionPublicSparse.model_validate(session, from_attributes=True)
        for session in exising_sessions
    ]


async def delete_session(ses_id: str) -> SessionPublicDeep:
    deleted_session = await delete_session_by_id(ses_id)

    if deleted_session is None:
        raise ValueError(f"{ses_id} session not found")

    return SessionPublicDeep.model_validate(deleted_session, from_attributes=True)
