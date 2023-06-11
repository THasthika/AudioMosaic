from uuid import UUID, uuid4
from datetime import datetime
from app.config.database import Base
from sqlalchemy import Column, String, DateTime
from app.utils.guid import GUID


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(GUID(), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
