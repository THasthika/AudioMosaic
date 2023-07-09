from uuid import uuid4
from app.services.dataset import DatasetService
from app.schemas.dataset import DatasetCreate, DatasetQuery, DatasetUpdate
from app.models.dataset import Dataset
from app.exceptions.base import AppExceptionCase
from app.exceptions.dataset import (
    DatasetCreateFailed,
    DatasetUpdateFailed,
    DatasetDeleteFailed,
    DatasetNotFound,
)
from datetime import datetime


class TestDatasetService:
    def test_create_dataset(self, mock_repository):
        id = uuid4()

        repo = mock_repository()
        repo.create.return_value = Dataset(
            id=id,
            name="XXX",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        req = DatasetCreate(name="XXX")

        service = DatasetService(repo)
        created_model = service.create_dataset(req)

        repo.create.assert_called_once()
        assert created_model.value.id == id

    def test_create_dataset_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("create", AppExceptionCase, [500, None])]
        )

        req = DatasetCreate(name="")

        service = DatasetService(repo)
        result = service.create_dataset(req)
        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_create_dataset_db_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("create", Exception, [])])

        req = DatasetCreate(name="")

        service = DatasetService(repo)
        result = service.create_dataset(req)
        assert result.success is False
        assert type(result.value) is DatasetCreateFailed

    def test_list_datasets(self, mock_repository):
        repo = mock_repository()

        models = [
            Dataset(
                id=uuid4(),
                name="XXX",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Dataset(
                id=uuid4(),
                name="XXX",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

        repo.get_paginated_list.return_value = (models, len(models))

        service = DatasetService(repo)
        result = service.list_datasets(DatasetQuery(offset=0, limit=10))

        assert result.success is True
        assert result.value.count == len(models)

    def test_list_datasets_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("get_paginated_list", Exception, [])]
        )

        service = DatasetService(repo)
        result = service.list_datasets(DatasetQuery(offset=0, limit=10))

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_update_dataset(self, mock_repository):
        repo = mock_repository()

        repo.update.return_value = Dataset(
            id=uuid4(),
            name="XXX",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        id = uuid4()
        update_req = DatasetUpdate(name="XXY")

        service = DatasetService(repo)
        result = service.update_dataset(id, update_req)

        assert result.success is True
        repo.update.assert_called_once_with(id, update_req)

    def test_update_dataset_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("update", AppExceptionCase, [500, None])]
        )

        service = DatasetService(repo)
        result = service.update_dataset(uuid4(), DatasetUpdate())
        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_update_dataset_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("update", Exception, [])])

        service = DatasetService(repo)
        result = service.update_dataset(uuid4(), DatasetUpdate())
        assert result.success is False
        assert type(result.value) is DatasetUpdateFailed

    def test_delete_dataset(self, mock_repository):
        repo = mock_repository()

        repo.delete.return_value = Dataset(
            id=uuid4(),
            name="XXX",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        id = uuid4()

        service = DatasetService(repo)
        result = service.delete_dataset(id)

        assert result.success is True
        repo.delete.assert_called_once_with(id)

    def test_delete_dataset_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("delete", AppExceptionCase, [500, None])]
        )

        service = DatasetService(repo)
        result = service.delete_dataset(uuid4())
        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_delete_dataset_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("delete", Exception, [])])

        service = DatasetService(repo)
        result = service.delete_dataset(uuid4())
        assert result.success is False
        assert type(result.value) is DatasetDeleteFailed

    def test_get_dataset(self, mock_repository):
        repo = mock_repository()

        repo.get_by_id.return_value = Dataset(
            id=uuid4(),
            name="XXX",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        id = uuid4()

        service = DatasetService(repo)
        result = service.get_dataset(id)

        assert result.success is True
        repo.get_by_id.assert_called_once_with(id)

    def test_get_dataset_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("get_by_id", AppExceptionCase, [500, None])]
        )

        service = DatasetService(repo)
        result = service.get_dataset(uuid4())
        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_get_dataset_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("get_by_id", Exception, [])])

        service = DatasetService(repo)
        result = service.get_dataset(uuid4())
        assert result.success is False
        assert type(result.value) is DatasetNotFound
