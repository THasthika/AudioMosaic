from sqlalchemy.orm import Session
from .base import BaseCRUDRepository
from app.exceptions.label import LabelNotFound
from app.models.audio_sample import AudioSample
from app.schemas.audio_sample import AudioSampleCreate, AudioSampleUpdate


class AudioSampleRepository(BaseCRUDRepository):
    ModelType = AudioSample
    ModelCreateType = AudioSampleCreate
    ModelUpdateType = AudioSampleUpdate

    ItemNotFoundException = LabelNotFound

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def bulk_create(
        self, create_audio_samples: list[ModelCreateType]
    ) -> list[ModelType]:
        with self.db.begin():
            ret: list[AudioSampleRepository.ModelType] = []
            for create_audio_sample in create_audio_samples:
                audio_sample = self.get_model_from_create_type(
                    create_audio_sample
                )
                self.db.add(audio_sample)
            ret.append(audio_sample)

        for s in ret:
            self.db.refresh(s)

        return ret

    def bulk_delete(self, models: list[ModelType]):
        with self.db.begin():
            for m in models:
                self.db.delete(m)

    def set_model_parent_null(self, model: ModelType):
        model.parent_id = None
        return model

    def get_model_from_create_type(
        self, create_type: ModelCreateType
    ) -> ModelType:
        return AudioSample(
            path=create_type.path,
            parent_id=create_type.parent_id,
            processing_status=create_type.processing_status,
            approval_status=create_type.approval_status,
            sample_rate=create_type.sample_rate,
            bit_rate=create_type.bit_rate,
            duration=create_type.duration,
            dataset_id=create_type.dataset_id,
        )

    def get_model_from_update_type(
        self, current_model: ModelType, update_model: ModelUpdateType
    ) -> ModelType:
        if update_model.parent_id is not None:
            current_model.parent_id = update_model.parent_id
        if update_model.processing_status is not None:
            current_model.processing_status = update_model.processing_status
        if update_model.approval_status is not None:
            current_model.approval_status = update_model.approval_status
        if update_model.sample_rate is not None:
            current_model.sample_rate = update_model.sample_rate
        if update_model.bit_rate is not None:
            current_model.bit_rate = update_model.bit_rate
        if update_model.duration is not None:
            current_model.duration = update_model.duration

        return current_model
