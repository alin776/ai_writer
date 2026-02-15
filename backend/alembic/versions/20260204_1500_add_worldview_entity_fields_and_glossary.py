"""add_worldview_entity_glossary

Revision ID: add_worldview_entity_glossary
Revises: add_work_guidelines_fields
Create Date: 2026-02-04 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "add_worldview_entity_glossary"
down_revision = "add_work_guidelines_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # characters: 补齐实体字段
    char_columns = [col['name'] for col in inspector.get_columns('characters')]
    if 'status' not in char_columns:
        op.add_column("characters", sa.Column("status", sa.String(length=100), nullable=True))
    if 'voice' not in char_columns:
        op.add_column("characters", sa.Column("voice", sa.String(length=200), nullable=True))
    if 'aliases' not in char_columns:
        op.add_column("characters", sa.Column("aliases", postgresql.JSON(), nullable=True))
    if 'constraints' not in char_columns:
        op.add_column("characters", sa.Column("constraints", postgresql.JSON(), nullable=True))
    if 'evidence' not in char_columns:
        op.add_column("characters", sa.Column("evidence", postgresql.JSON(), nullable=True))

    # locations: 补齐实体字段
    loc_columns = [col['name'] for col in inspector.get_columns('locations')]
    if 'status' not in loc_columns:
        op.add_column("locations", sa.Column("status", sa.String(length=100), nullable=True))
    if 'voice' not in loc_columns:
        op.add_column("locations", sa.Column("voice", sa.String(length=200), nullable=True))
    if 'aliases' not in loc_columns:
        op.add_column("locations", sa.Column("aliases", postgresql.JSON(), nullable=True))
    if 'relations' not in loc_columns:
        op.add_column("locations", sa.Column("relations", postgresql.JSON(), nullable=True))
    if 'constraints' not in loc_columns:
        op.add_column("locations", sa.Column("constraints", postgresql.JSON(), nullable=True))
    if 'evidence' not in loc_columns:
        op.add_column("locations", sa.Column("evidence", postgresql.JSON(), nullable=True))

    # settings: 补齐实体字段
    set_columns = [col['name'] for col in inspector.get_columns('settings')]
    if 'status' not in set_columns:
        op.add_column("settings", sa.Column("status", sa.String(length=100), nullable=True))
    if 'voice' not in set_columns:
        op.add_column("settings", sa.Column("voice", sa.String(length=200), nullable=True))
    if 'aliases' not in set_columns:
        op.add_column("settings", sa.Column("aliases", postgresql.JSON(), nullable=True))
    if 'relations' not in set_columns:
        op.add_column("settings", sa.Column("relations", postgresql.JSON(), nullable=True))
    if 'constraints' not in set_columns:
        op.add_column("settings", sa.Column("constraints", postgresql.JSON(), nullable=True))
    if 'evidence' not in set_columns:
        op.add_column("settings", sa.Column("evidence", postgresql.JSON(), nullable=True))

    # glossary_terms - 检查表是否存在
    tables = inspector.get_table_names()
    if 'glossary_terms' not in tables:
        op.create_table(
            "glossary_terms",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column("work_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("term", sa.String(length=200), nullable=False),
            sa.Column("definition", sa.Text(), nullable=False),
            sa.Column("aliases", postgresql.JSON(), nullable=True),
            sa.Column("tags", postgresql.JSON(), nullable=True),
            sa.Column("evidence", postgresql.JSON(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id")
        )
        op.create_index("ix_glossary_terms_id", "glossary_terms", ["id"])
        op.create_index("ix_glossary_terms_work_id", "glossary_terms", ["work_id"])
        op.create_index("ix_glossary_terms_term", "glossary_terms", ["term"])


def downgrade() -> None:
    op.drop_index("ix_glossary_terms_term", table_name="glossary_terms")
    op.drop_index("ix_glossary_terms_work_id", table_name="glossary_terms")
    op.drop_index("ix_glossary_terms_id", table_name="glossary_terms")
    op.drop_table("glossary_terms")

    op.drop_column("settings", "evidence")
    op.drop_column("settings", "constraints")
    op.drop_column("settings", "relations")
    op.drop_column("settings", "aliases")
    op.drop_column("settings", "voice")
    op.drop_column("settings", "status")

    op.drop_column("locations", "evidence")
    op.drop_column("locations", "constraints")
    op.drop_column("locations", "relations")
    op.drop_column("locations", "aliases")
    op.drop_column("locations", "voice")
    op.drop_column("locations", "status")

    op.drop_column("characters", "evidence")
    op.drop_column("characters", "constraints")
    op.drop_column("characters", "aliases")
    op.drop_column("characters", "voice")
    op.drop_column("characters", "status")
