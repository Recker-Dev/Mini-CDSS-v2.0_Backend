from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from app.core.config import GOOGLE_API_KEY
from app.models.sessions import SessionEligibilityResult
import json


def format_session_creation_context(age: int, gender: str, note: str) -> str:
    return f"""
    Patient Age: {age}
    Patient Gender: {gender}
    Patient Note: \n\n {note} """.strip()


SESSION_CREATION_VALIDATION_PROMPT = """
You are a medical intake validation assistant.

Your task is to determine whether the provided patient information
is sufficient and relevant to begin a medical diagnosis session.

Rules:
- You are NOT diagnosing
- You are ONLY judging information quality and relevance
- The note must contain symptoms, complaints, or medical context
- Vague, empty, or irrelevant notes should be rejected

=========================

{PATIENT_DETAILS}

=========================

Return ONLY valid JSON with:
{{
  "eligible": boolean,
  "reasoning": string
}}
"""


def validate_content_before_session_creation(age: int, gender: str, note: str) -> SessionEligibilityResult:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GOOGLE_API_KEY,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        response_mime_type="application/json",
        response_schema=SessionEligibilityResult.model_json_schema(),
    )

    formatted_payload = format_session_creation_context(age, gender, note)

    # Prepare the input for the prompt
    prompt_load = {
        "PATIENT_DETAILS": formatted_payload,
    }

    # Format the prompt using the template
    prompt = SESSION_CREATION_VALIDATION_PROMPT.format(**prompt_load)

    # Invoke the LLM with the formatted prompt
    response = llm.invoke(prompt)

    if not isinstance(response.content, str):
        raise TypeError(f"Expected JSON string, got {type(response.content)}")


    return SessionEligibilityResult.model_validate_json(response.content)


    
