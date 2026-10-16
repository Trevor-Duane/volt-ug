"""SQLAlchemy model for the ProjectStatDaily table."""

import enum
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class ProjectStatDaily(Base):
    __tablename__ = "project_stats_daily"

    project_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    usage_count: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    stars_total: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
