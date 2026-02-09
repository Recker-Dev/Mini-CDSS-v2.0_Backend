from enum import Enum
from typing import Literal, Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from datetime import datetime


class ClinicalMetric(BaseModel):
    """Internal scores for AI reasoning."""

    confidence: float = Field(ge=0, le=1, description="Probability score 0.0-1.0")
    support_score: float = Field(description="How much positive evidence supports this")
    conflict_score: float = Field(
        description="How much negative evidence contradicts this"
    )


class RelevanceStatus(str, Enum):
    """Marks if a Evidence is still relevant"""

    ACTIVE = "Active"
    REDUNDANT = "Redundant"


class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: f"ev_{int(datetime.now().timestamp())}")
    creator: Literal["Doctor", "AI"]
    content: str
    clinical_type: Literal["Symptom", "Sign", "Lab", "History"]
    reasoning: str = Field(
        default_factory=str,
        description="Brief description as to why and how this evidence came into existence",
    )
    relevance: RelevanceStatus = RelevanceStatus.ACTIVE


class Diagnosis(BaseModel):
    id: str = Field(default_factory=lambda: f"diag_{int(datetime.now().timestamp())}")
    name: str = Field(description="Name of the suggested Diagnosis")
    creator: Literal["Doctor", "AI"]
    metrics: ClinicalMetric
    reasoning: str = Field(
        description="Doctor-authored reasoning is authoritative; AI reasoning applies only to AI diagnoses"
    )
    supporting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="Evidence ids of the positive evidences that suggest this diagnosis",
    )
    conflicting_evidence_ids: list[str] = Field(
        default_factory=list,
        description="Evidence ids of the negative evidences that contradicts this diagnosis",
    )
    relevance: RelevanceStatus = RelevanceStatus.ACTIVE


class ReasoningStep(BaseModel):
    thought: str = Field(
        description="Concise clinical justification for the chosen action (decision-level, non-deliberative)"
    )
    action_taken: Literal[
        "Trigger Diagnosis Auditer",
        "Trigger Evidence Auditer",
        "Trigger Both",
        "Request Clarification",
    ]


class DiagnosticStrategy(BaseModel):
    next_question: Optional[str] = None
    differential_status: Literal["Expanding", "Narrowing", "Stable"] = Field(
        default="Expanding",
        description="Current Strategy of diagnosis based on current state and state delta",
    )

    summary: str = Field(
        default_factory=str,
        description="High-level clinical summary of the current case",
    )


class EvidenceDelta(BaseModel):
    """Tracks changes in evidence between states."""

    added: list[Evidence] = Field(
        default_factory=list,
        description="List of new evidences that have been added by doctor since last state",
    )
    removed: list[Evidence] = Field(
        default_factory=list,
        description="List of evidences that have been removed by doctor since last state",
    )


class DiagnosesDelta(BaseModel):
    """Tracks changes in diagnoses between states"""

    added: list[Diagnosis] = Field(
        default_factory=list,
        description="List of new Diagnoses that have been added by doctor since last state",
    )

    removed: list[Diagnosis] = Field(
        default_factory=list,
        description="List of Diagnoses that have been removed by doctor since last state",
    )


class EvidenceAuditerMeta(BaseModel):
    should_run: bool

    # Why the builder is running
    reasons: list[
        Literal[
            "Implicit Evidence Update",
            "Implicit Extraction",
            "Redundancy Check",
            "Doctor Advisory",
        ]
    ] = Field(default_factory=list)

    # What kind of evidence is needed
    target_clinical_types: list[Literal["Symptom", "Sign", "Lab", "History"]] = []

    implicit_sources: list[Literal["DoctorChat", "InitialNotes"]] = Field(
        default_factory=list,
        description="Informs about the source of the to be created evidences",
    )

    allowed_actions: list[
        Literal[
            "CreateImplicitEvidence",
            "UpdateAIEvidence",
            "MarkAIRedundant",
            "GenerateDoctorAdvisory",
        ]
    ] = Field(
        default_factory=list,
        description="Meta-data for Auditer and Builder Agent as to what tasks it needs to perform",
    )

    to_be_updated_evidence_ids: list[str] = Field(
        default_factory=list,
        description="List of all the AI created evidence Id's that need updation",
    )

    to_be_redundant_evidence_ids: list[str] = Field(
        default_factory=list,
        description="List of all the AI created evidence Id's that need to be made redundant",
    )

    objective: str = Field(
        default_factory=str,
        description="Explicit clear and brief objective for guidance of evidence maintenance, evidence building or/and creation of doctor advisory",
    )


