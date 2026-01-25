from app.models.doctors import (
    DoctorCreate,
    DoctorInDB,
    DoctorLogin,
    DoctorPublic,
    AuthResult,
)
from app.repositories.doctors import (
    find_doctor_by_email,
    find_doctor_by_id,
    insert_doctor,
    delete_doctor_by_id,
)
from app.core.security import verify_hash, create_hash


async def create_doctor_profile(data: DoctorCreate) -> DoctorPublic:

    ## Check if entry exists.
    if await find_doctor_by_email(data.email):
        raise ValueError("Mail already in use.")

    ## Create a new entry Object
    doctor = DoctorInDB(
        name=data.name,
        email=data.email,
        speciality=data.speciality or "",
        hashed_password=create_hash(data.password),
    )

    new_id = await insert_doctor(doctor)
    doctor.id = new_id
    return DoctorPublic.model_validate(doctor.model_dump())


async def get_doctor_profile(doc_id: str) -> DoctorPublic:

    existing = await find_doctor_by_id(doc_id)
    ## Check if entry exist
    if existing is None:
        raise ValueError(f"{doc_id} not found.")

    return DoctorPublic.model_validate(existing.model_dump())


async def authenticate_user(login_payload: DoctorLogin) -> AuthResult:

    existing = await find_doctor_by_email(login_payload.email)
    if existing is None:
        raise ValueError(f"{login_payload.email} not found.")

    if verify_hash(existing.hashed_password, login_payload.password):
        if existing.id:
            return AuthResult(id=existing.id, name=existing.name, authenticated=True)

    return AuthResult(id="", name="", authenticated=True)


async def delete_doctor_profile(doc_id: str) -> DoctorPublic:

    ## Check if entry exists.
    deleted_result = await delete_doctor_by_id(doc_id)

    if deleted_result is None:
        raise ValueError(f"{doc_id} not found.")

    return DoctorPublic.model_validate(deleted_result.model_dump())
