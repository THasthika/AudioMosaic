from fastapi import BackgroundTasks, UploadFile
from typing import Union

from sqlalchemy.orm import Session
from .base import BaseService
from uuid import UUID, uuid4
from app.utils.service_result import ServiceResult
from app.exceptions.base import AppExceptionCase
from sqlalchemy.exc import IntegrityError

import app.exceptions.audio_sample as audio_sample_exceptions

from app.schemas.audio_sample import (
    AudioSampleItem,
    AudioSampleCreate,
    AudioSampleUpdate,
)
from app.repositories.audio_sample import AudioSampleRepository
from app.models.audio_sample import AudioSample, AudioSampleApprovalStatus

from app.tasks.audio_sample import (
    process_queued_audio_sample,
    delete_audio_sample,
)

from app.config.app import STORAGE_AUDIO_SAMPLE_PATH, STORAGE_TYPE

import os

# from app.models.audio_sample import Label


class AudioSampleService(BaseService):
    ACCEPTED_FILE_TYPES = ["audio/mpeg"]

    @staticmethod
    def _is_audio_sample_valid_content_type(audio_sample: UploadFile):
        if (
            audio_sample.content_type
            not in AudioSampleService.ACCEPTED_FILE_TYPES
        ):
            return False
        return True

    def _make_insert_models(
        self, dataset_id: UUID, audio_sample_files: list[UploadFile]
    ) -> list[AudioSampleCreate]:
        audio_sample_create_models: list[AudioSampleCreate] = []

        for file in audio_sample_files:
            file_uuid = uuid4()
            [_, ext] = os.path.splitext(file.filename)
            if ext is None:
                raise audio_sample_exceptions.AudioSampleIncorrectContentType(
                    {"reason": f"invalid file extension: {file.filename}"}
                )
            file_path = os.path.join(
                STORAGE_AUDIO_SAMPLE_PATH, f"{dataset_id}", f"{file_uuid}{ext}"
            )

            audio_sample_create_models.append(
                AudioSampleCreate(
                    path=file_path, parent_id=None, dataset_id=dataset_id
                )
            )

        return audio_sample_create_models

    async def batch_upload_audio_samples(
        self,
        dataset_id: UUID,
        audio_sample_files: list[UploadFile],
        background_tasks: BackgroundTasks,
    ) -> ServiceResult:
        inserted_models = None
        audio_sample_repo = AudioSampleRepository(self.db)

        try:
            # validate files
            for file in audio_sample_files:
                if not AudioSampleService._is_audio_sample_valid_content_type(
                    file
                ):
                    raise audio_sample_exceptions.AudioSampleIncorrectContentType(
                        {"reason": f"invalid file: {file.filename}"}
                    )

            insert_models = self._make_insert_models(
                dataset_id, audio_sample_files
            )

            # make database entries for the files
            inserted_models = audio_sample_repo.bulk_create(insert_models)

            # make the folder if not exists
            dataset_folder_path = os.path.join(
                STORAGE_AUDIO_SAMPLE_PATH, f"{dataset_id}"
            )
            if not os.path.exists(dataset_folder_path):
                os.mkdir(dataset_folder_path)

            # move files to storage
            for i, file in enumerate(audio_sample_files):
                file_path = insert_models[i].path
                with open(file_path, "wb+") as f:
                    f.write(await file.read())

            # trigger background task to process files
            for inserted_model in inserted_models:
                background_tasks.add_task(
                    process_queued_audio_sample, self.db, inserted_model.id
                )

            return ServiceResult(
                list(
                    map(lambda x: AudioSampleItem.from_orm(x), inserted_models)
                )
            )

        except IOError as e:
            # cleanup saved files and return error
            print(e)
            if inserted_models is not None:
                for m in inserted_models:
                    try:
                        os.unlink(m.path)
                    except Exception:
                        pass

            # remove database entries
            audio_sample_repo.bulk_delete(inserted_models)

            return ServiceResult(
                audio_sample_exceptions.AudioSampleCreateFailed(
                    {"reason": "Internal error!"}
                )
            )
        except IntegrityError as e:
            error_str = f"{e}"
            error_str = error_str.splitlines()[0]
            return ServiceResult(
                audio_sample_exceptions.AudioSampleCreateFailed(
                    {"reason": "Database insert failed!", "context": error_str}
                )
            )
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(
                audio_sample_exceptions.AppExceptionCase(500, None)
            )

    def list_audio_samples_by_dataset_id(
        self, dataset_id: UUID
    ) -> ServiceResult:
        try:
            audio_samples = (
                self.db.query(AudioSample)
                .filter(AudioSample.dataset_id == dataset_id)
                .all()
            )
            audio_samples = list(
                map(lambda x: AudioSampleItem.from_orm(x), audio_samples)
            )
            return ServiceResult(audio_samples)
        except Exception as e:
            print(e)
            return ServiceResult(label_exceptions.AppExceptionCase(500, None))

    def get_audio_sample(self, sample_id: UUID) -> ServiceResult:
        try:
            audio_sample = AudioSampleRepository(self.db).get_by_id(sample_id)
            return ServiceResult(AudioSampleItem.from_orm(audio_sample))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(audio_sample_exceptions.AudioSampleNotFound())

    def update_approval_status(
        self, sample_id: UUID, new_status: AudioSampleApprovalStatus
    ) -> ServiceResult:
        try:
            update_model = AudioSampleUpdate(approval_status=new_status)
            audio_sample = AudioSampleRepository(self.db).update(
                sample_id, update_model
            )
            return ServiceResult(AudioSampleItem.from_orm(audio_sample))
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception:
            return ServiceResult(
                audio_sample_exceptions.AudioSampleApprovalStatusUpdateFailed()
            )

    def delete_audio_sample(
        self,
        sample_id: UUID,
        background_tasks: BackgroundTasks,
    ) -> ServiceResult:
        try:
            deleted_audio_sample = AudioSampleRepository(self.db).delete(
                sample_id
            )
            background_tasks.add_task(
                delete_audio_sample, deleted_audio_sample.path
            )
            return ServiceResult(
                AudioSampleItem.from_orm(deleted_audio_sample)
            )
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(
                audio_sample_exceptions.AudioSampleDeleteFailed()
            )

    def get_audio_sample_path(self, sample_id: UUID) -> ServiceResult:
        try:
            audio_sample = AudioSampleRepository(self.db).get_by_id(sample_id)
            return ServiceResult(audio_sample.path)
        except AppExceptionCase as e:
            return ServiceResult(e)
        except Exception as e:
            print(e)
            return ServiceResult(audio_sample_exceptions.AudioSampleNotFound())
