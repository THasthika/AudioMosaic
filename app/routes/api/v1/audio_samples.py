from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, status
from fastapi.responses import FileResponse
from uuid import UUID

from app.config.database import get_db

from app.schemas.audio_sample import AudioSampleItem
from app.utils.service_result import handle_result
from app.services.audio_sample import AudioSampleService
from app.models.audio_sample import AudioSampleApprovalStatus

router = APIRouter()


@router.post(
    "/{dataset_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Audio Samples"],
)
async def upload_audio_samples(
    dataset_id: UUID,
    audio_samples: list[UploadFile],
    background_tasks: BackgroundTasks,
    db: get_db = Depends(),
):
    result = await AudioSampleService(db).batch_upload_audio_samples(
        dataset_id, audio_samples, background_tasks
    )
    return handle_result(result)


@router.get(
    "/{dataset_id}",
    response_model=list[AudioSampleItem],
    tags=["Audio Samples"],
)
async def audio_samples(dataset_id: UUID, db: get_db = Depends()):
    result = AudioSampleService(db).list_audio_samples_by_dataset_id(
        dataset_id
    )
    return handle_result(result)


@router.get(
    "/sample/{id}",
    response_model=AudioSampleItem,
    status_code=status.HTTP_200_OK,
    tags=["Audio Samples"],
)
async def get_audio_sample_by_id(id: UUID, db: get_db = Depends()):
    result = AudioSampleService(db).get_audio_sample(id)
    return handle_result(result)


@router.patch(
    "/sample/{id}/accept",
    response_model=AudioSampleItem,
    tags=["Audio Samples"],
)
async def accept_audio_sample(id: UUID, db: get_db = Depends()):
    result = AudioSampleService(db).update_approval_status(
        id, AudioSampleApprovalStatus.ACCEPTED
    )
    return handle_result(result)


@router.patch(
    "/sample/{id}/reject",
    response_model=AudioSampleItem,
    tags=["Audio Samples"],
)
async def reject_audio_sample(id: UUID, db: get_db = Depends()):
    result = AudioSampleService(db).update_approval_status(
        id, AudioSampleApprovalStatus.REJECTED
    )
    return handle_result(result)


@router.delete(
    "/sample/{id}",
    response_model=AudioSampleItem,
    status_code=status.HTTP_200_OK,
    tags=["Audio Samples"],
)
async def delete_audio_sample(
    id: UUID, background_tasks: BackgroundTasks, db: get_db = Depends()
):
    result = AudioSampleService(db).delete_audio_sample(id, background_tasks)
    return handle_result(result)


@router.get("/sample/{id}/data", tags=["Audio Samples"])
async def get_audio_sample_data(id: UUID, db: get_db = Depends()):
    result = AudioSampleService(db).get_audio_sample_path(id)
    if not result.success:
        return handle_result(handle_result)
    return FileResponse(result.value)
