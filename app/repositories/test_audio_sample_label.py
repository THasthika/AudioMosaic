from uuid import uuid4
from pytest import raises
from app.repositories.audio_sample_label import AudioSampleLabelRepository
from app.exceptions.label import LabelNotFound
from app.schemas.audio_sample_label import AudioSampleLabelCreate, AudioSampleLabelUpdate
from app.models.audio_sample_label import AudioSampleLabel
from unittest.mock import MagicMock


class TestAudioSampleRepository:
    def test_create(self):

        create_schema = AudioSampleLabelCreate(
            label_id=uuid4(),
            audio_sample_id=uuid4(),
            is_sample_level=True
        )

        def refresh_side_effect(m):
            m.id = uuid4()

        db = MagicMock()
        db.refresh.side_effect = refresh_side_effect

        repo = AudioSampleLabelRepository(db)
        created_model = repo.create(create_schema)

        assert created_model.id is not None

    def test_update_not_sample_level(self, mock_sqlalchemy_orm):
        update_schema = AudioSampleLabelUpdate(
            is_sample_level=False,
            start_time=1.0,
            end_time=2.0
        )

        id = uuid4()

        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                AudioSampleLabel(
                    id=id,
                    label_id=uuid4(),
                    audio_sample_id=uuid4(),
                    is_sample_level=True
                ),
            ),
        )

        repo = AudioSampleLabelRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.is_sample_level == update_schema.is_sample_level
        assert updated_model.start_time == update_schema.start_time
        assert updated_model.end_time == update_schema.end_time

    def test_update_sample_level(self, mock_sqlalchemy_orm):
        update_schema = AudioSampleLabelUpdate(
            is_sample_level=True
        )

        id = uuid4()

        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                AudioSampleLabel(
                    id=id,
                    label_id=uuid4(),
                    audio_sample_id=uuid4(),
                    is_sample_level=False,
                    start_time=1.0,
                    end_time=2.0
                ),
            ),
        )

        repo = AudioSampleLabelRepository(db)
        updated_model = repo.update(id, update_schema)

        assert updated_model.is_sample_level == update_schema.is_sample_level
        assert updated_model.start_time is None
        assert updated_model.end_time is None

    def test_update_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        update_schema = AudioSampleLabelUpdate(
            is_sample_level=False,
            start_time=1.0,
            end_time=2.0
        )

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = AudioSampleLabelRepository(db)
        with raises(LabelNotFound):
            repo.update(id, update_schema)

    def test_delete(self, mock_sqlalchemy_orm):
        id = uuid4()
        model = AudioSampleLabel(
            id=id,
            label_id=uuid4(),
            audio_sample_id=uuid4(),
            is_sample_level=True
        )

        db = mock_sqlalchemy_orm(["query", "filter"], ("first", model))

        repo = AudioSampleLabelRepository(db)
        deleted_model = repo.delete(id)

        db.delete.assert_called_once()
        db.commit.assert_called_once()
        assert deleted_model.id == id

    def test_delete_with_non_existent_dataset(self, mock_sqlalchemy_orm):
        db = mock_sqlalchemy_orm(["query", "filter"], ("first", None))

        repo = AudioSampleLabelRepository(db)
        with raises(LabelNotFound):
            repo.delete(id)

    def test_get_by_id(self, mock_sqlalchemy_orm):
        id = uuid4()
        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "first",
                AudioSampleLabel(
                    id=id,
                    label_id=uuid4(),
                    audio_sample_id=uuid4(),
                    is_sample_level=True
                ),
            ),
        )

        repo = AudioSampleLabelRepository(db)

        ret = repo.get_by_id(id)

        assert ret is not None
        assert ret.id == id
        db.first.assert_called_once()

    def test_get_by_audio_sample_id(self, mock_sqlalchemy_orm):
        id = uuid4()
        models = [
            AudioSampleLabel(
                id=id,
                label_id=uuid4(),
                audio_sample_id=uuid4(),
                is_sample_level=True
            ),
            AudioSampleLabel(
                id=id,
                label_id=uuid4(),
                audio_sample_id=uuid4(),
                is_sample_level=True
            )
        ]
        db = mock_sqlalchemy_orm(
            ["query", "filter"],
            (
                "all",
                models,
            ),
        )

        repo = AudioSampleLabelRepository(db)

        ret = repo.get_by_audio_sample_id(uuid4())

        assert ret is not None
        assert len(ret) == len(models)
