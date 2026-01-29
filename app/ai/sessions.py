from app.models.sessions import SessionEligibilityResult, SessionInitializationResult
from app.ai.prompts import (
    SESSION_CREATION_VALIDATION_PROMPT,
    SESSION_DIAGNOSIS_INITIALIZATION_PROMPT,
)
from app.llm.builder import LLMProviderFactory


def format_session_creation_context(age: int, gender: str, note: str) -> str:
    return f"""
    Patient Age: {age}
    Patient Gender: {gender}
    Patient Note: \n\n {note} """.strip()


async def validate_content_before_session_creation(
    age: int, gender: str, note: str
) -> SessionEligibilityResult:

    formatted_payload = format_session_creation_context(age, gender, note)

    # Prepare the input for the prompt
    prompt_load = {
        "PATIENT_DETAILS": formatted_payload,
    }

    # Format the prompt using the template
    prompt = SESSION_CREATION_VALIDATION_PROMPT.format(**prompt_load)

    # Invoke the LLM with the formatted prompt
    llm = LLMProviderFactory.ollama()

    return await llm.invoke(prompt, SessionEligibilityResult)


async def initialize_session_differential_diagnosis(
    age: int, gender: str, note: str
) -> SessionInitializationResult:

    formatted_payload = format_session_creation_context(age, gender, note)

    # Prepare the input for the prompt
    prompt_load = {
        "PATIENT_DETAILS": formatted_payload,
    }

    # Format the prompt using the template
    prompt = SESSION_DIAGNOSIS_INITIALIZATION_PROMPT.format(**prompt_load)

    # Invoke the LLM with the formatted prompt
    llm = LLMProviderFactory.ollama()

    return await llm.invoke(prompt, SessionInitializationResult)
