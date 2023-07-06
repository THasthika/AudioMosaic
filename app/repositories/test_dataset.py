"""
Dataset Repository

- create
- update
- delete
- read

"""
from uuid import uuid4
from pytest import raises
from mock import patch
import pytest
from app.repositories.dataset import DatasetRepository
from app.exceptions.dataset import DatasetNotFound
from app.schemas.dataset import DatasetCreate, DatasetUpdate
from app.models.dataset import Dataset
from unittest.mock import MagicMock


@pytest.fixture
def mock_sqlalchemy_orm(request):
    db = MagicMock()
    return request.param


class TestDatasetRepository:

    def test_create(self):
        create_schema = DatasetCreate(name="Hello")

        def refresh_side_effect(m):
            m.id = uuid4()
        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = DatasetRepository(db)
        created_model = repo.create(create_schema)

        assert created_model.name == create_schema.name
        assert created_model.id is not None

    def test_update(self):
        update_schema = DatasetUpdate(name="Hello B")

        id = uuid4()

        db = MagicMock()
        db.__getattr__('query').return_value = db
        db.__getattr__('filter').return_value = db
        db.__getattr__('first').return_value = Dataset(id=id, name="Hello")

        repo = DatasetRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.name == update_schema.name
        assert updated_model.id == id

    @pytest.mark.parametrize('mock_sqlalchemy_orm', [
        [
            ("query|filter|first")
        ]
    ], indirect=True)
    def test_update_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        print(mock_sqlalchemy_orm)

    def test_delete(self):

        id = uuid4()
        model = Dataset(id=id, name="Hello")

        db = MagicMock()
        db.__getattr__('query').return_value = db
        db.__getattr__('filter').return_value = db
        db.__getattr__('first').return_value = model

        repo = DatasetRepository(db)
        deleted_model = repo.delete(id)

        db.delete.assert_called_once()
        db.commit.assert_called_once()
        assert deleted_model.id == id

    def test_delete_with_non_existent_dataset(self):

        db = MagicMock()
        db.__getattr__('query').return_value = db
        db.__getattr__('filter').return_value = db
        db.__getattr__('first').return_value = None

        repo = DatasetRepository(db)
        with raises(DatasetNotFound):
            repo.delete(id)
