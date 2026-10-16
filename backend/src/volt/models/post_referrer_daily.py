"""SQLAlchemy model for the PostReferrerDaily table."""

import enum
from datetime import date, datetime
import uuid
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, BINARY, INTEGER, TINYINT, CHAR, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class ReferrerKind(str, enum.Enum):
    direct = "direct"
    search = "search"
    social = "social"
    messaging = "messaging"
    newsletter = "newsletter"
    other = "other"


class PostReferrerDaily(Base):
    __tablename__ = "post_referrer_daily"
    __table_args__ = (Index("post_referrer_day_idx", "day"),)

    post_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    referrer_kind: Mapped[ReferrerKind] = mapped_column(
        Enum(ReferrerKind, name="daily_referrer_kind", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]), primary_key=True
    )
    referrer_host: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, server_default="")
    views: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
