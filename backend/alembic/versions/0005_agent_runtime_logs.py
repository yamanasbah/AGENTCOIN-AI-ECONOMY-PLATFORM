"""add runtime log fields

Revision ID: 0005_agent_runtime_logs
Revises: 0004_ai_agent_economy_extension
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_agent_runtime_logs"
down_revision = "0004_ai_agent_economy_extension"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("agent_logs", sa.Column("input_payload", sa.Text(), nullable=True))
    op.add_column("agent_logs", sa.Column("output_payload", sa.Text(), nullable=True))
    op.add_column("agent_logs", sa.Column("tokens_used", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.add_column("agent_logs", sa.Column("execution_time", sa.Numeric(18, 6), nullable=False, server_default="0"))
    op.add_column("agent_logs", sa.Column("status", sa.String(length=32), nullable=False, server_default="success"))


def downgrade() -> None:
    op.drop_column("agent_logs", "status")
    op.drop_column("agent_logs", "execution_time")
    op.drop_column("agent_logs", "tokens_used")
    op.drop_column("agent_logs", "output_payload")
    op.drop_column("agent_logs", "input_payload")
