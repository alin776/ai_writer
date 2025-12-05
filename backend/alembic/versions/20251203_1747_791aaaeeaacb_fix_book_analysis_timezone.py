"""fix_book_analysis_timezone

Revision ID: 791aaaeeaacb
Revises: f31b356bab4a
Create Date: 2025-12-03 17:47:50.400493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791aaaeeaacb'
down_revision = 'f31b356bab4a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 修改book_analysis_jobs表的时间戳列，添加timezone支持
    # 注意：这个迁移会转换现有数据，假设现有数据是UTC时间

    # 修改created_at列
    op.alter_column('book_analysis_jobs', 'created_at',
                    type_=sa.DateTime(timezone=True),
                    server_default=sa.text('now()'),
                    nullable=False,
                    existing_type=sa.DateTime(),
                    existing_nullable=False)

    # 修改started_at列
    op.alter_column('book_analysis_jobs', 'started_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    existing_nullable=True)

    # 修改completed_at列
    op.alter_column('book_analysis_jobs', 'completed_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    existing_nullable=True)

    # 修改updated_at列
    op.alter_column('book_analysis_jobs', 'updated_at',
                    type_=sa.DateTime(timezone=True),
                    server_default=sa.text('now()'),
                    existing_type=sa.DateTime(),
                    existing_nullable=True)


def downgrade() -> None:
    # 回滚：移除timezone支持，恢复为naive datetime

    op.alter_column('book_analysis_jobs', 'created_at',
                    type_=sa.DateTime(),
                    server_default=None,
                    nullable=False,
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('book_analysis_jobs', 'started_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('book_analysis_jobs', 'completed_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('book_analysis_jobs', 'updated_at',
                    type_=sa.DateTime(),
                    server_default=None,
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)
