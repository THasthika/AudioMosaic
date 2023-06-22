from sqlalchemy.orm import Session
from uuid import UUID


def process_queued_audio_sample(db: Session, audio_sample_id: UUID):
    print("PROCESSING")
    pass


def delete_unrelated_audio_samples(db: Session):
    pass
