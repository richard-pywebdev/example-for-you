from datetime import datetime
from sqlmodel import SQLModel, Field


class CaptchaIn(SQLModel):
    id: str | None = None
    captcha_image: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "id": "asdwf",
                "captcha_image": "pxfcb_2023_03_10_18_45_31.png",
            }
        }


class CaptchaOut(CaptchaIn):
    created: datetime


class Captcha(CaptchaIn, table=True):
    id: str | None = Field(
        default=None,
        max_length=5,
        primary_key=True,
        index=True,
        nullable=False)
    created: datetime | None = Field(
        default_factory=datetime.utcnow,
        nullable=False)