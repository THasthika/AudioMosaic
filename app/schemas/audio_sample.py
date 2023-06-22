from pydantic import BaseModel
from uuid import UUID
from app.models.audio_sample import (
    AudioSampleProcessingStatus,
    AudioSampleApprovalStatus,
)


class AudioSampleBase(BaseModel):
    parent_id: UUID | None
    approval_status: AudioSampleApprovalStatus = (
        AudioSampleApprovalStatus.PENDING
    )
    processing_status: AudioSampleProcessingStatus = (
        AudioSampleProcessingStatus.QUEUED
    )


class AudioSampleCreate(AudioSampleBase):
    path: str | None
    dataset_id: UUID


class AudioSampleUpdate(AudioSampleBase):
    approval_status: AudioSampleApprovalStatus | None
    processing_status: AudioSampleProcessingStatus | None
    sample_rate: int | None
    bit_rate: int | None
    duration: float | None


class AudioSampleItem(AudioSampleBase):
    id: UUID
    dataset_id: UUID
    processing_status: AudioSampleProcessingStatus
    approval_status: AudioSampleApprovalStatus
    sample_rate: int | None
    bit_rate: int | None
    duration: float | None

    class Config:
        orm_mode = True
