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
