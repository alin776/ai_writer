"""add_user_stickers

Revision ID: 94e8fc7d9c2f
Revises: e2f3g4h5i6j7
Create Date: 2025-12-31 15:10:52.539576

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '94e8fc7d9c2f'
down_revision = 'e2f3g4h5i6j7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建贴图来源枚举类型
    sticker_source = postgresql.ENUM('upload', 'tenor', name='stickersource', create_type=False)
    sticker_source.create(op.get_bind(), checkfirst=True)

    # 创建用户自定义贴图表
    op.create_table(
        'user_stickers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=True, comment='贴图名称'),
        sa.Column('image_url', sa.String(500), nullable=False, comment='贴图图片URL'),
        sa.Column('preview_url', sa.String(500), nullable=True, comment='预览图URL'),
        sa.Column('source', sticker_source, nullable=False, server_default='upload', comment='贴图来源'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 创建用户收藏贴图表
    op.create_table(
        'user_favorite_stickers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('sticker_url', sa.String(500), nullable=False, comment='贴图URL'),
        sa.Column('preview_url', sa.String(500), nullable=True, comment='预览图URL'),
        sa.Column('source', sticker_source, nullable=False, server_default='tenor', comment='贴图来源'),
        sa.Column('tenor_id', sa.String(100), nullable=True, comment='Tenor贴图ID'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user_favorite_stickers')
    op.drop_table('user_stickers')

    # 删除枚举类型
    sticker_source = postgresql.ENUM('upload', 'tenor', name='stickersource', create_type=False)
    sticker_source.drop(op.get_bind(), checkfirst=True)
