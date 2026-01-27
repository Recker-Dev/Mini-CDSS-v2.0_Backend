from fastapi import APIRouter, HTTPException, status
from app.models.doctors import DoctorCreate, DoctorLogin
from app.services.doctors import (
    authenticate_user,
    create_doctor_profile,
    delete_doctor_profile,
    get_doctor_profile,
)


router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("")
async def create_doctor_profile_endpoint(profile: DoctorCreate):
    try:
        return await create_doctor_profile(profile)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{dod_id}")
async def delete_doctor_profile_endpoint(doc_id: str):
    try:
        return await delete_doctor_profile(doc_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def auth_doctor_login(payload: DoctorLogin):
    try:
        return await authenticate_user(payload)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{doc_id}")
async def get_doctor_profile_endpoint(doc_id: str):

    try:
        return await get_doctor_profile(doc_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
