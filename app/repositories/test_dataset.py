from uuid import uuid4
from pytest import raises
from app.repositories.dataset import DatasetRepository
from app.exceptions.dataset import DatasetNotFound
from app.schemas.dataset import DatasetCreate, DatasetUpdate
from app.models.dataset import Dataset
from unittest.mock import MagicMock


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

    def test_update(self, mock_sqlalchemy_orm):
        update_schema = DatasetUpdate(name="Hello B")

        id = uuid4()

        db = mock_sqlalchemy_orm(
            ['query', 'filter'], ('first', Dataset(id=id, name="Hello")))

        repo = DatasetRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.name == update_schema.name
        assert updated_model.id == id

    def test_update_with_non_existent_dataset(self, mock_sqlalchemy_orm):

        update_schema = DatasetUpdate(name="Hello B")

        db = mock_sqlalchemy_orm(
            ['query', 'filter'], ('first', None))

        repo = DatasetRepository(db)
        with raises(DatasetNotFound):
            repo.update(id, update_schema)

    def test_delete(self, mock_sqlalchemy_orm):

        id = uuid4()
        model = Dataset(id=id, name="Hello")

        db = mock_sqlalchemy_orm(
            ['query', 'filter'], ('first', model))

        repo = DatasetRepository(db)
        deleted_model = repo.delete(id)

        db.delete.assert_called_once()
        db.commit.assert_called_once()
        assert deleted_model.id == id

    def test_delete_with_non_existent_dataset(self, mock_sqlalchemy_orm):

        db = mock_sqlalchemy_orm(
            ['query', 'filter'], ('first', None))

        repo = DatasetRepository(db)
        with raises(DatasetNotFound):
            repo.delete(id)

    def test_get_all(self, mock_sqlalchemy_orm):

        db = mock_sqlalchemy_orm(
            [], ('query', []))

        repo = DatasetRepository(db)

        repo.get_all()
        db.query.assert_called_once()

    def test_get_by_id(self, mock_sqlalchemy_orm):

        id = uuid4()
        db = mock_sqlalchemy_orm(
            ['query', 'filter'], ('first', Dataset(id=id, name="Hello")))

        repo = DatasetRepository(db)

        ret = repo.get_by_id(id)

        assert ret is not None
        assert ret.id == id
        db.first.assert_called_once()

    def test_get_paginated_list(self, mock_sqlalchemy_orm):

        models = [
            Dataset(id=uuid4(), name="Hello 1"),
            Dataset(id=uuid4(), name="Hello 2")
        ]

        db = mock_sqlalchemy_orm([
            (
                ['query'], ('count', len(models))
            ),
            (
                ['query', 'offset', 'limit'], ('all', models)
            ),
        ])

        repo = DatasetRepository(db)

        (ret_models, count) = repo.get_paginated_list(0, 10)

        assert count == len(models)
        assert len(models) == len(ret_models)
