from dotenv import load_dotenv
import os

load_dotenv()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


MONGO_URI = require_env("MONGO_URI")
DB_NAME = require_env("DATABASE_NAME")
ORIGINS = [
    origin.strip() for origin in require_env("ORIGINS").split(",") if origin.strip()
]


DOCTOR_COLLECTION = "doctors"
PATIENT_COLLECTION = "patients"
SESSION_COLLECTION = "sessions"
COLLECTIONS = [DOCTOR_COLLECTION, PATIENT_COLLECTION, SESSION_COLLECTION]
