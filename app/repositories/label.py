from sqlalchemy.orm import Session
from .base import BaseCRUDRepository
from app.exceptions.label import LabelNotFound
from app.models.label import Label
from app.schemas.label import LabelCreate, LabelUpdate


class LabelRepository(BaseCRUDRepository):
    ModelType = Label
    ModelCreateType = LabelCreate
    ModelUpdateType = LabelUpdate

    ItemNotFoundException = LabelNotFound

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def bulk_create(
        self, create_labels: list[ModelCreateType]
    ) -> list[ModelType]:
        with self.db.begin():
            ret: list[LabelRepository.ModelType] = []
            for create_label in create_labels:
                label = self.get_model_from_create_type(create_label)
                self.db.add(label)
            ret.append(label)
            return ret

    def get_model_from_create_type(
        self, create_type: ModelCreateType
    ) -> ModelType:
        return Label(name=create_type.name, dataset_id=create_type.dataset_id)

    def get_model_from_update_type(
        self, current_model: ModelType, update_model: ModelUpdateType
    ) -> ModelType:
        if update_model.name is not None:
            current_model.name = update_model.name

        return current_model
