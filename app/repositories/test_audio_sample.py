from uuid import uuid4
from pytest import raises
from app.repositories.audio_sample import AudioSampleRepository
from app.exceptions.audio_sample import AudioSampleNotFound
from app.schemas.audio_sample import AudioSampleCreate, AudioSampleUpdate
from app.models.audio_sample import (
    AudioSample,
    AudioSampleApprovalStatus,
    AudioSampleProcessingStatus,
)
from unittest.mock import MagicMock


class TestAudioSampleRepository:
    def test_create(self):
        dataset_id = uuid4()

        create_schema = AudioSampleCreate(
            parent_id=None, path="some_path.mp3", dataset_id=dataset_id
        )

        def refresh_side_effect(m):
            m.id = uuid4()

        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = AudioSampleRepository(db)
        created_model = repo.create(create_schema)

        assert created_model.path == create_schema.path
        assert created_model.id is not None

    def test_bulk_create(self):
        dataset_id = uuid4()

        create_schemas = [
            AudioSampleCreate(
                parent_id=None, path="some_path.mp3", dataset_id=dataset_id
            ),
            AudioSampleCreate(
                parent_id=None, path="some_path1.mp3", dataset_id=dataset_id
            ),
        ]

        def refresh_side_effect(m):
            m.id = uuid4()

        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = AudioSampleRepository(db)
        created_models = repo.bulk_create(create_schemas)

        db.begin.assert_called_once()
        db.refresh.assert_called()

        assert len(created_models) == len(create_schemas)
        assert all(
            [
                created_models[i].path == create_schemas[i].path
                for i in range(len(create_schemas))
            ]
        )

    def test_update(self, mock_sqlalchemy_orm):
        p_id = uuid4()

        update_schema = AudioSampleUpdate(
            parent_id=p_id,
            approval_status=AudioSampleApprovalStatus.ACCEPTED,
            processing_status=AudioSampleProcessingStatus.QUEUED,
            sample_rate=44100,
            bit_rate=100,
            duration=1.5,
        )

        id = uuid4()
        dataset_id = uuid4()

        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                AudioSample(
                    id=id,
                    parent_id=None,
                    path="some_path.mp3",
                    dataset_id=dataset_id,
                ),
            ),
        )

        repo = AudioSampleRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.parent_id == p_id
        assert updated_model.approval_status == update_schema.approval_status
        assert (
            updated_model.processing_status == update_schema.processing_status
        )
        assert updated_model.sample_rate == update_schema.sample_rate
        assert updated_model.bit_rate == update_schema.bit_rate
        assert updated_model.duration == update_schema.duration
        assert updated_model.id == id

    def test_update_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        update_schema = AudioSampleUpdate(bit_rate=1)

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = AudioSampleRepository(db)
        with raises(AudioSampleNotFound):
            repo.update(id, update_schema)

    def test_delete(self, mock_sqlalchemy_orm):
        id = uuid4()
        model = AudioSample(id=id, parent_id=None, path="some_path.mp3")

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", model))

        repo = AudioSampleRepository(db)
        deleted_model = repo.delete(id)

        db.delete.assert_called_once()
        db.commit.assert_called_once()
        assert deleted_model.id == id

    def test_delete_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = AudioSampleRepository(db)
        with raises(AudioSampleNotFound):
            repo.delete(id)

    def test_bulk_delete(self, mock_sqlalchemy_orm):
        models = [
            AudioSample(parent_id=None, path="some_path.mp3"),
            AudioSample(parent_id=None, path="some_path1.mp3"),
        ]
        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))
        repo = AudioSampleRepository(db)
        repo.bulk_delete(models)

        db.begin.assert_called_once()
        db.delete.assert_called()

    def test_set_parent_model_null(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm([])
        model = AudioSample(parent_id=uuid4(), path="some_path1.mp3")
        repo = AudioSampleRepository(db)
        updated_model = repo.set_model_parent_null(model)
        assert updated_model.parent_id is None

    def test_get_all(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm([], ("query", []))

        repo = AudioSampleRepository(db)

        repo.get_all()
        db.query.assert_called_once()

    def test_get_by_id(self, mock_sqlalchemy_orm):
        id = uuid4()
        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                AudioSample(id=id, parent_id=None, path="some_path.mp3"),
            ),
        )

        repo = AudioSampleRepository(db)

        ret = repo.get_by_id(id)

        assert ret is not None
        assert ret.id == id
        db.first.assert_called_once()

    def test_get_paginated_list(self, mock_sqlalchemy_orm):
        models = [
            AudioSample(id=uuid4(), parent_id=None, path="some_path.mp3"),
            AudioSample(id=uuid4(), parent_id=None, path="some_path1.mp3"),
        ]

        db = mock_sqlalchemy_orm(
            [
                (["query"], ("count", len(models))),
                (["query", "filter", "offset", "limit"], ("all", models)),
            ]
        )

        repo = AudioSampleRepository(db)

        (ret_models, count) = repo.get_paginated_list_by_dataset_id(
            0, 10, uuid4()
        )

        assert count == len(models)
        assert len(models) == len(ret_models)
