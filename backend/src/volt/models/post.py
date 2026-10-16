"""SQLAlchemy model for the Post table."""

import enum
import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, SMALLINT, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base

class PostStatus(str, enum.Enum):
    draft = "draft"
    in_review = "in_review"
    published = "published"
    unpublished = "unpublished"


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        Index("posts_author_idx", "author_id", "status", "deleted_at"),
        Index("posts_feed_idx", "status", "deleted_at", "published_at"),
        Index("posts_category_idx", "category_id", "status", "published_at"),
        Index("posts_featured_idx", "is_featured", "published_at"),
        Index("posts_review_idx", "status", "review_requested_at"),
        Index("posts_reviewer_idx", "reviewed_by"),
        Index("posts_cover_idx", "cover_media_id"),
        Index("posts_ft_all", "title", "excerpt", "body_md", mysql_prefix="FULLTEXT"),
        Index("posts_ft_title", "title", mysql_prefix="FULLTEXT"),
        UniqueConstraint("slug", name="posts_slug_uk"),
        CheckConstraint(
            "REGEXP_LIKE(slug, '^[a-z0-9]+(-[a-z0-9]+)*$', 'c')",
            name="posts_slug_ck",
        ),
        CheckConstraint(
            "status <> 'published' OR published_at IS NOT NULL",
            name="posts_published_ck",
        ),
        CheckConstraint(
            "is_featured = 0 OR status = 'published'",
            name="posts_featured_ck",
        ),
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    # The supplied SQL used INT UNSIGNED for user references. Volt's users.id is UUID,
    # so these references intentionally use SQLAlchemy Uuid to match users.id.
    author_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    category_id: Mapped[int | None] = mapped_column(
        SMALLINT(unsigned=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(220), nullable=True)
    body_md: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=False)
    cover_media_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("media.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, name="post_status", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=PostStatus.draft, server_default="draft"
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
    reading_minutes: Mapped[int] = mapped_column(
        SMALLINT(unsigned=True), nullable=False, default=1, server_default=text("1")
    )
    seo_title: Mapped[str | None] = mapped_column(String(70), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(160), nullable=True)
    canonical_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    review_requested_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    review_note: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
