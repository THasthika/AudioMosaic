from uuid import uuid4
from datetime import datetime
from app.config.database import Base
from app.utils.guid import GUID
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Integer,
    Float,
)
from .dataset import Dataset
from sqlalchemy.orm import relationship
import enum


class AudioSampleProcessingStatus(enum.StrEnum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    ERROR = "ERROR"


class AudioSampleApprovalStatus(enum.StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class AudioSample(Base):
    __tablename__ = "audio_samples"

    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    path = Column(String, nullable=True)
    parent_id = Column(GUID(), ForeignKey("audio_samples.id"), nullable=True)
    dataset_id = Column(GUID(), ForeignKey(Dataset.id))

    processing_status = Column(
        Enum(AudioSampleProcessingStatus),
        default=AudioSampleProcessingStatus.QUEUED,
    )
    approval_status = Column(
        Enum(AudioSampleApprovalStatus),
        default=AudioSampleApprovalStatus.PENDING,
    )

    sample_rate = Column(Integer, nullable=True)
    bit_rate = Column(Integer, nullable=True)
    duration = Column(Float(), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # dataset = relationship("Dataset", foreign_keys="Label.dataset_id")

    # __table_args__ = (UniqueConstraint("dataset_id", "name"),)

    children = relationship("AudioSample")
    dataset = relationship("Dataset", foreign_keys="AudioSample.dataset_id")
