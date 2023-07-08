import pytest
import os
import io
from uuid import uuid4
from fastapi import UploadFile
from unittest.mock import MagicMock, patch
from app.services.audio_sample import AudioSampleService
from app.models.audio_sample import (
    AudioSample,
    AudioSampleApprovalStatus,
    AudioSampleProcessingStatus,
)
from datetime import datetime


@pytest.fixture
def uploaded_mpeg_file():
    file_data = os.urandom(20)
    headers = {"content-type": "audio/mpeg", "content-length": len(file_data)}
    x = io.BytesIO(file_data)
    file = UploadFile(x, headers=headers, filename="test.mp3")
    return file


@pytest.fixture
def uploaded_mpeg_file_list():
    files = []
    for _ in range(2):
        file_data = os.urandom(20)
        headers = {
            "content-type": "audio/mpeg",
            "content-length": len(file_data),
        }
        x = io.BytesIO(file_data)
        file = UploadFile(x, headers=headers, filename="test.mp3")
        files.append(file)
    return files


@pytest.fixture
def uploaded_invalid_file_list():
    files = []
    for _ in range(2):
        file_data = os.urandom(20)
        headers = {"content-type": "xxx", "content-length": len(file_data)}
        x = io.BytesIO(file_data)
        file = UploadFile(x, headers=headers, filename="test.xxx")
        files.append(file)
    return files


