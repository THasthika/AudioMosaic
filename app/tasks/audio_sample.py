from sqlalchemy.orm import Session
from uuid import UUID

import audio_metadata

import logging

from app.repositories.audio_sample import AudioSampleRepository
from app.schemas.audio_sample import AudioSampleUpdate
from app.models.audio_sample import AudioSampleProcessingStatus

import os


async def process_queued_audio_sample(db: Session, audio_sample_id: UUID):
    logging.debug(f"PROCESSING Audio Sample: {audio_sample_id}")

    audio_sample_repo = AudioSampleRepository(db)

    audio_sample = audio_sample_repo.get_by_id(audio_sample_id)
    if audio_sample is None:
        logging.error(f"Audio Sample not found id: {audio_sample_id}")
        return

    metadata = audio_metadata.load(audio_sample.path)

    bitrate = 0
    duration = 0
    sample_rate = 0

    try:
        bitrate = metadata.streaminfo.bitrate
    except Exception:
        logging.error(f"Error on extracting metadata id: {audio_sample_id}")

    try:
        duration = metadata.streaminfo.duration
    except Exception:
        logging.error(f"Error on extracting metadata id: {audio_sample_id}")

    try:
        sample_rate = metadata.streaminfo.sample_rate
    except Exception:
        logging.error(f"Error on extracting metadata id: {audio_sample_id}")

    update_model = AudioSampleUpdate(
        bit_rate=bitrate,
        duration=duration,
        sample_rate=sample_rate,
        processing_status=AudioSampleProcessingStatus.READY,
    )

    try:
        audio_sample_repo.update(audio_sample_id, update_model)
    except Exception as e:
        print(e)
        logging.error(f"Error on updating audio sample id: {audio_sample_id}")


async def delete_audio_sample(audio_sample_path: str):
    try:
        os.unlink(audio_sample_path)
    except Exception:
        logging.error(f"Error while deleting path: {audio_sample_path}")


def delete_unrelated_audio_samples(db: Session):
    pass
