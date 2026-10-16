"""SQLAlchemy model for the Comment table."""

import enum
from datetime import datetime
import uuid
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base

class CommentStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    spam = "spam"
    deleted = "deleted"

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = (
        Index("comments_post_idx", "post_id", "status", "created_at"),
        Index("comments_status_idx", "status", "created_at"),
        Index("comments_parent_idx", "parent_id"),
        Index("comments_mod_idx", "moderated_by"),
        CheckConstraint("CHAR_LENGTH(body) BETWEEN 1 AND 4000", name="comments_body_ck"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CommentStatus] = mapped_column(
        Enum(CommentStatus, name="comment_status", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=CommentStatus.pending, server_default="pending"
    )
    moderated_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    moderated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
