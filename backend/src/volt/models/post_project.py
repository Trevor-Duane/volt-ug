"""SQLAlchemy model for the PostProject table."""

import enum
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class PostProject(Base):
    __tablename__ = "post_projects"
    __table_args__ = (Index("post_projects_project_idx", "project_id"),)

    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
