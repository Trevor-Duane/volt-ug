"""SQLAlchemy model for the Media table."""

from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class Media(Base):
    __tablename__ = "media"
    __table_args__ = (
        UniqueConstraint("storage_key", name="media_storage_key_uk"),
        Index("media_owner_idx", "owner_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    bytes: Mapped[int] = mapped_column(BIGINT(unsigned=True), nullable=False)
    width: Mapped[int | None] = mapped_column(SMALLINT(unsigned=True), nullable=True)
    height: Mapped[int | None] = mapped_column(SMALLINT(unsigned=True), nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
