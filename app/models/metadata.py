from sqlmodel import SQLModel

from .dataset import Dataset  # noqa: F401


def get_metadata():
    return SQLModel.metadata
