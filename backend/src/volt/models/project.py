"""SQLAlchemy model for the Project table."""

import enum
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base

class ProjectType(str, enum.Enum):
    library = "library"
    plugin = "plugin"
    product = "product"


class ProjectStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        Index("projects_owner_idx", "owner_id", "status", "deleted_at"),
        Index("projects_public_idx", "status", "deleted_at", "type", "latest_release_at"),
        UniqueConstraint("slug", name="projects_slug_uk"),
        UniqueConstraint("npm_package", name="projects_npm_uk"),
        CheckConstraint(
            "REGEXP_LIKE(slug, '^[a-z0-9]+(-[a-z0-9]+)*$', 'c')",
            name="projects_slug_ck",
        ),
        CheckConstraint("CHAR_LENGTH(summary) >= 20", name="projects_summary_ck"),
        CheckConstraint(
            "npm_package IS NULL OR REGEXP_LIKE(npm_package, '^(@[a-z0-9~-][a-z0-9._~-]*/)?[a-z0-9~-][a-z0-9._~-]*$', 'c')",
            name="projects_npm_ck",
        ),
        CheckConstraint(
            "latest_version IS NULL OR REGEXP_LIKE(latest_version, '^[0-9]+[.][0-9]+[.][0-9]+([-+].+)?$')",
            name="projects_version_ck",
        ),
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[ProjectType] = mapped_column(
        Enum(ProjectType, name="project_type", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]), nullable=False
    )
    summary: Mapped[str] = mapped_column(String(200), nullable=False)
    description_md: Mapped[str | None] = mapped_column(MEDIUMTEXT, nullable=True)
    npm_package: Mapped[str | None] = mapped_column(String(214), nullable=True)
    repo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    homepage_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    marketplace_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    license: Mapped[str | None] = mapped_column(String(40), nullable=True)
    latest_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    latest_release_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status", native_enum=True,
             values_callable=lambda cls: [item.value for item in cls]),
        nullable=False, default=ProjectStatus.draft, server_default="draft"
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
