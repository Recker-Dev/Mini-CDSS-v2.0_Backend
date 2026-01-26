from datetime import datetime, timezone
from typing import List, Literal, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


## Shared by all
class SessionBase(BaseModel):
    pat_name: str
    pat_age: int
    pat_gender: Literal["Male", "Female", "Non-binary", "Other", "Unknown"]
    pat_note: str


## Patient Creation
class SessionCreate(SessionBase):
    doc_id: str


## "Source of Truth" in MongoDB
class SessionInDB(SessionBase):
    model_config = ConfigDict(validate_by_name=True)  ## Enables Mapping
    id: Optional[str] = (
        Field(  # Maps "_id" from Mongo to `id` field ; but returns as "id" when serialized
            default=None, alias="_id", serialization_alias="id", validation_alias="_id"
        )
    )

    doc_id: str
    pat_id: str
    chronic_conditions: Optional[str] = "To be discovered.."
    status: Optional[Literal["Critical", "Stable", "Follow-up"]] = "Follow-up"

    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("id", "doc_id", "pat_id", mode="before")
    @classmethod
    def covert_objectid(cls, value):  ## Converts the id which will be ObjectId to str.
        if isinstance(value, ObjectId):
            return str(value)
        return value


## Public Profile (No sensitive data)
class SessionPublic(SessionInDB):
    pass
