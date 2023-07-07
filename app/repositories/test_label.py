from uuid import uuid4
from pytest import raises
from app.repositories.label import LabelRepository
from app.exceptions.label import LabelNotFound
from app.schemas.label import LabelCreate, LabelUpdate
from app.models.label import Label
from unittest.mock import MagicMock


class TestLabelRepository:
    def test_create(self):
        dataset_id = uuid4()

        create_schema = LabelCreate(
            dataset_id=dataset_id,
            name="Hello",
            description="Hello Desc",
            color="#fff",
        )

        def refresh_side_effect(m):
            m.id = uuid4()

        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = LabelRepository(db)
        created_model = repo.create(create_schema)

        assert created_model.name == create_schema.name
        assert created_model.id is not None

    def test_bulk_create(self):
        dataset_id = uuid4()

        create_schemas = [
            LabelCreate(
                dataset_id=dataset_id,
                name="Hello",
                description="Hello Desc",
                color="#fff",
            ),
            LabelCreate(
                dataset_id=dataset_id,
                name="Hello 1",
                description="Hello Desc 1",
                color="#ffe",
            ),
        ]

        def refresh_side_effect(m):
            m.id = uuid4()

        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = LabelRepository(db)
        created_models = repo.bulk_create(create_schemas)

        db.begin.assert_called_once()
        db.refresh.assert_called()

        assert len(created_models) == len(create_schemas)
        assert all(
            [
                created_models[i].color == create_schemas[i].color
                for i in range(len(create_schemas))
            ]
        )

    def test_update(self, mock_sqlalchemy_orm):
        update_schema = LabelUpdate(
            name="Hello B", color="#000", description="Hello D"
        )

        id = uuid4()

        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                Label(
                    id=id, name="Hello", description="Hello Desc", color="#fff"
                ),
            ),
        )

        repo = LabelRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.name == update_schema.name
        assert updated_model.color == update_schema.color
        assert updated_model.description == update_schema.description
        assert updated_model.id == id

    def test_update_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        update_schema = LabelUpdate(name="Hello B")

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = LabelRepository(db)
        with raises(LabelNotFound):
            repo.update(id, update_schema)

    def test_delete(self, mock_sqlalchemy_orm):
        id = uuid4()
        model = Label(
            id=id, name="Hello", description="Hello Desc", color="#fff"
        )

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", model))

        repo = LabelRepository(db)
        deleted_model = repo.delete(id)

        db.delete.assert_called_once()
        db.commit.assert_called_once()
        assert deleted_model.id == id

    def test_delete_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = LabelRepository(db)
        with raises(LabelNotFound):
            repo.delete(id)

    def test_get_all(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm([], ("query", []))

        repo = LabelRepository(db)

        repo.get_all()
        db.query.assert_called_once()

    def test_get_by_id(self, mock_sqlalchemy_orm):
        id = uuid4()
        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                Label(
                    id=id, name="Hello", description="Hello Desc", color="#fff"
                ),
            ),
        )

        repo = LabelRepository(db)

        ret = repo.get_by_id(id)

        assert ret is not None
        assert ret.id == id
        db.first.assert_called_once()
