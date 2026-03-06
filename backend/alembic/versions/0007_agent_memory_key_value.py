"""agent memory key value schema

Revision ID: 0007_agent_memory_key_value
Revises: 0006_agent_memory_and_log_fields
Create Date: 2026-03-06 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0007_agent_memory_key_value"
down_revision = "0006_agent_memory_and_log_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("agent_memory", "role", new_column_name="memory_key", existing_type=sa.String(length=32), nullable=False)
    op.alter_column("agent_memory", "content", new_column_name="memory_value", existing_type=sa.Text(), nullable=False)
    op.alter_column("agent_memory", "memory_key", type_=sa.String(length=128), existing_type=sa.String(length=32), nullable=False)


def downgrade() -> None:
    op.alter_column("agent_memory", "memory_key", type_=sa.String(length=32), existing_type=sa.String(length=128), nullable=False)
    op.alter_column("agent_memory", "memory_value", new_column_name="content", existing_type=sa.Text(), nullable=False)
    op.alter_column("agent_memory", "memory_key", new_column_name="role", existing_type=sa.String(length=32), nullable=False)
