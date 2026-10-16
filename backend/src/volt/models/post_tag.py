"""SQLAlchemy model for the PostTag table."""

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


class PostTag(Base):
    __tablename__ = "post_tags"
    __table_args__ = (Index("post_tags_tag_idx", "tag_id"),)

    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )
