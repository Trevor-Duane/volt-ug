"""SQLAlchemy model for the PostStatsDaily table."""

import enum
from datetime import date, datetime
import uuid
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, BINARY, INTEGER, TINYINT, CHAR, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class PostStatsDaily(Base):
    __tablename__ = "post_stats_daily"
    __table_args__ = (
        Index("post_stats_author_idx", "author_id", "day"),
        Index("post_stats_day_idx", "day"),
    )

    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    author_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    views: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    unique_visitors: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    read_seconds_total: Mapped[int] = mapped_column(BIGINT(unsigned=True), nullable=False, default=0, server_default=text("0"))
    finished_count: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    subscribers_gained: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    comments_count: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
