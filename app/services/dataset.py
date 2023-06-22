from uuid import UUID

from .base import BaseService
from app.models import Dataset
from app.schemas import DatasetCreate, DatasetQuery, DatasetItem, DatasetUpdate
from app.repositories import DatasetRepository
from app.utils.service_result import ServiceResult
import app.exceptions.dataset as dataset_exceptions
from app.exceptions.base import AppExceptionCase


class DatasetService(BaseService):
    def create_dataset(self, create_dataset: DatasetCreate) -> ServiceResult:
        try:
            created_dataset = DatasetRepository(self.db).create(create_dataset)
            return ServiceResult(DatasetItem.from_orm(created_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetCreateFailed())

    def list_datasets(self, query: DatasetQuery) -> ServiceResult:
        try:
            datasets = (
                self.db.query(Dataset)
                .offset(query.offset)
                .limit(query.limit)
                .all()
            )
            datasets = list(map(lambda x: DatasetItem.from_orm(x), datasets))
            return ServiceResult(datasets)
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
            updated_dataset = DatasetRepository(self.db).update(
                id, update_dataset
            )
            return ServiceResult(DatasetItem.from_orm(updated_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetUpdateFailed())

    def delete_dataset(self, id: UUID) -> ServiceResult:
        try:
            deleted_dataset = DatasetRepository(self.db).delete(id)
            return ServiceResult(DatasetItem.from_orm(deleted_dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetDeleteFailed())

    def get_dataset(self, id: UUID) -> ServiceResult:
        try:
            dataset = DatasetRepository(self.db).get_by_id(id)
            return ServiceResult(DatasetItem.from_orm(dataset))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(dataset_exceptions.DatasetNotFound())
