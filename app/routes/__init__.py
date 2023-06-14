from importlib import import_module

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from app.config.app import API_VERSION
from app.config.database import get_db

api = import_module(f".{API_VERSION}", package="app.routes")
router = APIRouter()


@router.get(
    "/db-version",
    response_model=dict,
    tags=["Healthcheck"],
)
async def db_version(session: Session = Depends(get_db)):
    version = session.execute(text("select sqlite_version()")).first()[0]

    return {"version": version}


router.include_router(api.router, prefix=f"/{API_VERSION}")
