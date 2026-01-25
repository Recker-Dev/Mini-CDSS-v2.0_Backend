from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.setup import database_setup_ops


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database_setup_ops()
    yield

    # shutdown
    # await cleanup_ops()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def ping():
    return {"pong"}


# @app.post("/create-doc")