from datetime import datetime
from typing import Annotated, List, Literal, Optional, Any
from bson import ObjectId
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    BeforeValidator,
    field_validator,
)
from app.models.shared import MongoDbId


## Shared by all
class SessionBase(BaseModel):
    pat_name: str
    pat_age: int
    pat_gender: Literal["Male", "Female", "Non-binary", "Other", "Unknown"]
    pat_note: str


class SessionEligibilityResult(BaseModel):
    eligible: bool
    reasoning: str


class SessionInitializationResult(BaseModel):
    positives: List[str] = []
    negatives: List[str] = []
    safety_checklist: list[str] = []
    question: str


## Session Creation
class SessionCreate(SessionBase):
    doc_id: str

    @field_validator("pat_age", mode="after")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age cannot be negative or zero.")
        if value >= 150:
            raise ValueError("Age cannot be more than 150(cuz that will be weird)")
        return value


#### SESSION MODEL DEEP NESTED ####


class Evidence(BaseModel):
    positives: List[str] = []
    negatives: List[str] = []


class DiagnosisEntry(BaseModel):
    id: MongoDbId = Field(default_factory=lambda: ObjectId())
    creator: Literal["AI", "Doctor"]
    disease_name: str
    reasoning: str


class ChatMessages(BaseModel):
    id: MongoDbId = Field(default_factory=lambda: ObjectId())
    sender: Literal["AI", "Doctor"]
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now())


## "Source of Truth" in MongoDB
class SessionInDB(SessionBase):
    model_config = ConfigDict(validate_by_name=True, arbitrary_types_allowed=True)

    id: MongoDbId

    doc_id: MongoDbId
    pat_id: MongoDbId
    complaint: str = "To be discovered.."
    chronic_conditions: List[str] = []

    ## Nested Fields
    evidences: Evidence = Field(default_factory=Evidence)
    diagnoses: List[DiagnosisEntry] = []
    safety_checklist: list[str] = []
    chats: list[ChatMessages] = []

    status: Literal["Critical", "Stable", "Follow-up"] = "Follow-up"

    last_activity: datetime = Field(default_factory=lambda: datetime.now())


## Public Profile - Deep (Full details)
class SessionPublicDeep(SessionInDB):
    """Contains everything from the DB model."""
    pass


class SessionPublicSparse(BaseModel):
    """Minimal view for  dashboards."""

    id: MongoDbId 
    doc_id: MongoDbId
    pat_id: MongoDbId
    complaint: str = "To be discovered..."
    status: Literal["Critical", "Stable", "Follow-up"] = "Follow-up"
    last_activity: datetime = Field(default_factory=lambda: datetime.now())
