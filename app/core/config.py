from dotenv import load_dotenv
import os

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DATABASE_NAME")


DOCTOR_COLLECTION = "doctors"
PATIENT_COLLECTION = "patients"
SESSION_COLLECTION = "sessions"
COLLECTIONS = [DOCTOR_COLLECTION, PATIENT_COLLECTION, SESSION_COLLECTION]
