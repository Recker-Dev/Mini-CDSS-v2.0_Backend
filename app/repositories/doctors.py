from app.db.collections import get_doctor_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from backend.app.models.doctors import DoctorInDB


async def find_doctor_by_id(doc_id: str) -> DoctorInDB | None:

    ## Validates the objectId
    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        return None

    collection = get_doctor_collection()
    result = await collection.find_one({"_id": oid})

    ## Runs the data through pydantic validation; such that is respects all the necessities defined by the model.
    return DoctorInDB.model_validate(result) if result else None


async def find_doctor_by_email(email: str) -> DoctorInDB | None:
    collection = get_doctor_collection()
    result = await collection.find_one({"email": email})

    return DoctorInDB.model_validate(result) if result else None


async def insert_doctor(doc: DoctorInDB) -> str:
    collection = get_doctor_collection()
    result = await collection.insert_one(
        doc.model_dump(by_alias=True, exclude_none=True)
    )
    return str(result.inserted_id)


async def delete_doctor_by_id(doc_id: str) -> DoctorInDB | None:
    ## Validates the objectId
    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        return None

    collection = get_doctor_collection()
    result = await collection.find_one_and_delete({"_id": oid})

    return DoctorInDB.model_validate(result) if result else None
