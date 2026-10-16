"""create analytics procedures

Revision ID: 27758f10ef99
Revises: 2fd39267674e
Create Date: 2026-10-14 14:19:16.010053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27758f10ef99'
down_revision: Union[str, Sequence[str], None] = '2fd39267674e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Procedure 1: rebuild daily analytics for a UTC day.
    op.execute("""
        CREATE PROCEDURE rollup_day(IN p_day DATE)
        BEGIN
            DECLARE d0 DATETIME;
            DECLARE d1 DATETIME;

            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;

            SET d0 = TIMESTAMP(p_day);
            SET d1 = TIMESTAMP(DATE_ADD(p_day, INTERVAL 1 DAY));

            START TRANSACTION;

            DELETE FROM post_stats_daily
            WHERE day = p_day;

            DELETE FROM post_referrer_daily
            WHERE day = p_day;

            DELETE FROM post_country_daily
            WHERE day = p_day;

            INSERT INTO post_stats_daily
                (
                    post_id, day, author_id, views, unique_visitors,
                    read_seconds_total, finished_count
                )
            SELECT
                v.post_id,
                p_day,
                p.author_id,
                COUNT(*),
                COUNT(DISTINCT v.visitor_hash),
                SUM(v.read_seconds),
                SUM(v.finished)
            FROM post_views v
            JOIN posts p ON p.id = v.post_id
            WHERE v.occurred_at >= d0
              AND v.occurred_at < d1
            GROUP BY v.post_id, p.author_id;

            INSERT INTO post_referrer_daily
                (post_id, day, referrer_kind, referrer_host, views)
            SELECT
                v.post_id,
                p_day,
                v.referrer_kind,
                COALESCE(v.referrer_host, ''),
                COUNT(*)
            FROM post_views v
            JOIN posts p ON p.id = v.post_id
            WHERE v.occurred_at >= d0
              AND v.occurred_at < d1
            GROUP BY
                v.post_id,
                v.referrer_kind,
                COALESCE(v.referrer_host, '');

            INSERT INTO post_country_daily
                (post_id, day, country, views)
            SELECT
                v.post_id,
                p_day,
                COALESCE(v.country, 'ZZ'),
                COUNT(*)
            FROM post_views v
            JOIN posts p ON p.id = v.post_id
            WHERE v.occurred_at >= d0
              AND v.occurred_at < d1
            GROUP BY v.post_id, COALESCE(v.country, 'ZZ');

            -- Add rows for subscriber or comment activity even
            -- when an article had no page views.
            INSERT INTO post_stats_daily (post_id, day, author_id)
            SELECT p.id, p_day, p.author_id
            FROM posts p
            WHERE NOT EXISTS (
                SELECT 1
                FROM post_stats_daily s
                WHERE s.post_id = p.id AND s.day = p_day
            )
            AND (
                p.id IN (
                    SELECT source_post_id
                    FROM subscribers
                    WHERE confirmed_at >= d0
                      AND confirmed_at < d1
                      AND source_post_id IS NOT NULL
                )
                OR p.id IN (
                    SELECT post_id
                    FROM comments
                    WHERE status = 'approved'
                      AND created_at >= d0
                      AND created_at < d1
                )
            );

            UPDATE post_stats_daily s
            JOIN (
                SELECT source_post_id AS post_id, COUNT(*) AS n
                FROM subscribers
                WHERE confirmed_at >= d0
                  AND confirmed_at < d1
                  AND source_post_id IS NOT NULL
                GROUP BY source_post_id
            ) x ON x.post_id = s.post_id
            SET s.subscribers_gained = x.n
            WHERE s.day = p_day;

            UPDATE post_stats_daily s
            JOIN (
                SELECT post_id, COUNT(*) AS n
                FROM comments
                WHERE status = 'approved'
                  AND created_at >= d0
                  AND created_at < d1
                GROUP BY post_id
            ) x ON x.post_id = s.post_id
            SET s.comments_count = x.n
            WHERE s.day = p_day;

            COMMIT;
        END
    """)

    # Procedure 2: create a missing future monthly partition.
    op.execute("""
        CREATE PROCEDURE ensure_post_views_partition(IN p_month DATE)
        BEGIN
            DECLARE pname VARCHAR(16);
            DECLARE bound DATE;

            SET bound = DATE_ADD(
                DATE_FORMAT(p_month, '%Y-%m-01'),
                INTERVAL 1 MONTH
            );

            SET pname = CONCAT('p', DATE_FORMAT(p_month, '%Y_%m'));

            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.PARTITIONS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'post_views'
                  AND PARTITION_NAME = pname
            ) THEN
                SET @volt_sql = CONCAT(
                    'ALTER TABLE post_views ',
                    'REORGANIZE PARTITION pmax INTO (',
                    'PARTITION ', pname,
                    ' VALUES LESS THAN (''', bound,
                    ' 00:00:00''), ',
                    'PARTITION pmax VALUES LESS THAN (MAXVALUE))'
                );

                PREPARE stmt FROM @volt_sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            END IF;
        END
    """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS ensure_post_views_partition")
    op.execute("DROP PROCEDURE IF EXISTS rollup_day")
