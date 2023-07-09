from app.repositories import LabelRepository
from uuid import UUID
from app.schemas.label import LabelCreate, LabelUpdate, LabelItem
from app.utils.service_result import ServiceResult
from app.exceptions.base import AppExceptionCase
import app.exceptions.label as label_exceptions


class LabelService:
    def __init__(self, label_repo: LabelRepository) -> None:
        self.label_repo = label_repo

    def create_labels(self, create_labels: list[LabelCreate]) -> ServiceResult:
        try:
            created_labels = self.label_repo.bulk_create(create_labels)
            created_labels = list(
                map(lambda x: LabelItem.from_orm(x), created_labels)
            )
            return ServiceResult(created_labels)
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.LabelCreateFailed())

    def create_label(self, create_label: LabelCreate) -> ServiceResult:
        try:
            created_label = self.label_repo.create(create_label)
            return ServiceResult(LabelItem.from_orm(created_label))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.LabelCreateFailed())

    def list_labels_by_dataset_id(self, dataset_id: UUID) -> ServiceResult:
        try:
            labels = self.label_repo.get_by_dataset_id(dataset_id)
            labels = list(map(lambda x: LabelItem.from_orm(x), labels))
            return ServiceResult(labels)
        except Exception as e:
            print(e)
            # TODO: Make the exception more refined
            return ServiceResult(label_exceptions.AppExceptionCase(500, None))

    def update_label(
        self, id: UUID, update_label: LabelUpdate
    ) -> ServiceResult:
        try:
            updated_label = self.label_repo.update(id, update_label)
            return ServiceResult(LabelItem.from_orm(updated_label))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.LabelUpdateFailed())

    def delete_label(self, id: UUID) -> ServiceResult:
        try:
            deleted_label = self.label_repo.delete(id)
            return ServiceResult(LabelItem.from_orm(deleted_label))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.LabelDeleteFailed())

    def get_label(self, id: UUID) -> ServiceResult:
        try:
            label = self.label_repo.get_by_id(id)
            return ServiceResult(LabelItem.from_orm(label))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.LabelNotFound())
