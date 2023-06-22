from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import router
from app.config.app import (
    API_VERSION,
    DEBUG,
    PROJECT_NAME,
    ROOT_PATH,
    APP_DIST_PATH,
)
from app.exceptions.base import AppExceptionCase
from app.utils.request_exceptions import (
    request_validation_exception_handler,
    http_exception_handler,
)
from app.exceptions.base import app_exception_handler

# setup logging
import logging

# TODO: make it better later
logging.basicConfig(level=logging.DEBUG,
                    format='%(relativeCreated)6d %(threadName)s %(message)s')

app = FastAPI(
    root_path=ROOT_PATH,
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
    description="Audio Dataset Manager",
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(router)

# frontend
app.mount(
    "/", StaticFiles(directory=APP_DIST_PATH, html=True), name="Frontend App"
)
