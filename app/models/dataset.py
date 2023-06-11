from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel


class DatasetBase(SQLModel):
    name: str


class Dataset(DatasetBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)


class DatasetCreate(DatasetBase):
    pass
