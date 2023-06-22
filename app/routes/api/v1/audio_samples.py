from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from uuid import UUID

from app.config.database import get_db
# from app.schemas import LabelItem, LabelCreate, LabelUpdate
# from app.services.label import LabelService
from app.utils.service_result import handle_result
from app.services.audio_sample import AudioSampleService

router = APIRouter()


@router.post("/{dataset_id}", tags=["Audio Sample"])
async def upload_audio_samples(dataset_id: UUID, audio_samples: list[UploadFile], background_tasks: BackgroundTasks, db: get_db = Depends()):
    result = await AudioSampleService(
        db, background_tasks).batch_upload_audio_samples(dataset_id, audio_samples)

    print(result)

    return handle_result(result=result)


# @router.get(
#     "/{dataset_id}",
#     response_model=list[LabelItem],
#     status_code=status.HTTP_200_OK,
#     tags=["Labels"],
# )
# async def list_labels(dataset_id: UUID, db: get_db = Depends()):
#     labels = LabelService(db).list_labels_by_dataset_id(dataset_id)
#     return handle_result(labels)


# @router.post(
#     "",
#     response_model=LabelItem,
#     status_code=status.HTTP_201_CREATED,
#     tags=["Labels"],
# )
# async def create_label(label_create: LabelCreate, db: get_db = Depends()):
#     label = LabelService(db).create_label(label_create)
#     return handle_result(label)


# @router.patch(
#     "/label/{id}",
#     response_model=LabelItem,
#     status_code=status.HTTP_200_OK,
#     tags=["Labels"],
# )
# async def update_label(
#     id: UUID, label_update: LabelUpdate, db: get_db = Depends()
# ):
#     updated_label = LabelService(db).update_label(id, label_update)
#     return handle_result(updated_label)


# @router.delete(
#     "/label/{id}",
#     response_model=LabelItem,
#     status_code=status.HTTP_200_OK,
#     tags=["Labels"],
# )
# async def delete_label(id: UUID, db: get_db = Depends()):
#     deleted_label = LabelService(db).delete_label(id)
#     return handle_result(deleted_label)


# @router.get(
#     "/label/{id}",
#     response_model=LabelItem,
#     status_code=status.HTTP_200_OK,
#     tags=["Labels"],
# )
# async def get_Label_by_id(id: UUID, db: get_db = Depends()):
#     label = LabelService(db).get_label(id)
#     return handle_result(label)
