import pathlib

from pydantic import BaseSettings


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    CONF_API_V1_STR: str = "/api/v1"

    CONF_MAIN_APP_HOST = "0.0.0.0"
    CONF_MAIN_APP_PORT = 8000

    class Config:
        case_sensitive = True


settings = Settings()