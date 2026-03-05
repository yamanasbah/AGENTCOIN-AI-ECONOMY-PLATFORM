"""0003 agent wallet token system

Revision ID: 0003_agent_wallet_token_system
Revises: 0002_agent_wallet_economy
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_agent_wallet_token_system"
down_revision = "0002_agent_wallet_economy"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_wallets_user_id", table_name="wallets")
    op.drop_column("wallets", "user_id")
    op.drop_column("wallets", "agc_balance")
    op.drop_column("wallets", "staked_balance")
    op.add_column("wallets", sa.Column("owner_type", sa.Enum("user", "agent", name="walletownertype"), nullable=False, server_default="user"))
    op.add_column("wallets", sa.Column("owner_id", sa.String(length=64), nullable=False, server_default="0"))
    op.add_column("wallets", sa.Column("balance", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.add_column("wallets", sa.Column("locked_balance", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.create_index("ix_wallet_owner", "wallets", ["owner_type", "owner_id"], unique=False)

    op.create_table(
        "token_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=False),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("type", sa.Enum("mint", "burn", "reward", "transfer", "fee", name="tokentransactiontype"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_token_transactions_wallet_id", "token_transactions", ["wallet_id"])

    op.drop_table("wallet_transactions")
    op.drop_table("stakes")
    op.create_table(
        "stakes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=False),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("reward_rate", sa.Numeric(8, 4), nullable=False),
    )
    op.create_index("ix_stakes_wallet_id", "stakes", ["wallet_id"])

    op.add_column("managed_agents", sa.Column("initial_capital", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.alter_column("managed_agents", "status", type_=sa.Enum("created", "running", "paused", name="agentstatus"), existing_type=sa.Enum("created", "running", "stopped", name="agentstatus"))
    op.alter_column(
        "managed_agents",
        "strategy_type",
        type_=sa.Enum("grid_trading", "momentum", "arbitrage", "ai_trader", name="agentstrategytype"),
        existing_type=sa.Enum("trading", "marketing", "research", "arbitrage", "social", name="agentstrategytype"),
    )


def downgrade() -> None:
    op.drop_column("managed_agents", "initial_capital")
    op.drop_index("ix_stakes_wallet_id", table_name="stakes")
    op.drop_table("stakes")
    op.drop_index("ix_token_transactions_wallet_id", table_name="token_transactions")
    op.drop_table("token_transactions")
    op.drop_index("ix_wallet_owner", table_name="wallets")
    op.drop_column("wallets", "locked_balance")
    op.drop_column("wallets", "balance")
    op.drop_column("wallets", "owner_id")
    op.drop_column("wallets", "owner_type")
