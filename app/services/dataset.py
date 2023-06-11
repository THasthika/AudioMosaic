from uuid import UUID

from .base import AppService, AppCRUD
from app.utils.app_exceptions import AppExceptionCase
from app.models import Dataset
from app.schemas import (
    DatasetCreate, DatasetQuery, DatasetItem,
    DatasetUpdate
)
from app.utils.service_result import ServiceResult


class DatasetService(AppService):

    def create_dataset(self, create_dataset: DatasetCreate) -> ServiceResult:
        created_dataset = DatasetCRUD(self.db).create_dataset(create_dataset)
        if not created_dataset:
            return ServiceResult(DatasetServiceExceptions
                                 .DatasetCreateFailed())
        return ServiceResult(DatasetItem.from_orm(created_dataset))

    def list_datasets(self, query: DatasetQuery)\
            -> ServiceResult:
        datasets = self.db.query(Dataset).offset(
            query.offset).limit(query.limit).all()
        datasets = list(map(lambda x: DatasetItem.from_orm(x), datasets))
        return ServiceResult(datasets)

    def update_dataset(self, id: UUID, update_dataset: DatasetUpdate)\
            -> ServiceResult:
        updated_dataset = DatasetCRUD(
            self.db).update_dataset(id, update_dataset)
        if not update_dataset:
            return ServiceResult(DatasetServiceExceptions.
                                 DatasetUpdateFailed())
        return ServiceResult(DatasetItem.from_orm(updated_dataset))

    def delete_dataset(self, id: UUID) -> ServiceResult:
        deleted_dataset = DatasetCRUD(self.db).delete_dataset(id)
        if not deleted_dataset:
            return ServiceResult(DatasetServiceExceptions.
                                 DatasetDeleteFailed())
        return ServiceResult(DatasetItem.from_orm(deleted_dataset))

    def get_dataset(self, id: UUID) -> ServiceResult:
        dataset = DatasetCRUD(self.db).get_dataset(id)
        if not dataset:
            return ServiceResult(DatasetServiceExceptions.DatasetNotFound())
        return ServiceResult(DatasetItem.from_orm(dataset))


class DatasetCRUD(AppCRUD):

    def create_dataset(self, dataset: DatasetCreate) -> Dataset:
        created_item = Dataset(name=dataset.name)
        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)
        return created_item

    def update_dataset(self, id: UUID, update_dataset: DatasetUpdate)\
            -> Dataset:
        dataset = self.db.query(Dataset).filter(Dataset.id == id).first()
        if dataset is None:
            raise DatasetServiceExceptions.DatasetNotFound()
        if update_dataset.name is not None:
            dataset.name = update_dataset.name
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    def delete_dataset(self, id: UUID) -> Dataset:
        dataset = self.db.query(Dataset).filter(Dataset.id == id).first()
        if dataset is None:
            raise DatasetServiceExceptions.DatasetNotFound()
        self.db.delete(dataset)
        self.db.commit()
        return dataset

    def get_dataset(self, id: UUID) -> Dataset:
        dataset = self.db.query(Dataset).filter(Dataset.id == id).first()
        if dataset is None:
            raise DatasetServiceExceptions.DatasetNotFound()
        return dataset


class DatasetServiceExceptions:

    class DatasetCreateFailed(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Dataset Creation Failed
            """
            status_code = 500
            super().__init__(status_code, context)

    class DatasetUpdateFailed(AppExceptionCase):
        def __init__(self, context: dict = None):
            status_code = 500
            super().__init__(status_code, context)

    class DatasetDeleteFailed(AppExceptionCase):
        def __init__(self, context: dict = None):
            status_code = 500
            super().__init__(status_code, context)

    class DatasetNotFound(AppExceptionCase):
        def __init__(self, context: dict = None):
            status_code = 404
            super().__init__(status_code, context)
