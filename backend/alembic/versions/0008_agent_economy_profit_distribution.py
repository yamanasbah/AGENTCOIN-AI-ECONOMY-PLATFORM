"""agent economy profit distribution fields

Revision ID: 0008_agent_economy_profit_distribution
Revises: 0007_agent_memory_key_value
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0008_agent_economy_profit_distribution"
down_revision = "0007_agent_memory_key_value"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE walletownertype ADD VALUE IF NOT EXISTS 'treasury'")

    op.add_column("managed_agents", sa.Column("total_earnings", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("total_runs", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("average_rating", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("success_rate", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("last_run_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("managed_agents", "last_run_at")
    op.drop_column("managed_agents", "success_rate")
    op.drop_column("managed_agents", "average_rating")
    op.drop_column("managed_agents", "total_runs")
    op.drop_column("managed_agents", "total_earnings")
