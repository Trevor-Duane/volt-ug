"""SQLAlchemy model for the SiteSetting table."""

from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, Index, JSON, String, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class SiteSetting(Base):
    __tablename__ = "site_settings"
    __table_args__ = (Index("site_settings_user_idx", "updated_by"),)

    setting_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    setting_value: Mapped[dict] = mapped_column(JSON, nullable=False)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
