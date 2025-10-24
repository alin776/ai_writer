"""add chapter status enum column

Revision ID: e1f2g3h4i5j6
Revises: d1e2f3g4h5i6
Create Date: 2025-10-24 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1f2g3h4i5j6'
down_revision = 'd1e2f3g4h5i6'
branch_labels = None
depends_on = None


chapter_status_enum = sa.Enum('draft', 'published', 'archived', name='chapterstatus')


def upgrade() -> None:
    bind = op.get_bind()
    chapter_status_enum.create(bind, checkfirst=True)

    op.add_column(
        'chapters',
        sa.Column(
            'status',
            chapter_status_enum,
            nullable=False,
            server_default=sa.text("'draft'::chapterstatus")
        )
    )

    op.execute("UPDATE chapters SET status = 'published' WHERE is_published = TRUE")
    op.execute("UPDATE chapters SET status = 'draft' WHERE is_published = FALSE OR is_published IS NULL")

    op.alter_column('chapters', 'status', server_default=None)
    op.create_index(op.f('ix_chapters_status'), 'chapters', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_chapters_status'), table_name='chapters')
    op.drop_column('chapters', 'status')
    chapter_status_enum.drop(op.get_bind(), checkfirst=True)
