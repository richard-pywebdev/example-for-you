import uuid
from pydantic import AnyUrl
import datetime

from pydantic.types import UUID
from sqlmodel import SQLModel, Field


# Posts Schemas
class BlogPostIn(SQLModel):
    title: str
    teaser: str
    content: str
    cover_image: AnyUrl
    published: bool

    class Config:
        schema_extra = {
            "example": {
                "title": "Lorem ipsum",
                "teaser": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                "cover_image": "http://www.exampleforyou.net/static/images/excepteur_sint.jpg",
                "published": True
            }
        }


class BlogPostOut(BlogPostIn):
    id: uuid.UUID
    created_date: datetime.datetime


# SQLModel Database Schemas
class BlogPost(BlogPostIn, table=True):
    id: UUID | None = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False)
    created_date: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False)