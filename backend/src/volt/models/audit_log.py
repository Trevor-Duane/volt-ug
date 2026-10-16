"""SQLAlchemy model for the AuditLog table."""

from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, Index, JSON, String, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("audit_log_entity_idx", "entity_type", "entity_id", "created_at"),
        Index("audit_log_actor_idx", "actor_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    ip: Mapped[bytes | None] = mapped_column(VARBINARY(16), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
