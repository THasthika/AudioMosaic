from .base import BaseService

from fastapi import status
from uuid import UUID

from app.repositories.audio_sample_label import AudioSampleLabelRepository

from app.schemas.audio_sample_label import (
    AudioSampleLabelCreate,
    AudioSampleLabelItem,
    AudioSampleLabelUpdate,
)
from app.models.audio_sample_label import AudioSampleLabel
from app.utils.service_result import ServiceResult
from app.exceptions.base import AppExceptionCase

from sqlalchemy.exc import IntegrityError


class AudioSampleLabelService(BaseService):
    def _get_sample_label(
        self, audio_sample_id: UUID, label_instance_id: UUID
    ) -> AudioSampleLabel:
        audio_sample_label: AudioSampleLabel = AudioSampleLabelRepository(
            self.db
        ).get_by_id(label_instance_id)

        if audio_sample_label is None:
            raise AppExceptionCase(
                status.HTTP_404_NOT_FOUND,
                {"reason": "Audio Sample Label not found"},
            )

        if audio_sample_label.audio_sample_id != audio_sample_id:
            raise AppExceptionCase(
                status.HTTP_404_NOT_FOUND,
                {"reason": "Audio Sample Label not found"},
            )

        return audio_sample_label

    @staticmethod
    def _validate_audio_sample_label_times(
        sample_label: AudioSampleLabelCreate | AudioSampleLabelUpdate,
    ):
        # validation
        if not sample_label.is_sample_level:
            if sample_label.start_time is None or sample_label.start_time < 0:
                raise AppExceptionCase(
                    status.HTTP_400_BAD_REQUEST,
                    {"reason": "Invalid start_time"},
                )
            if sample_label.end_time is None or sample_label.end_time < 0:
                raise AppExceptionCase(
                    status.HTTP_400_BAD_REQUEST, {"reason": "Invalid end_time"}
                )
            if sample_label.start_time > sample_label.end_time:
                raise AppExceptionCase(
                    status.HTTP_400_BAD_REQUEST,
                    {"reason": "start_time should be less than end_time"},
                )
        else:
            sample_label.start_time = None
            sample_label.end_time = None

        return sample_label

    def create_audio_sample_label(
        self, create_request: AudioSampleLabelCreate
    ) -> ServiceResult:
        try:
            create_request = (
                AudioSampleLabelService._validate_audio_sample_label_times(
                    create_request
                )
            )

            created_model: AudioSampleLabel = AudioSampleLabelRepository(
                self.db
            ).create(create_request)
            return ServiceResult(AudioSampleLabelItem.from_orm(created_model))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except IntegrityError as e:
            print(e)
            return ServiceResult(
                AppExceptionCase(
                    status.HTTP_400_BAD_REQUEST, {"reason": "could not create"}
                )
            )
        except Exception as e:
            print(e)
            return ServiceResult(
                AppExceptionCase(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    {"reason": "something went wrong"},
                )
            )

    def delete_audio_sample_label(
        self, audio_sample_id: UUID, label_instance_id: UUID
    ) -> ServiceResult:
        try:
            audio_sample_label = self._get_sample_label(
                audio_sample_id, label_instance_id
            )
            AudioSampleLabelRepository(self.db).delete(audio_sample_label.id)
            return ServiceResult(
                AudioSampleLabelItem.from_orm(audio_sample_label)
            )
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(
                AppExceptionCase(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    {"reason": "something went wrong"},
                )
            )

    def update_audio_sample_label(
        self,
        audio_sample_id: UUID,
        label_instance_id: UUID,
        update_request: AudioSampleLabelUpdate,
    ) -> ServiceResult:
        try:
            update_request = (
                AudioSampleLabelService._validate_audio_sample_label_times(
                    update_request
                )
            )

            audio_sample_label = self._get_sample_label(
                audio_sample_id, label_instance_id
            )
            updated_model = AudioSampleLabelRepository(self.db).update(
                audio_sample_label.id, update_request
            )
            return ServiceResult(AudioSampleLabelItem.from_orm(updated_model))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(
                AppExceptionCase(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    {"reason": "something went wrong"},
                )
            )

    def get_audio_sample_labels(self, audio_sample_id: UUID) -> ServiceResult:
        try:
            audio_sample_labels = AudioSampleLabelRepository(
                self.db
            ).get_by_audio_sample_id(audio_sample_id)
            return ServiceResult(
                list(
                    map(
                        lambda x: AudioSampleLabelItem.from_orm(x),
                        audio_sample_labels,
                    )
                )
            )
        except Exception as e:
            print(e)
            return ServiceResult(
                AppExceptionCase(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    {"reason": "something went wrong"},
                )
            )
