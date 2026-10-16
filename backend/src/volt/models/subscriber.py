"""SQLAlchemy model for the Subscriber table."""

import enum
from datetime import datetime
import uuid
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base

class SubscriberStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    unsubscribed = "unsubscribed"

class Subscriber(Base):
    __tablename__ = "subscribers"
    __table_args__ = (
        UniqueConstraint("email", name="subscribers_email_uk"),
        Index("subscribers_source_idx", "source_post_id"),
        Index("subscribers_confirmed_idx", "confirmed_at"),
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[SubscriberStatus] = mapped_column(
        Enum(SubscriberStatus, name="subscriber_status", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=SubscriberStatus.pending, server_default="pending"
    )
    source_post_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("posts.id", ondelete="SET NULL"), nullable=True
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    unsubscribed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
