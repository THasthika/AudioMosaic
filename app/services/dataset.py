from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseService
from app.schemas import DatasetCreate, DatasetQuery, DatasetItem, DatasetUpdate
from app.repositories import DatasetRepository
from app.utils.service_result import ServiceResult
import app.exceptions.dataset as dataset_exceptions
from app.exceptions.base import AppExceptionCase
from app.schemas.generics import PaginatedResponse


class DatasetService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.dataset_repo = DatasetRepository(self.db)

    def create_dataset(self, create_dataset: DatasetCreate) -> ServiceResult:
        try:
            created_dataset = self.dataset_repo.create(create_dataset)
            return ServiceResult(DatasetItem.from_orm(created_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetCreateFailed())

    def list_datasets(self, query: DatasetQuery) -> ServiceResult:
        try:
            (datasets, total) = self.dataset_repo.get_paginated_list(
                query.offset, query.limit
            )
            count = len(datasets)
            datasets = list(map(lambda x: DatasetItem.from_orm(x), datasets))
            return ServiceResult(
                PaginatedResponse(count=count, total=total, items=datasets)
            )
        except Exception as e:
            print(e)
            # TODO: Make the exception more refined
            return ServiceResult(
                dataset_exceptions.AppExceptionCase(500, None)
            )

    def update_dataset(
        self, id: UUID, update_dataset: DatasetUpdate
    ) -> ServiceResult:
        try:
            updated_dataset = self.dataset_repo.update(id, update_dataset)
            return ServiceResult(DatasetItem.from_orm(updated_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetUpdateFailed())

    def delete_dataset(self, id: UUID) -> ServiceResult:
        try:
            deleted_dataset = self.dataset_repo.delete(id)
            return ServiceResult(DatasetItem.from_orm(deleted_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetDeleteFailed())

    def get_dataset(self, id: UUID) -> ServiceResult:
        try:
            dataset = self.dataset_repo.get_by_id(id)
            return ServiceResult(DatasetItem.from_orm(dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetNotFound())
