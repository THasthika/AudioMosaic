from fastapi import BackgroundTasks, UploadFile
from typing import Union

from sqlalchemy.orm import Session
from .base import BaseService
from app.repositories import LabelRepository
from uuid import UUID, uuid4
from app.utils.service_result import ServiceResult
from app.exceptions.base import AppExceptionCase
import app.exceptions.label as label_exceptions
from sqlalchemy.exc import IntegrityError

import app.exceptions.audio_sample as audio_sample_exceptions

from app.schemas.audio_sample import AudioSampleItem, AudioSampleCreate
from app.repositories.audio_sample import AudioSampleRepository
from app.models.audio_sample import AudioSample

from app.tasks.audio_sample import process_queued_audio_sample

from app.config.app import STORAGE_AUDIO_SAMPLE_PATH, STORAGE_TYPE

import os

# from app.models.audio_sample import Label

"""

1. Audio Sample Upload Procedure
    - User Uploads the mp3 / or other format file
        - Store in the storage folder with a status QUEUED
        - Notify the processing service that a new file has been uploaded
        - Return the status to the client
    - The processing service kicks in
        - Looks for current jobs
        - Open the file to read the metadata (sample rate, bit rate, duration)
        - Store them in the database and mark the file READY


"""


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

    # def create_label(self, create_label: LabelCreate) -> ServiceResult:
    #     try:
    #         created_label = LabelRepository(self.db).create(create_label)
    #         return ServiceResult(LabelItem.from_orm(created_label))
    #     except AppExceptionCase as e:
    #         return ServiceResult(e)
    #     except IntegrityError:
    #         return ServiceResult(label_exceptions.LabelAlreadyExists())
    #     except Exception as e:
    #         print(e)
    #         return ServiceResult(label_exceptions.LabelCreateFailed())

    # def list_labels_by_dataset_id(self, dataset_id: UUID) -> ServiceResult:
    #     try:
    #         labels = (
    #             self.db.query(Label)
    #             .filter(Label.dataset_id == dataset_id)
    #             .all()
    #         )
    #         labels = list(map(lambda x: LabelItem.from_orm(x), labels))
    #         return ServiceResult(labels)
    #     except Exception as e:
    #         print(e)
    #         # TODO: Make the exception more refined
    #         return ServiceResult(label_exceptions.AppExceptionCase(500, None))

    # def update_label(
    #     self, id: UUID, update_label: LabelUpdate
    # ) -> ServiceResult:
    #     try:
    #         updated_label = LabelRepository(self.db).update(id, update_label)
    #         return ServiceResult(LabelItem.from_orm(updated_label))
    #     except AppExceptionCase as e:
    #         return ServiceResult(e)
    #     except IntegrityError:
    #         return ServiceResult(label_exceptions.LabelAlreadyExists())
    #     except Exception as e:
    #         print(e)
    #         return ServiceResult(label_exceptions.LabelUpdateFailed())

    # def delete_label(self, id: UUID) -> ServiceResult:
    #     try:
    #         deleted_label = LabelRepository(self.db).delete(id)
    #         return ServiceResult(LabelItem.from_orm(deleted_label))
    #     except AppExceptionCase as e:
    #         return ServiceResult(e)
    #     except Exception as e:
    #         print(e)
    #         return ServiceResult(label_exceptions.LabelDeleteFailed())

    # def get_label(self, id: UUID) -> ServiceResult:
    #     try:
    #         label = LabelRepository(self.db).get_by_id(id)
    #         return ServiceResult(LabelItem.from_orm(label))
    #     except AppExceptionCase as e:
    #         return ServiceResult(e)
    #     except Exception as e:
    #         print(e)
    #         return ServiceResult(label_exceptions.LabelNotFound())
