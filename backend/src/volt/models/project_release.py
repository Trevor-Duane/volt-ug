"""SQLAlchemy model for the ProjectRelease table."""

import enum
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class ProjectRelease(Base):
    __tablename__ = "project_releases"
    __table_args__ = (
        UniqueConstraint("project_id", "version", name="project_releases_version_uk"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    notes_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    released_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