@pytest.fixture
def audio_sample_model_list():
    dataset_id = uuid4()
    models = [
        AudioSample(
            id=uuid4(),
            path="/path/to/file.mp3",
            parent_id=None,
            dataset_id=dataset_id,
            processing_status=AudioSampleProcessingStatus.QUEUED,
            approval_status=AudioSampleApprovalStatus.PENDING,
            sample_rate=None,
            bit_rate=None,
            duration=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        AudioSample(
            id=uuid4(),
            path="/path/to/file.mp3",
            parent_id=None,
            dataset_id=dataset_id,
            processing_status=AudioSampleProcessingStatus.QUEUED,
            approval_status=AudioSampleApprovalStatus.PENDING,
            sample_rate=None,
            bit_rate=None,
            duration=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    return models


class TestAudioSampleService:
    @pytest.mark.asyncio
    async def test_batch_upload_audio_samples(
        self, mock_repository, uploaded_mpeg_file_list, audio_sample_model_list
    ):
        repo = mock_repository()
        repo.bulk_create.return_value = audio_sample_model_list

        background_tasks = MagicMock()

        assert len(audio_sample_model_list) == len(uploaded_mpeg_file_list)

        with patch("builtins.open", new=MagicMock()) as mock_open, patch(
            "os.mkdir", new=MagicMock()
        ) as os_mkdir:
            service = AudioSampleService(repo)

            result = await service.batch_upload_audio_samples(
                uuid4(), uploaded_mpeg_file_list, background_tasks
            )

            mock_open.assert_called()
            os_mkdir.assert_called()
            assert result.success is True

    @pytest.mark.asyncio
    async def test_batch_upload_audio_samples_invalid_content_type(
        self,
        mock_repository,
        uploaded_invalid_file_list,
        audio_sample_model_list,
    ):
        repo = mock_repository()
        repo.bulk_create.return_value = audio_sample_model_list

        background_tasks = MagicMock()

        service = AudioSampleService(repo)

        result = await service.batch_upload_audio_samples(
            uuid4(), uploaded_invalid_file_list, background_tasks
        )

        assert result.success is False


# class TestLabelService:
#     def test_create_labels(self, mock_repository, create_labels, label_models):
#         repo = mock_repository()

#         repo.bulk_create.return_value = label_models

#         service = LabelService(repo)
#         result = service.create_labels(create_labels)

#         assert result.success is True
#         assert len(result.value) == len(label_models)

#     def test_create_labels_app_exception(self, mock_repository, create_labels):
#         repo = mock_repository(
#             exceptions=[("bulk_create", AppExceptionCase, [500, None])]
#         )

#         service = LabelService(repo)
#         result = service.create_labels(create_labels)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_create_labels_exception(self, mock_repository, create_labels):
#         repo = mock_repository(exceptions=[("bulk_create", Exception, [])])

#         service = LabelService(repo)
#         result = service.create_labels(create_labels)

#         assert result.success is False
#         assert type(result.value) is label_exceptions.LabelCreateFailed

#     def test_create_label(self, mock_repository, create_label, label_model):
#         repo = mock_repository()

#         repo.create.return_value = label_model

#         service = LabelService(repo)
#         result = service.create_label(create_label)

#         assert result.success is True
#         assert result.value.id == label_model.id

#     def test_create_label_app_exception(self, mock_repository, create_label):
#         repo = mock_repository(
#             exceptions=[("create", AppExceptionCase, [500, None])]
#         )

#         service = LabelService(repo)
#         result = service.create_label(create_label)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_create_label_exception(self, mock_repository, create_label):
#         repo = mock_repository(exceptions=[("create", Exception, [])])

#         service = LabelService(repo)
#         result = service.create_label(create_label)

#         assert result.success is False
#         assert type(result.value) is label_exceptions.LabelCreateFailed

#     def test_list_labels_by_dataset_id(self, mock_repository, label_models):
#         repo = mock_repository()

#         dataset_id = uuid4()

#         repo.get_by_dataset_id.return_value = label_models

#         service = LabelService(repo)
#         result = service.list_labels_by_dataset_id(dataset_id)

#         assert result.success is True
#         assert len(result.value) == len(label_models)

#     def test_list_labels_by_dataset_id_exception(self, mock_repository):
#         repo = mock_repository(
#             exceptions=[("get_by_dataset_id", Exception, [])]
#         )

#         dataset_id = uuid4()

#         service = LabelService(repo)
#         result = service.list_labels_by_dataset_id(dataset_id)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_update_label(self, mock_repository, label_model):
#         repo = mock_repository()

#         label_id = uuid4()
#         update_label = LabelUpdate(name="Updated Label")

#         repo.update.return_value = label_model

#         service = LabelService(repo)
#         result = service.update_label(label_id, update_label)

#         assert result.success is True
#         repo.update.assert_called_once()

#     def test_update_label_app_exception(self, mock_repository):
#         repo = mock_repository(
#             exceptions=[("update", AppExceptionCase, [500, None])]
#         )

#         label_id = uuid4()
#         update_label = LabelUpdate(name="Updated Label")

#         service = LabelService(repo)
#         result = service.update_label(label_id, update_label)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_update_label_exception(self, mock_repository):
#         repo = mock_repository(exceptions=[("update", Exception, [])])

#         label_id = uuid4()
#         update_label = LabelUpdate(name="Updated Label")

#         service = LabelService(repo)
#         result = service.update_label(label_id, update_label)

#         assert result.success is False
#         assert type(result.value) is label_exceptions.LabelUpdateFailed

#     def test_delete_label(self, mock_repository, label_model):
#         repo = mock_repository()

#         label_id = uuid4()

#         repo.delete.return_value = label_model

#         service = LabelService(repo)
#         result = service.delete_label(label_id)

#         assert result.success is True
#         repo.delete.assert_called_once()

#     def test_delete_label_app_exception(self, mock_repository):
#         repo = mock_repository(
#             exceptions=[("delete", AppExceptionCase, [500, None])]
#         )

#         label_id = uuid4()

#         service = LabelService(repo)
#         result = service.delete_label(label_id)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_delete_label_exception(self, mock_repository):
#         repo = mock_repository(exceptions=[("delete", Exception, [])])

#         label_id = uuid4()

#         service = LabelService(repo)
#         result = service.delete_label(label_id)

#         assert result.success is False
#         assert type(result.value) is label_exceptions.LabelDeleteFailed

#     def test_get_label(self, mock_repository, label_model):
#         repo = mock_repository()

#         repo.get_by_id.return_value = label_model

#         service = LabelService(repo)
#         result = service.get_label(uuid4())

#         assert result.success is True

#     def test_get_label_app_exception(self, mock_repository):
#         repo = mock_repository(
#             exceptions=[("get_by_id", AppExceptionCase, [500, None])]
#         )

#         label_id = uuid4()

#         service = LabelService(repo)
#         result = service.get_label(label_id)

#         assert result.success is False
#         assert type(result.value) is AppExceptionCase

#     def test_get_label_exception(self, mock_repository):
#         repo = mock_repository(exceptions=[("get_by_id", Exception, [])])

#         label_id = uuid4()

#         service = LabelService(repo)
#         result = service.get_label(label_id)

#         assert result.success is False
#         assert type(result.value) is label_exceptions.LabelNotFound
