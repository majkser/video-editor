from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.error_handler.error_handler import AppError, NotFoundError
from app.error_handler.error_map import ERROR_MAP
from .api.api import api_router
from .database import Base, engine
from . import models

app = FastAPI()


@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):

    return JSONResponse(
        status_code=ERROR_MAP.get(type(exc), 400), content={"detail": exc.message}
    )


app.include_router(api_router, prefix="/api")

Base.metadata.create_all(bind=engine)
