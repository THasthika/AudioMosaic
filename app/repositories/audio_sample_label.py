from uuid import UUID
from sqlalchemy.orm import Session
from .base import BaseCRUDRepository
from app.exceptions.label import LabelNotFound
from app.models.audio_sample_label import AudioSampleLabel
from app.schemas.audio_sample_label import (
    AudioSampleLabelCreate,
    AudioSampleLabelUpdate,
)


class AudioSampleLabelRepository(BaseCRUDRepository):
    ModelType = AudioSampleLabel
    ModelCreateType = AudioSampleLabelCreate
    ModelUpdateType = AudioSampleLabelUpdate

    ItemNotFoundException = LabelNotFound

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_model_from_create_type(
        self, create_type: ModelCreateType
    ) -> ModelType:
        return AudioSampleLabel(
            label_id=create_type.label_id,
            audio_sample_id=create_type.audio_sample_id,
            is_sample_level=create_type.is_sample_level,
            start_time=create_type.start_time,
            end_time=create_type.end_time,
        )

    def get_model_from_update_type(
        self, current_model: ModelType, update_model: ModelUpdateType
    ) -> ModelType:
        if update_model.is_sample_level is not None:
            current_model.is_sample_level = update_model.is_sample_level
        if update_model.start_time is not None:
            current_model.start_time = update_model.start_time
        if update_model.end_time is not None:
            current_model.end_time = update_model.end_time
        if update_model.is_sample_level:
            current_model.start_time = None
            current_model.end_time = None

        return current_model

    def get_by_audio_sample_id(self, audio_sample_id: UUID) -> list[ModelType]:
        audio_sample_labels = (
            self.db.query(AudioSampleLabel)
            .filter(AudioSampleLabel.audio_sample_id == audio_sample_id)
            .all()
        )

        return audio_sample_labels
