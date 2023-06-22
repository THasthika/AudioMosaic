from pydantic import BaseModel
from uuid import UUID


class LabelBase(BaseModel):
    name: str
    description: str
    color: str


class LabelCreate(LabelBase):
    dataset_id: UUID | None
    description: str | None


class LabelUpdate(LabelBase):
    name: str | None
    description: str | None
    color: str | None


class LabelItem(LabelBase):
    id: UUID

    class Config:
        orm_mode = True
