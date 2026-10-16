"""create analytics events

Revision ID: 849a86795e03
Revises: f5a3d99fb782
Create Date: 2026-10-14 14:25:25.189665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '849a86795e03'
down_revision: Union[str, Sequence[str], None] = 'f5a3d99fb782'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Create the schedules using UTC as the session time zone.
    op.execute("SET time_zone = '+00:00'")

    # Rebuild today's analytics every hour.
    op.execute("""
        CREATE EVENT ev_rollup_today
        ON SCHEDULE EVERY 1 HOUR
        DO CALL rollup_day(UTC_DATE())
    """)

    # Rebuild yesterday's analytics daily at 00:15 UTC.
    op.execute("""
        CREATE EVENT ev_rollup_yesterday
        ON SCHEDULE EVERY 1 DAY
        STARTS (
            UTC_DATE() + INTERVAL 1 DAY + INTERVAL 15 MINUTE
        )
        DO CALL rollup_day(
            DATE_SUB(UTC_DATE(), INTERVAL 1 DAY)
        )
    """)

    # Ensure the partition two months ahead exists.
    op.execute("""
        CREATE EVENT ev_post_views_partitions
        ON SCHEDULE EVERY 1 WEEK
        DO CALL ensure_post_views_partition(
            DATE_ADD(UTC_DATE(), INTERVAL 2 MONTH)
        )
    """)


def downgrade() -> None:
    op.execute("DROP EVENT IF EXISTS ev_post_views_partitions")
    op.execute("DROP EVENT IF EXISTS ev_rollup_yesterday")
    op.execute("DROP EVENT IF EXISTS ev_rollup_today")
