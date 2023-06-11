from .base import AppService, AppCRUD

from app.utils.app_exceptions import AppExceptionCase
from app.models import Dataset
from app.schemas import DatasetCreate, DatasetQuery, DatasetItem
from app.utils.service_result import ServiceResult


class DatasetService(AppService):

    def create_dataset(self, dataset: DatasetCreate) -> ServiceResult:
        created_dataset = DatasetCRUD(self.db).create_dataset(dataset)
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


class DatasetCRUD(AppCRUD):

    def create_dataset(self, dataset: DatasetCreate) -> Dataset:
        created_item = Dataset(name=dataset.name)
        self.db.add(created_item)
        self.db.commit()
        self.db.refresh(created_item)
        return created_item


class DatasetServiceExceptions:

    class DatasetCreateFailed(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Dataset Creation Failed
            """
            status_code = 500
            super().__init__(status_code, context)
