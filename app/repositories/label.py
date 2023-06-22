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

        for label in ret:
            self.db.refresh(label)

        return ret

    def get_model_from_create_type(
        self, create_type: ModelCreateType
    ) -> ModelType:
        return Label(
            name=create_type.name,
            color=create_type.color,
            description=create_type.description,
            dataset_id=create_type.dataset_id,
        )

    def get_model_from_update_type(
        self, current_model: ModelType, update_model: ModelUpdateType
    ) -> ModelType:
        if update_model.name is not None:
            current_model.name = update_model.name
        if update_model.color is not None:
            current_model.color = update_model.color
        if update_model.description is not None:
            current_model.description = update_model.description

        return current_model
