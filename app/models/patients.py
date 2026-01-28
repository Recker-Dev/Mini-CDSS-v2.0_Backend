from datetime import datetime, timezone
from typing import List, Literal, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.shared import MongoDbId


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
    id: MongoDbId
    chronic_conditions: Optional[List[str]] = []
    past_medical_history: Optional[List[str]] = []



## Public Profile (No sensitive data)
class PatientPublic(PatientInDB):
    pass
