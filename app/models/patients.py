from datetime import datetime, timezone
from typing import List, Literal, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


## Shared by all
class PatientBase(BaseModel):
    name: str
    age: int
    gender: Literal["Male", "Female", "Non-binary", "Other", "Unknown"]


## Patient Creation
class PatientCreate(PatientBase):
    pass


## "Source of Truth" in MongoDB
class PatientInDB(PatientBase):
    model_config = ConfigDict(validate_by_name=True)  ## Enables Mapping
    id: Optional[str] = (
        Field(  # Maps "_id" from Mongo to `id` field ; but returns as "id" when serialized
            default=None, alias="_id", serialization_alias="id", validation_alias="_id"
        )
    )

    chronic_conditions: Optional[List[str]] = []
    past_medical_history: Optional[List[str]] = []

    @field_validator("id", mode="before")
    @classmethod
    def covert_objectid(cls, value):  ## Converts the id which will be ObjectId to str.
        if isinstance(value, ObjectId):
            return str(value)
        return value


## Public Profile (No sensitive data)
class PatientPublic(PatientInDB):
    pass
