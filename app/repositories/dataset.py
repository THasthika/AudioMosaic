from sqlalchemy.orm import Session
from .base import BaseCRUDRepository
from app.exceptions.dataset import DatasetNotFound
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate


class DatasetRepository(BaseCRUDRepository):
    ModelType = Dataset
    ModelCreateType = DatasetCreate
    ModelUpdateType = DatasetUpdate

    ItemNotFoundException = DatasetNotFound

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_model_from_create_type(
        self, create_type: ModelCreateType
    ) -> ModelType:
        return Dataset(name=create_type.name)

    def get_model_from_update_type(
        self, current_model: ModelType, update_model: ModelUpdateType
    ) -> ModelType:
        if update_model.name is not None:
            current_model.name = update_model.name

        return current_model

    def get_paginated_list(self, offset: int, limit: int):
        total = self.db.query(Dataset).count()

        datasets = self.db.query(Dataset).offset(offset).limit(limit).all()

        return (datasets, total)
