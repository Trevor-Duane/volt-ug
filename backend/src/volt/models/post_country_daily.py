"""SQLAlchemy model for the PostCountryDaily table."""

import enum
from datetime import date, datetime
import uuid
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, BINARY, INTEGER, TINYINT, CHAR, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class PostCountryDaily(Base):
    __tablename__ = "post_country_daily"
    __table_args__ = (Index("post_country_day_idx", "day"),)

    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    country: Mapped[str] = mapped_column(CHAR(2), primary_key=True, nullable=False, default="ZZ", server_default="ZZ")
    views: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
