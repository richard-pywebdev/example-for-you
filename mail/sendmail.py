from typing import List

from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from config.settings import settings


# Configure fastapi-mail settings
class EmailSchema(BaseModel):
    email: List[EmailStr]


send_mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.CONF_MAIL_USERNAME,
    MAIL_PASSWORD=settings.CONF_MAIL_PASSWORD,
    MAIL_FROM=settings.CONF_MAIL_FROM,
    MAIL_PORT=settings.CONF_MAIL_PORT,
    MAIL_SERVER=settings.CONF_MAIL_SERVER,
    MAIL_FROM_NAME="ExampleForYou Website",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_message_or_500(message: str):
    if not settings.CONF_MAIL_DEV_MODE:
        try:
            message = MessageSchema(
                subject="Message from exampleforyou.net contact form",
                recipients=["richard@pythonwebdeveloper.com"],
                body=message,
                subtype="plain"
            )

            fm = FastMail(send_mail_conf)

            await fm.send_message(message)

        except KeyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(message)