from app.config.database import Base
from app.utils.guid import GUID
from uuid import uuid4
from .audio_sample import AudioSample
from .label import Label
from sqlalchemy import Column, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship


class AudioSampleLabel(Base):
    __tablename__ = "audio_sample_labels"

    id = Column(GUID(), primary_key=True, default=uuid4)
    label_id = Column(GUID(), ForeignKey(Label.id))
    audio_sample_id = Column(GUID(), ForeignKey(AudioSample.id))
    is_sample_level = Column(Boolean, default=True)
    start_time = Column(
        Float(), nullable=True
    )
    end_time = Column(
        Float(), nullable=True
    )

    label = relationship("Label", foreign_keys="AudioSampleLabel.label_id")
    audio_sample = relationship(
        "AudioSample", foreign_keys="AudioSampleLabel.audio_sample_id"
    )
