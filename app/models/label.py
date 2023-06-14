from uuid import uuid4
from datetime import datetime
from app.config.database import Base
from app.utils.guid import GUID
from .dataset import Dataset
from sqlalchemy import Column, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Label(Base):
    __tablename__ = "labels"

    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    dataset_id = Column(GUID(), ForeignKey(Dataset.id))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    dataset = relationship("Dataset", foreign_keys="Label.dataset_id")

    __table_args__ = (UniqueConstraint("dataset_id", "name"),)
