from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DatasetBase(BaseModel):
    name: str


class DatasetCreate(DatasetBase):
    pass


class DatasetQuery(DatasetBase):
    name: str | None
    offset: int
    limit: int


class DatasetItem(DatasetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
