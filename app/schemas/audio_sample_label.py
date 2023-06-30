from pydantic import BaseModel
from uuid import UUID


class AudioSampleLabelBase(BaseModel):
    is_sample_level: bool
    start_time: float | None
    end_time: float | None


class AudioSampleLabelCreate(AudioSampleLabelBase):
    label_id: UUID
    audio_sample_id: UUID


class AudioSampleLabelCreateRequest(AudioSampleLabelBase):
    label_id: UUID


class AudioSampleLabelUpdate(AudioSampleLabelBase):
    is_sample_level: bool | None
    start_time: float | None
    end_time: float | None


class AudioSampleLabelItem(AudioSampleLabelBase):
    id: UUID
    label_id: UUID
    audio_sample_id: UUID

    class Config:
        orm_mode = True
