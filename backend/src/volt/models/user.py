import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    Uuid,
    func
)

from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base

class UserRole(str, enum.Enum):
    writer = "writer"
    admin = "admin"
    reader = "reader"

class UserStatus(str, enum.Enum):
    invited = "invited"
    active = "active"
    suspended = "suspended"

class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "CHAR_LENGTH(handle) BETWEEN 3 AND 30",
            name="ck_users_handle_length",
        ),
        CheckConstraint(
            "status = 'invited' OR password_hash IS NOT NULL",
            name="ck_users_password_required"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(320, collation="utf8mb4_unicode_ci"),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    handle: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            native_enum = False,
            values_callable=lambda cls: [item.value for item in cls],
            length=20
        ),
        nullable=False,
        default=UserRole.writer,
        server_default=UserRole.writer
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(
            UserStatus,
            native_enum=False,
            values_callable = lambda cls: [item.value for item in cls],
            length=20
        ),
        nullable=False,
        default=UserStatus.invited,
        server_default=UserStatus.invited,
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    vatar_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    github_username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    npm_username: Mapped[str | None] = mapped_column(String(100), nullable=True)

    invited_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

