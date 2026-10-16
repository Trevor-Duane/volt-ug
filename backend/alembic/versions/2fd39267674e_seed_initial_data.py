"""seed initial data

Revision ID: 2fd39267674e
Revises: c25c794c7b81
Create Date: 2026-10-14 14:17:29.711918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fd39267674e'
down_revision: Union[str, Sequence[str], None] = 'c25c794c7b81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert the default categories without duplicating existing ones.
    op.execute("""
        INSERT IGNORE INTO categories (slug, name, sort_order)
        VALUES
            ('engineering', 'Engineering', 1),
            ('ai', 'AI', 2),
            ('security', 'Security', 3),
            ('tools', 'Dev Tools', 4),
            ('mobile', 'Mobile', 5)
    """)

    # Insert the initial setting if it doesn't already exist.
    op.execute("""
        INSERT IGNORE INTO site_settings (setting_key, setting_value)
        VALUES ('require_review', 'false')
    """)


def downgrade() -> None:
    # Intentionally preserve seed data because the application
    # may already be using these categories and settings.
    pass
