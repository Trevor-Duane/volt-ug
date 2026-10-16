"""partition post views by month

Revision ID: f5a3d99fb782
Revises: 27758f10ef99
Create Date: 2026-10-14 14:23:13.468657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5a3d99fb782'
down_revision: Union[str, Sequence[str], None] = '27758f10ef99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
