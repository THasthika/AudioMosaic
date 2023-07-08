import pytest
from uuid import uuid4
from app.schemas.label import LabelCreate, LabelUpdate
from app.models import Label
from app.exceptions.base import AppExceptionCase
import app.exceptions.label as label_exceptions
from app.services.label import LabelService
from datetime import datetime


@pytest.fixture
def create_labels():
    create_labels = [
        LabelCreate(name="Label 1", color="#fff", description=""),
        LabelCreate(name="Label 2", color="#fff", description=""),
    ]
    return create_labels


@pytest.fixture
def create_label():
    create_label = LabelCreate(name="Label 1", color="#fff", description="")
    return create_label


@pytest.fixture
def label_models():
    label_models = [
        Label(
            id=uuid4(),
            name="Label 1",
            color="#fff",
            description="",
            dataset_id=uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        Label(
            id=uuid4(),
            name="Label 2",
            color="#fff",
            description="",
            dataset_id=uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    return label_models


@pytest.fixture
def label_model():
    label_model = Label(
        id=uuid4(),
        name="Label 1",
        color="#fff",
        description="",
        dataset_id=uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    return label_model


class TestLabelService:
    def test_create_labels(self, mock_repository, create_labels, label_models):
        repo = mock_repository()

        repo.bulk_create.return_value = label_models

        service = LabelService(repo)
        result = service.create_labels(create_labels)

        assert result.success is True
        assert len(result.value) == len(label_models)

    def test_create_labels_app_exception(self, mock_repository, create_labels):
        repo = mock_repository(
            exceptions=[("bulk_create", AppExceptionCase, [500, None])]
        )

        service = LabelService(repo)
        result = service.create_labels(create_labels)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_create_labels_exception(self, mock_repository, create_labels):
        repo = mock_repository(exceptions=[("bulk_create", Exception, [])])

        service = LabelService(repo)
        result = service.create_labels(create_labels)

        assert result.success is False
        assert type(result.value) is label_exceptions.LabelCreateFailed

    def test_create_label(self, mock_repository, create_label, label_model):
        repo = mock_repository()

        repo.create.return_value = label_model

        service = LabelService(repo)
        result = service.create_label(create_label)

        assert result.success is True
        assert result.value.id == label_model.id

    def test_create_label_app_exception(self, mock_repository, create_label):
        repo = mock_repository(
            exceptions=[("create", AppExceptionCase, [500, None])]
        )

        service = LabelService(repo)
        result = service.create_label(create_label)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_create_label_exception(self, mock_repository, create_label):
        repo = mock_repository(exceptions=[("create", Exception, [])])

        service = LabelService(repo)
        result = service.create_label(create_label)

        assert result.success is False
        assert type(result.value) is label_exceptions.LabelCreateFailed

    def test_list_labels_by_dataset_id(self, mock_repository, label_models):
        repo = mock_repository()

        dataset_id = uuid4()

        repo.get_by_dataset_id.return_value = label_models

        service = LabelService(repo)
        result = service.list_labels_by_dataset_id(dataset_id)

        assert result.success is True
        assert len(result.value) == len(label_models)

    def test_list_labels_by_dataset_id_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("get_by_dataset_id", Exception, [])]
        )

        dataset_id = uuid4()

        service = LabelService(repo)
        result = service.list_labels_by_dataset_id(dataset_id)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_update_label(self, mock_repository, label_model):
        repo = mock_repository()

        label_id = uuid4()
        update_label = LabelUpdate(name="Updated Label")

        repo.update.return_value = label_model

        service = LabelService(repo)
        result = service.update_label(label_id, update_label)

        assert result.success is True
        repo.update.assert_called_once()

    def test_update_label_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("update", AppExceptionCase, [500, None])]
        )

        label_id = uuid4()
        update_label = LabelUpdate(name="Updated Label")

        service = LabelService(repo)
        result = service.update_label(label_id, update_label)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_update_label_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("update", Exception, [])])

        label_id = uuid4()
        update_label = LabelUpdate(name="Updated Label")

        service = LabelService(repo)
        result = service.update_label(label_id, update_label)

        assert result.success is False
        assert type(result.value) is label_exceptions.LabelUpdateFailed

    def test_delete_label(self, mock_repository, label_model):
        repo = mock_repository()

        label_id = uuid4()

        repo.delete.return_value = label_model

        service = LabelService(repo)
        result = service.delete_label(label_id)

        assert result.success is True
        repo.delete.assert_called_once()

    def test_delete_label_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("delete", AppExceptionCase, [500, None])]
        )

        label_id = uuid4()

        service = LabelService(repo)
        result = service.delete_label(label_id)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_delete_label_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("delete", Exception, [])])

        label_id = uuid4()

        service = LabelService(repo)
        result = service.delete_label(label_id)

        assert result.success is False
        assert type(result.value) is label_exceptions.LabelDeleteFailed

    def test_get_label(self, mock_repository, label_model):
        repo = mock_repository()

        repo.get_by_id.return_value = label_model

        service = LabelService(repo)
        result = service.get_label(uuid4())

        assert result.success is True

    def test_get_label_app_exception(self, mock_repository):
        repo = mock_repository(
            exceptions=[("get_by_id", AppExceptionCase, [500, None])]
        )

        label_id = uuid4()

        service = LabelService(repo)
        result = service.get_label(label_id)

        assert result.success is False
        assert type(result.value) is AppExceptionCase

    def test_get_label_exception(self, mock_repository):
        repo = mock_repository(exceptions=[("get_by_id", Exception, [])])

        label_id = uuid4()

        service = LabelService(repo)
        result = service.get_label(label_id)

        assert result.success is False
        assert type(result.value) is label_exceptions.LabelNotFound
