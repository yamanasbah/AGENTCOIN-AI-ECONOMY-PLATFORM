"""add agent memory and execution log extensions

Revision ID: 0006_agent_memory_and_log_fields
Revises: 0005_agent_runtime_logs
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0006_agent_memory_and_log_fields"
down_revision = "0005_agent_runtime_logs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_memory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_memory_agent_id", "agent_memory", ["agent_id"], unique=False)

    op.add_column("agent_logs", sa.Column("input_text", sa.Text(), nullable=True))
    op.add_column("agent_logs", sa.Column("output_text", sa.Text(), nullable=True))
    op.add_column("agent_logs", sa.Column("execution_cost", sa.Numeric(18, 4), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("agent_logs", "execution_cost")
    op.drop_column("agent_logs", "output_text")
    op.drop_column("agent_logs", "input_text")
    op.drop_index("ix_agent_memory_agent_id", table_name="agent_memory")
    op.drop_table("agent_memory")
