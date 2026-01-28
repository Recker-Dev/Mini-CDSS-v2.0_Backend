from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from app.core.setup import database_setup_ops
from app.api.doctors import router as doctor_router
from app.api.sessions import router as session_router
from app.core.config import ORIGINS
from app.models.error import UserFacingError
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database_setup_ops()
    yield

    # shutdown
    # await cleanup_ops()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##########################
# 400 -> UserErrors
# 422 -> Pydantic
# 500 -> Server
##########################

## Handles the errors that the User is supposed to see with code 400
@app.exception_handler(UserFacingError)
async def user_facing_error_handler(_, exc: UserFacingError):
    return JSONResponse(
        status_code=400, content={"message": "User Error", "detail": exc.detail}
    )


## Handles pydantic request level validation errors (Entry Point Trigger -> we happy if happens)
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "details": [
                {
                    "field": ".".join(map(str, err["loc"][1:])),
                    "message": err["msg"],
                }
                for err in exc.errors()
            ],
        },
    )


## Handles pydantic validation errors (Might Happen in between code -> we sad if happens)
@app.exception_handler(ValidationError)
async def validation_error_handler(_, exc: ValidationError):

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "details": [
                {
                    "field": ".".join(map(str, err["loc"])),
                    "message": err["msg"],
                }
                for err in exc.errors()
            ],
        },
    )


## Handles Generic Exceptions (All Errors are Exceptions)
@app.exception_handler(Exception)
async def generic_exception_handler(_, exc: Exception):
    print(f"Exception Raised: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Server Error", "detail": exc}, # <- Should not be leaking error only logging; kept for now.
    )



app.include_router(doctor_router)
app.include_router(session_router)


@app.get("/")
async def status():
    return {"Online"}
