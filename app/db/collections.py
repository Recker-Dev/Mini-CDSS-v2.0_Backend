from app.core.config import (
    DB_NAME,
    DOCTOR_COLLECTION,
    PATIENT_COLLECTION,
    SESSION_COLLECTION,
)
from app.db.client import get_client


def get_doctor_collection():
    client = get_client()
    if DB_NAME is None or client is None:
        raise Exception("Database client or DB_NAME is not initialized")

    return client[DB_NAME][DOCTOR_COLLECTION]


def get_patient_collection():
    client = get_client()
    if DB_NAME is None or client is None:
        raise Exception("Database client or DB_NAME is not initialized")

    return client[DB_NAME][PATIENT_COLLECTION]


def get_session_collection():
    client = get_client()
    if DB_NAME is None or client is None:
        raise Exception("Database client or DB_NAME is not initialized")

    return client[DB_NAME][SESSION_COLLECTION]
