import os

from starlette.datastructures import CommaSeparatedStrings

PROJECT_NAME = os.getenv("PROJECT_NAME", "Audio Dataset Manager")
LOG_LEVEL = os.getenv("LOG_LEVEL")
DEBUG = os.getenv("LOG_LEVEL", "").strip().lower() == "debug"
API_VERSION = os.getenv("API_VERSION", "v1")
ROOT_PATH = os.getenv("ROOT_PATH", "")
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-KEY"
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))

APP_DIST_PATH = os.getenv("APP_DIST_PATH", os.path.join("frontend", "dist"))

STORAGE_PATH = os.getenv("STORAGE_PATH", "storage")
STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")

STORAGE_AUDIO_SAMPLE_PATH = os.path.join(STORAGE_PATH, "audio_samples")
