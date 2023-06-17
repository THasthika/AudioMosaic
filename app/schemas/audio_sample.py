from pydantic import BaseModel
from uuid import UUID
from app.models.audio_sample import (
    AudioSampleProcessingStatus,
    AudioSampleApprovalStatus,
)


class AudioSampleBase(BaseModel):
    path: str | None
    parent_id: UUID | None
    processing_status: AudioSampleProcessingStatus = (
        AudioSampleProcessingStatus.QUEUED
    )
    approval_status: AudioSampleApprovalStatus = (
        AudioSampleApprovalStatus.PENDING
    )
    sample_rate: int
    bit_rate: int
    duration: float


class AudioSampleCreate(AudioSampleBase):
    dataset_id: UUID


class AudioSampleUpdate(AudioSampleBase):
    processing_status: AudioSampleProcessingStatus | None
    approval_status: AudioSampleApprovalStatus | None
    sample_rate: int | None
    bit_rate: int | None
    duration: float | None


class AudioSampleItem(AudioSampleBase):
    id: UUID
    dataset_id: UUID

    class Config:
        orm_mode = True
