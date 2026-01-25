from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.setup import database_setup_ops
from app.models.doctors import DoctorCreate, DoctorLogin
from app.services.doctors import (
    authenticate_user,
    create_doctor_profile,
    delete_doctor_profile,
    get_doctor_profile,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database_setup_ops()
    yield

    # shutdown
    # await cleanup_ops()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def status():
    return {"Online"}


@app.post("/createdoc")
async def create_doctor_profile_endpoint(profile: DoctorCreate):
    try:
        return await create_doctor_profile(profile)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deletedoc/{dod_id}")
async def delete_doctor_profile_endpoint(doc_id: str):
    try:
        return await delete_doctor_profile(doc_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def auth_doctor_login(payload: DoctorLogin):
    try:
        return await authenticate_user(payload)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/getdoc/{doc_id}")
async def get_doctor_profile_endpoint(doc_id: str):

    try:
        return await get_doctor_profile(doc_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
