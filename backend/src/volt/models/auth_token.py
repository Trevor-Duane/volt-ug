"""SQLAlchemy model for the AuthToken table."""

import enum
from datetime import datetime
import uuid
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Index, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, BINARY
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class AuthTokenPurpose(str, enum.Enum):
    invite = "invite"
    password_reset = "password_reset"
    email_verify = "email_verify"


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    __table_args__ = (
        UniqueConstraint("token_hash", name="auth_tokens_token_uk"),
        Index("auth_tokens_user_idx", "user_id", "purpose"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    purpose: Mapped[AuthTokenPurpose] = mapped_column(
        Enum(
            AuthTokenPurpose,
            name="auth_token_purpose",
            native_enum=True,
            values_callable=lambda cls: [item.value for item in cls],
        ),
        nullable=False,
    )
    token_hash: Mapped[bytes] = mapped_column(BINARY(32), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
