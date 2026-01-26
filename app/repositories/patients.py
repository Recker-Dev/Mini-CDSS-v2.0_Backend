from app.db.collections import get_patient_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.models.patients import PatientInDB


async def insert_patient(patient: PatientInDB, session=None) -> str:
    collection = get_patient_collection()

    doc = patient.model_dump(by_alias=True, exclude_none=True)
    _id = doc.get("_id")
    if _id and isinstance(_id, str):
        doc["_id"] = ObjectId(_id)

    result = await collection.insert_one(doc)
    return str(result.inserted_id)


async def delete_patient_by_id(pat_id: str) -> PatientInDB | None:

    try:
        oid = ObjectId(pat_id)
    except InvalidId:
        return None

    collection = get_patient_collection()
    result = await collection.find_one_and_delete({"_id": oid})

    return PatientInDB.model_validate(result) if result else None
