from langgraph.graph import StateGraph, END, START
from langgraph.types import RetryPolicy
import time
from app.models.graph import MiniCDSSState, DifferentialDiagnosisAgentOutput
from app.ai.differential import carry_diagnosis
from app.ai.evidence import audit_evidence
from app.ai.diagnosis import audit_diagnoses


async def differential_diagnosis_node(state: MiniCDSSState):
    node_name = "differential_diagnosis_agent"
    starttime = time.perf_counter()
    print("\n" + "=" * 60)
    print("---DIFFERENTIAL DIAGNOSIS NODE---")
    try:
        result = await carry_diagnosis(
            last_mutation_source="UI",
            positive_evidence=[entry.model_dump() for entry in state.positive_evidence],
            negative_evidence=[entry.model_dump() for entry in state.negative_evidence],
            diagnoses=[entry.model_dump() for entry in state.diagnoses],
            reasoning_chain=[entry.model_dump() for entry in state.reasoning_chain],
            diagnosis_summary=state.diagnosis_summary,
            diagnosis_strategy=(
                state.diagnosis_strategy.model_dump()
                if state.diagnosis_strategy
                else {}
            ),
            doctor_last_chat=state.doctor_last_chat,
            evidence_delta=[entry.model_dump() for entry in state.evidence_delta],
            diagnoses_delta=[entry.model_dump() for entry in state.diagnoses_delta],
        )

        duration = round(time.perf_counter() - starttime, 3)

        return {"differential_diagnosis_output": result}

    except Exception as e:
        duration = round(time.perf_counter() - starttime, 3)
        print(f"{node_name} failed after {duration}s")
        raise e  ## Re-raise


async def evidence_audit_node(state: MiniCDSSState):
    node_name = "evidence_audit_agent"
    starttime = time.perf_counter()
    print("\n" + "=" * 60)
    print("---EVIDENCE AUDIT AND BUILDER NODE---")
    if (
        state.differential_diagnosis_output is None
        or state.differential_diagnosis_output.evidence_auditer_meta.should_run == False
    ):
        print(
            f"-- Exiting {node_name}. As no differential diagnosis agent state or command passed. --"
        )
        return None

    try:

        result = await audit_evidence(
            differential_diagnosis_output=state.differential_diagnosis_output,
            initial_patient_notes=state.initial_patient_notes,
            positive_evidence=[entry.model_dump() for entry in state.positive_evidence],
            negative_evidence=[entry.model_dump() for entry in state.negative_evidence],
            diagnoses=[entry.model_dump() for entry in state.diagnoses],
            reasoning_chain=[entry.model_dump() for entry in state.reasoning_chain],
            diagnosis_summary=state.diagnosis_summary,
            diagnosis_strategy=(
                state.diagnosis_strategy.model_dump()
                if state.diagnosis_strategy
                else {}
            ),
            evidence_delta=[entry.model_dump() for entry in state.evidence_delta],
            diagnoses_delta=[entry.model_dump() for entry in state.diagnoses_delta],
        )

        duration = round(time.perf_counter() - starttime, 3)

        return {"evidence_audit_output": result}

    except Exception as e:
        duration = round(time.perf_counter() - starttime, 3)
        print(f"{node_name} failed after {duration}s")
        raise e  ## Re-raise


async def diagnosis_audit_node(state: MiniCDSSState):
    node_name = "diagnosis_audit_agent"
    starttime = time.perf_counter()
    print("\n" + "=" * 60)
    print("---DIAGNOSIS AUDIT AND BUILDER NODE---")
    if (
        state.differential_diagnosis_output is None
        or state.differential_diagnosis_output.diagnosis_auditer_meta.should_run
        == False
    ):
        print(
            f"-- Exiting {node_name}. As no differential diagnosis agent state or command passed. --"
        )
        return None

    try:

        result = await audit_diagnoses(
            differential_diagnosis_output=state.differential_diagnosis_output,
            initial_patient_notes=state.initial_patient_notes,
            positive_evidence=[entry.model_dump() for entry in state.positive_evidence],
            negative_evidence=[entry.model_dump() for entry in state.negative_evidence],
            diagnoses=[entry.model_dump() for entry in state.diagnoses],
            reasoning_chain=[entry.model_dump() for entry in state.reasoning_chain],
            diagnosis_summary=state.diagnosis_summary,
            diagnosis_strategy=(
                state.diagnosis_strategy.model_dump()
                if state.diagnosis_strategy
                else {}
            ),
            evidence_delta=[entry.model_dump() for entry in state.evidence_delta],
            diagnoses_delta=[entry.model_dump() for entry in state.diagnoses_delta],
        )

        duration = round(time.perf_counter() - starttime, 3)

        return {"diagnosis_audit_output": result}

    except Exception as e:
        duration = round(time.perf_counter() - starttime, 3)
        print(f"{node_name} failed after {duration}s")
        raise e  ## Re-raise


# Create the graph
graph = StateGraph(MiniCDSSState)

# Build the Nodes
graph.add_node(
    "Differential Diagnosis Agent",
    differential_diagnosis_node,
    retry_policy=RetryPolicy(max_attempts=2),
)
graph.add_node(
    "Evidence Builder and Auditer Agent",
    evidence_audit_node,
    retry_policy=RetryPolicy(max_attempts=2),
)
graph.add_node(
    "Diagnosis Builder and Auditer Agent",
    diagnosis_audit_node,
    retry_policy=RetryPolicy(max_attempts=2),
)


# Connect the Edges
graph.add_edge(START, "Differential Diagnosis Agent")
graph.add_edge("Differential Diagnosis Agent", "Evidence Builder and Auditer Agent")
graph.add_edge(
    "Evidence Builder and Auditer Agent", "Diagnosis Builder and Auditer Agent"
)
graph.add_edge("Diagnosis Builder and Auditer Agent", END)


compiled_graph = graph.compile()
