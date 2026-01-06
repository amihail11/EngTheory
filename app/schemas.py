from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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
    model_config = ConfigDict(from_attributes=True)
    
    pk: int
    slug: str
    topic_id: int
    author_id: int | None = None
    views_count: int
    created_at: datetime
    updated_at: datetime | None = None
    published_at: datetime | None = None


class ArticlePublic(ArticleInDB):
    topic: "TopicPublic"
    author: "UserPublic" | None = None
    tags: list["TagPublic"] = []


class TopicBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    order: int = 0
    is_published: bool = True


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    order: int | None = None
    is_published: bool | None = None


class TopicInDB(TopicBase):
    model_config = ConfigDict(from_attributes=True)
    
    pk: int
    slug: str
    created_at: datetime
    updated_at: datetime | None = None


class TopicPublic(TopicInDB):
    articles_count = 0


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagPublic(TagBase):
    model_config = ConfigDict(from_attributes=True)

    pk: int
    slug: str
    created_at: datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator
    @classmethod
    def validate_password(cls, password):
        if not any(char.isupper() for char in password):
            raise ValueError("Password should contain at least one uppercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password should contain at least one digit")
        return password
        

class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    pk: int
    is_admin: bool
    is_active: bool
    created_at: datetime


class UserPublic(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


ArticlePublic.model_rebuild()
