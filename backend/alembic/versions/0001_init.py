"""initial schema

Revision ID: 0001_init
Revises:
Create Date: 2026-03-04
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "agents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("agent_type", sa.Enum("trading", "marketing", "arbitrage", "social_growth", "custom", name="agenttype"), nullable=False),
        sa.Column("runtime_status", sa.Enum("draft", "active", "paused", "safe_mode", name="runtimestatus"), nullable=True),
        sa.Column("budget_allocation", sa.Float(), nullable=True),
        sa.Column("max_drawdown", sa.Float(), nullable=True),
        sa.Column("commission_model", sa.String(length=64), nullable=True),
        sa.Column("staking_requirement", sa.Float(), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    for name, cols in {
        "agent_configs": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), unique=True),
            sa.Column("risk_configuration", sa.JSON()),
            sa.Column("runtime_settings", sa.JSON()),
        ],
        "trades": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("symbol", sa.String(length=50), nullable=False),
            sa.Column("pnl", sa.Float()),
            sa.Column("executed_at", sa.DateTime()),
        ],
        "performance_metrics": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("roi", sa.Float()),
            sa.Column("sharpe_ratio", sa.Float()),
            sa.Column("rank_score", sa.Float()),
            sa.Column("measured_at", sa.DateTime()),
        ],
        "equity_snapshots": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("equity", sa.Float()),
            sa.Column("captured_at", sa.DateTime()),
        ],
        "stakes": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("amount", sa.Float(), nullable=False),
            sa.Column("tx_hash", sa.String(length=120)),
            sa.Column("created_at", sa.DateTime()),
        ],
        "commissions": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("beneficiary_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("amount", sa.Float(), nullable=False),
            sa.Column("token_symbol", sa.String(length=16)),
            sa.Column("distributed_at", sa.DateTime()),
        ],
        "subscriptions": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("tier", sa.String(length=64), nullable=False),
            sa.Column("amount_token", sa.Float(), nullable=False),
            sa.Column("active", sa.Boolean()),
            sa.Column("started_at", sa.DateTime()),
        ],
        "marketplace_listings": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id"), nullable=False),
            sa.Column("revenue_share_percent", sa.Float()),
            sa.Column("price_per_month_token", sa.Float()),
            sa.Column("active", sa.Boolean()),
        ],
        "audit_logs": [
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64)),
            sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id")),
            sa.Column("action", sa.String(length=120), nullable=False),
            sa.Column("metadata", sa.JSON()),
            sa.Column("created_at", sa.DateTime()),
        ],
    }.items():
        op.create_table(name, *cols)


def downgrade() -> None:
    for table in [
        "audit_logs",
        "marketplace_listings",
        "subscriptions",
        "commissions",
        "stakes",
        "equity_snapshots",
        "performance_metrics",
        "trades",
        "agent_configs",
        "agents",
        "users",
    ]:
        op.drop_table(table)