class DiagnosisAuditerMeta(BaseModel):
    should_run: bool

    reasons: list[
        Literal[
            "No Diagnosis",
            "Diagnosis Stale",
            "Evidence-Driven Update",
            "Doctor Diagnosis Review",
        ]
    ] = []

    # Which diagnoses to focus on
    focus_diagnosis_ids: list[str] = Field(
        default_factory=list, description="Diagnosis IDs in scope for this auditer run"
    )

    allowed_actions: list[
        Literal[
            "CreateAIDiagnosis",
            "UpdateAIDiagnosis",
            "AttachEvidence",
            "UpdateConfidenceMetrics",
            "MarkAIRedundant",
            "GenerateDoctorAdvisory",
        ]
    ] = Field(
        default_factory=list,
        description="Explicitly permitted diagnosis auditer actions",
    )

    to_be_updated_ai_diagnosis_ids: list[str] = Field(
        default_factory=list, description="AI diagnosis IDs that may be updated"
    )

    to_be_redundant_ai_diagnosis_ids: list[str] = Field(
        default_factory=list,
        description="AI diagnosis IDs that may be marked redundant",
    )

    objective: str = Field(
        default_factory=str,
        description="Explicit clear, brief objective guiding diagnosis building, maintenance, evaluation, and scoring",
    )


class EvidenceAuditerOutput(BaseModel):
    # AI-owned evidence lifecycle
    new_ai_evidences: list[Evidence] = Field(
        default_factory=list,
        description="New implicit evidences that are created from chat or notes",
    )

    updated_ai_evidences: list[Evidence] = Field(
        default_factory=list,
        description="AI evidences updated or refined based on new information",
    )

    redundant_ai_evidence_ids: list[str] = Field(
        default_factory=list, description="AI-created evidences that are now redundant"
    )

    # Doctor-facing advisory (single surface)
    doctor_advisory_note: str = Field(
        default_factory=str,
        description=(
            "Concise, human-readable guidance for the doctor covering:\n"
            "- Which explicit evidences would help\n"
            "- Which existing doctor's evidences may be weak, redundant, or conflicting\n"
            "- Why these matter diagnostically\n"
            "This is advisory only and never mutates doctor data."
        ),
    )


class DiagnosisEvaluationNote(BaseModel):
    diagnosis_id: str

    assessment: str = Field(
        description=(
            "Concise, doctor-facing evaluation of this diagnosis, covering:\n"
            "- Concerns, gaps, or inconsistencies\n"
            "- Missing or conflicting evidence\n"
            "- Why this impacts diagnostic confidence\n"
            "Advisory only; does not alter diagnosis content."
        )
    )


class DiagnosisAuditerOutput(BaseModel):
    # Creation
    new_ai_diagnoses: list[Diagnosis] = Field(
        default_factory=list, description="List of new AI-created diagnoses"
    )
    # AI diagnosis updates
    updated_ai_diagnoses: list[Diagnosis] = Field(
        default_factory=list,
        description="List of updated AI diagnoses (reasoning, evidence links, metrics)",
    )
    # Redundancy (AI only)
    redundant_ai_diagnosis_ids: list[str] = Field(
        default_factory=list, description="List of AI diagnoses to be marked redundant"
    )

    # Universal confidence updates
    confidence_updates: dict[str, ClinicalMetric] = Field(
        default_factory=dict,
        description="Updated confidence metrics for diagnoses (Doctor or AI)",
    )

    # Per-diagnosis evaluation (Doctor or AI)
    diagnosis_evaluations: list[DiagnosisEvaluationNote] = Field(
        default_factory=list,
        description="Per-diagnosis advisory evaluations for UI display",
    )


class DifferentialDiagnosisAgentOutput(BaseModel):
    current_reasoning_step: ReasoningStep
    strategy: DiagnosticStrategy = Field(default_factory=DiagnosticStrategy)
    diagnosis_summary: str = Field(
        default_factory=str,
        description="Detailed Summary of differential diagnosis up until this point",
    )
    evidence_auditer_meta: EvidenceAuditerMeta
    diagnosis_auditer_meta: DiagnosisAuditerMeta
    trigger_rationale: str = Field(
        default_factory=str,
        description=(
            "High-level explanation of why the brain decided to trigger "
            "or not trigger downstream auditers."
        ),
    )


class MiniCDSSState(BaseModel):
    # Core Data From DB/Redis
    initial_patient_notes: str = Field(
        default_factory=str,
        description="Initial Patient Notes collected before session starts",
    )
    diagnosis_summary: str = Field(
        default_factory=str,
        description="Summary of the current diagnosis",
    )
    doctor_last_chat: str = Field(
        default_factory=str,
        description="The last chat entry from doctor if UI_Chat is used as entry point",
    )

    positive_evidence: list[Evidence] = []
    negative_evidence: list[Evidence] = []
    diagnoses: list[Diagnosis] = []
    reasoning_chain: list[ReasoningStep] = []
    diagnosis_strategy: DiagnosticStrategy | None = None

    # State Diffs (The 'What changed this turn' layer)
    last_mutation_source: Literal["UI", "Start_Diagnosis"] = "Start_Diagnosis"
    evidence_delta: list[EvidenceDelta] = Field(
        default_factory=list,
        description="Change of evidences since last state snapshot",
    )
    diagnoses_delta: list[DiagnosesDelta] = Field(
        default_factory=list,
        description="Change of diagnoses since last state snapshot",
    )

    # State machines
    differential_diagnosis_output: DifferentialDiagnosisAgentOutput | None = None
    evidence_audit_output: EvidenceAuditerOutput | None = None
    diagnosis_audit_output: DiagnosisAuditerOutput | None = None
