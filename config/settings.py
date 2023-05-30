import pathlib

from pydantic import BaseSettings


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    CONF_API_V1_STR: str = "/api/v1"

    CONF_MAIN_APP_HOST = "0.0.0.0"
    CONF_MAIN_APP_PORT = 443

    CONF_DEBUG_LEVEL = "debug"
    CONF_SSL_KEYFILE = "mnt/certs/www.exampleforyou.net.key"
    CONF_SSL_CERTFILE = "mnt/certs/www.exampleforyou.net.crt"

    CONF_MAIN_APP_SQLITE = "sqlite:///mnt/db/exampleforyou.sqlite3"

    CONF_MAIN_DOMAIN = "https://localhost"
    CONF_IMAGE_UPLOADS_CONTEXT_PATH = "/uploads/"
    CONF_IMAGE_UPLOADS_FILE_PATH = "mnt/uploads/"

    CONF_MAIL_USERNAME = ""
    CONF_MAIL_PASSWORD = ""
    CONF_MAIL_FROM = "richard@exampleforyou.net"
    CONF_MAIL_PORT = "587"
    CONF_MAIL_SERVER = "email-smtp.eu-west-1.amazonaws.com"
    CONF_MAIL_FROM_NAME = "Exampleforyou Website"
    CONF_MAIL_DEV_MODE = True

    CONF_CAPTCHA_CONTEXT_PATH = "/captcha/"
    CONF_CAPTCHA_FILE_PATH = "mnt/captcha/"


    class Config:
        case_sensitive = True


settings = Settings()