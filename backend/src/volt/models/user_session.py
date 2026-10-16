import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Uuid,
    text,
)

from sqlalchemy.dialects.mysql import BIGINT, BINARY, VARBINARY
from sqlalchemy.orm import Mapped, mapped_column

from volt.db.base import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    __table_args__ = (
        UniqueConstraint(
            "token_hash",
            name="user_sessions_token_uk",
        ),
        Index(
            "user_sessions_user_idx",
            "user_id",
            "revoked_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[bytes] = mapped_column(
        BINARY(32),
        nullable=False,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    ip: Mapped[bytes | None] = mapped_column(
        VARBINARY(16),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
