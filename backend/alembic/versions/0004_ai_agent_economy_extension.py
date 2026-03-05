"""extend ai agent economy system

Revision ID: 0004_ai_agent_economy_extension
Revises: 0003_agent_wallet_token_system
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0004_ai_agent_economy_extension"
down_revision = "0003_agent_wallet_token_system"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("managed_agents", sa.Column("tenant_id", sa.String(length=64), nullable=False, server_default="default"))
    op.add_column("managed_agents", sa.Column("agent_type", sa.Enum(
        "marketing_agent", "trading_agent", "research_agent", "automation_agent", "custom_agent", name="agenttype"
    ), nullable=False, server_default="custom_agent"))
    op.add_column("managed_agents", sa.Column("system_prompt", sa.Text(), nullable=False, server_default="You are a helpful AI agent"))
    op.add_column("managed_agents", sa.Column("capabilities", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")))
    op.add_column("managed_agents", sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.alter_column(
        "managed_agents",
        "status",
        type_=sa.Enum("idle", "running", "paused", name="agentlifecyclestatus"),
        postgresql_using="CASE status::text WHEN 'created' THEN 'idle' ELSE status::text END::agentlifecyclestatus",
        existing_type=sa.Enum("created", "running", "paused", name="agentstatus"),
    )
    op.create_index("ix_managed_agents_tenant_id", "managed_agents", ["tenant_id"], unique=False)

    op.create_table(
        "transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("from_wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=True),
        sa.Column("to_wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=True),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("type", sa.Enum("transfer", "stake", "unstake", "execution", "marketplace_purchase", name="transactiontype"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_transactions_from_wallet_id", "transactions", ["from_wallet_id"])
    op.create_index("ix_transactions_to_wallet_id", "transactions", ["to_wallet_id"])

    op.add_column("stakes", sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")))
    op.add_column("stakes", sa.Column("unlock_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")))

    op.create_table(
        "agent_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("execution_message", sa.Text(), nullable=False),
        sa.Column("tokens_consumed", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_logs_agent_id", "agent_logs", ["agent_id"])

    op.alter_column("marketplace_listings", "agent_id", type_=sa.String(length=64), existing_type=sa.Integer(), postgresql_using="agent_id::text")
    op.add_column("marketplace_listings", sa.Column("price_per_run", sa.Float(), nullable=False, server_default="1"))
    op.add_column("marketplace_listings", sa.Column("rating", sa.Float(), nullable=False, server_default="0"))
    op.add_column("marketplace_listings", sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.alter_column("marketplace_listings", "agent_id", type_=sa.Integer(), existing_type=sa.String(length=64), postgresql_using="agent_id::integer")
    op.drop_column("marketplace_listings", "usage_count")
    op.drop_column("marketplace_listings", "rating")
    op.drop_column("marketplace_listings", "price_per_run")
    op.drop_index("ix_agent_logs_agent_id", table_name="agent_logs")
    op.drop_table("agent_logs")
    op.drop_column("stakes", "unlock_at")
    op.drop_column("stakes", "created_at")
    op.drop_index("ix_transactions_to_wallet_id", table_name="transactions")
    op.drop_index("ix_transactions_from_wallet_id", table_name="transactions")
    op.drop_table("transactions")
    op.drop_index("ix_managed_agents_tenant_id", table_name="managed_agents")
    op.alter_column("managed_agents", "status", type_=sa.Enum("created", "running", "paused", name="agentstatus"), existing_type=sa.Enum("idle", "running", "paused", name="agentlifecyclestatus"))
    op.drop_column("managed_agents", "is_public")
    op.drop_column("managed_agents", "capabilities")
    op.drop_column("managed_agents", "system_prompt")
    op.drop_column("managed_agents", "agent_type")
    op.drop_column("managed_agents", "tenant_id")
