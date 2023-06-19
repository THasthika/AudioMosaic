from pydantic import BaseModel
from uuid import UUID


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    dataset_id: UUID | None


class LabelUpdate(LabelBase):
    name: str | None


class LabelItem(LabelBase):
    id: UUID
    dataset_id: UUID

    class Config:
        orm_mode = True
