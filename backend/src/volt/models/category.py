"""SQLAlchemy model for the Category table."""

from sqlalchemy import CheckConstraint, SmallInteger, String, UniqueConstraint, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column
from volt.db.base import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("slug", name="categories_slug_uk"),
        CheckConstraint(
            "REGEXP_LIKE(slug, '^[a-z0-9]+(-[a-z0-9]+)*$', 'c')",
            name="categories_slug_ck",
        ),
    )

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    sort_order: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text("0"))
