"""SQLAlchemy model for the PostRevision table."""

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


class PostRevision(Base):
    __tablename__ = "post_revisions"
    __table_args__ = (
        Index("post_revisions_post_idx", "post_id", "created_at"),
        Index("post_revisions_editor_idx", "editor_id"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    editor_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body_md: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
