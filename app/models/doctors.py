from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


## Used for Login & shared by all
class DoctorBase(BaseModel):
    email: EmailStr


## Login for Doctor
class DoctorLogin(DoctorBase):
    password: str


## Account Creation (Internal/Admin use)
class DoctorCreate(DoctorBase):
    name: str
    password: str
    speciality: Optional[str] = Field(default="")


## "Source of Truth" in MongoDB
class DoctorInDB(DoctorBase):
    model_config = ConfigDict(validate_by_name=True) ## Enables Mapping
    id: Optional[str] = (
        Field(  # Maps "_id" from Mongo to `id` field ; but returns as "id" when serialized
            default=None, alias="_id", serialization_alias="id", validation_alias="_id"
        )
    )
    name: str
    hashed_password: str
    speciality: str = ""
    total_sessions_count: int = 0
    active_sessions_count: int = 0

    @field_validator("id", mode="before")
    @classmethod
    def covert_objectid(cls, value):  ## Converts the id which will be ObjectId to str.
        if isinstance(value, ObjectId):
            return str(value)
        return value


## Public Profile (No sensitive data)
class DoctorPublic(DoctorInDB):
    hashed_password: str = Field(exclude=True)


class AuthResult(BaseModel):
    id: str
    name: str  
    authenticated: bool = True
