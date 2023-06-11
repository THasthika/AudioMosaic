from fastapi import FastAPI
from app.api import router as api_router
from app.core.config import (
    API_VERSION,
    DEBUG,
    PROJECT_NAME,
    ROOT_PATH,
)

app = FastAPI(
    root_path=ROOT_PATH,
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
    description="Audio Dataset Manager",
)
app.include_router(api_router, prefix="/api")
