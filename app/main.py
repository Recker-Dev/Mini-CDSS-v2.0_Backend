from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.setup import database_setup_ops
from app.api.doctors import router as doctor_router
from app.api.sessions import router as session_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database_setup_ops()
    yield

    # shutdown
    # await cleanup_ops()


app = FastAPI(lifespan=lifespan)
app.include_router(doctor_router)
app.include_router(session_router)


@app.get("/")
async def status():
    return {"Online"}
