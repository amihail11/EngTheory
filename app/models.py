from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    pk: Mapped[int] = mapped_column("id", Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")


class Topic(Base):
    __tablename__ = "topic"

    pk: Mapped[int] = mapped_column("id", Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    articles: Mapped[list["Article"]] = relationship(
        "Article", back_populates="topic", cascade="all, delete-orphan"
    )


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(String(500), nullable=True)
    reading_time_minutes: Mapped[int] = mapped_column(Integer, default=5)

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topic.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))

    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    views_counter: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    topic: Mapped["Topic"] = relationship("Topic", back_populates="articles")
    author: Mapped["User" | None] = relationship("User", back_populates="articles")
