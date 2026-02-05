from dotenv import load_dotenv
import os

load_dotenv()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


### LOAD THE NECESSARY ENV VARS
MONGO_URI = require_env("MONGO_URI")
REDIS_URI = require_env("REDIS_URI")
DB_NAME = require_env("DATABASE_NAME")
ORIGINS = [
    origin.strip() for origin in require_env("ORIGINS").split(",") if origin.strip()
]
GOOGLE_API_KEY = require_env("GOOGLE_API_KEY")
GROQ_API_KEY = require_env("GROQ_API_KEY")
OLLAMA_MODEL = require_env("OLLAMA_MODEL")
GOOGLE_MODEL = require_env("GOOGLE_MODEL")
GROQ_MODEL = require_env("GROQ_MODEL")

### STATIC COLLECTION NAMES
DOCTOR_COLLECTION = "doctors"
PATIENT_COLLECTION = "patients"
SESSION_COLLECTION = "sessions"
COLLECTIONS = [DOCTOR_COLLECTION, PATIENT_COLLECTION, SESSION_COLLECTION]
