"""SQLAlchemy model for the PostView table."""

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

class DeviceKind(str, enum.Enum):
    mobile = "mobile"
    desktop = "desktop"
    tablet = "tablet"


class PostView(Base):
    __tablename__ = "post_views"
    __table_args__ = (
        Index("post_views_post_time_idx", "post_id", "occurred_at"),
        Index("post_views_time_idx", "occurred_at"),
        CheckConstraint("scroll_pct <= 100", name="post_views_scroll_ck"),
    )

    # Partitioning by occurred_at is added manually to the generated migration; see README.
    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    post_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    visitor_hash: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)
    referrer_kind: Mapped[ReferrerKind] = mapped_column(
        Enum(ReferrerKind, name="view_referrer_kind", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=ReferrerKind.direct, server_default="direct"
    )
    referrer_host: Mapped[str | None] = mapped_column(String(255), nullable=True)
    utm_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[str | None] = mapped_column(String(100), nullable=True)
    utm_campaign: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(CHAR(2), nullable=True)
    device: Mapped[DeviceKind] = mapped_column(
        Enum(DeviceKind, name="view_device_kind", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=DeviceKind.desktop, server_default="desktop"
    )
    read_seconds: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, server_default=text("0"))
    scroll_pct: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False, default=0, server_default=text("0"))
    finished: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
