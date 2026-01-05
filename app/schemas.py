from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ArticleStatus(BaseModel, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    excerpt: str | None = Field(None, max_length=500)
    reading_time_minutes: int = Field(default=5, ge=1, le=120)
    is_published: bool = True


class ArticleCreate(ArticleBase):
    topic_id: int
    tag_ids: list[int] | None


class ArticleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    excerpt: str | None = Field(None, max_length=500)
    reading_time_minutes: int | None = Field(None, min_length=1, max_length=120)
    is_published: bool | None = None
    topic_id: int | None = None
    tag_ids: list[int] | None = None


class ArticleInDB(ArticleBase):
    pk: int
    slug: str
    topic_id: int
    author_id: int | None = None
    views_count: int
    created_at: datetime
    updated_at: datetime | None = None
    published_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ArticlePublic(ArticleInDB):
    ...
