"""SQLAlchemy model for the Tag table."""

from sqlalchemy import CheckConstraint, SmallInteger, String, UniqueConstraint, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("slug", name="tags_slug_uk"),
        CheckConstraint(
            "REGEXP_LIKE(slug, '^[a-z0-9.+#-]+$', 'c')",
            name="tags_slug_ck",
        ),
    )

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
