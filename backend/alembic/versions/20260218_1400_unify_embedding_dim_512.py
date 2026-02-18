"""unify_embedding_dim_512

统一 Embedding 模型为 BAAI/bge-small-zh-v1.5（512 维），
旧的 384 维向量无法在新模型下使用，需要清空后重新生成。

Revision ID: unify_embedding_dim_512
Revises: drop_review_tables
Create Date: 2026-02-18 14:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "unify_embedding_dim_512"
down_revision = "drop_review_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 旧的 384 维向量在 512 维模型下无意义，必须清空
    op.execute("DELETE FROM novel_analysis_vectors")
    op.execute("ALTER TABLE novel_analysis_vectors ALTER COLUMN embedding TYPE vector(512)")


def downgrade() -> None:
    op.execute("DELETE FROM novel_analysis_vectors")
    op.execute("ALTER TABLE novel_analysis_vectors ALTER COLUMN embedding TYPE vector(384)")
