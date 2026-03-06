"""platform control center

Revision ID: 0011_platform_control_center
Revises: 0010_ai_agent_app_store
Create Date: 2026-03-06
"""

import uuid
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0011_platform_control_center"
down_revision = "0010_ai_agent_app_store"
branch_labels = None
depends_on = None


user_role_enum = sa.Enum("user", "creator", "admin", "super_admin", name="userrole")
agent_moderation_enum = sa.Enum("pending", "approved", "rejected", "banned", name="agentmoderationstatus")


def upgrade() -> None:
    bind = op.get_bind()

    user_role_enum.create(bind, checkfirst=True)
    op.add_column("users", sa.Column("role", user_role_enum, nullable=False, server_default="user"))
    op.execute("UPDATE users SET role = 'admin' WHERE is_admin = true")

    agent_moderation_enum.create(bind, checkfirst=True)
    op.add_column("managed_agents", sa.Column("agent_status", agent_moderation_enum, nullable=False, server_default="pending"))

    op.create_table(
        "platform_treasury",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=False),
        sa.Column("total_revenue", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("total_distributed", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_platform_treasury_wallet_id", "platform_treasury", ["wallet_id"], unique=True)

    op.create_table(
        "agent_flags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("reason", sa.String(length=128), nullable=False),
        sa.Column("flag_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_flags_agent_id", "agent_flags", ["agent_id"], unique=False)

    op.create_table(
        "feature_flags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_feature_flags_name", "feature_flags", ["name"], unique=True)

    now = datetime.utcnow()
    feature_flags = sa.table(
        "feature_flags",
        sa.column("name", sa.String),
        sa.column("enabled", sa.Boolean),
        sa.column("created_at", sa.DateTime),
    )
    op.bulk_insert(
        feature_flags,
        [
            {"name": "enable_marketplace", "enabled": True, "created_at": now},
            {"name": "enable_autonomous_agents", "enabled": True, "created_at": now},
            {"name": "enable_staking", "enabled": True, "created_at": now},
            {"name": "enable_api_access", "enabled": True, "created_at": now},
        ],
    )

    wallet_id = uuid.uuid4()
    op.execute(
        sa.text(
            """
            INSERT INTO wallets (id, owner_type, owner_id, balance, locked_balance, created_at)
            VALUES (:wallet_id, 'treasury', 'platform', 0, 0, :created_at)
            ON CONFLICT DO NOTHING
            """
        ).bindparams(wallet_id=wallet_id, created_at=now)
    )
    op.execute(
        sa.text(
            """
            INSERT INTO platform_treasury (wallet_id, total_revenue, total_distributed, created_at)
            SELECT :wallet_id, 0, 0, :created_at
            WHERE NOT EXISTS (SELECT 1 FROM platform_treasury)
            """
        ).bindparams(wallet_id=wallet_id, created_at=now)
    )


def downgrade() -> None:
    op.drop_index("ix_feature_flags_name", table_name="feature_flags")
    op.drop_table("feature_flags")

    op.drop_index("ix_agent_flags_agent_id", table_name="agent_flags")
    op.drop_table("agent_flags")

    op.drop_index("ix_platform_treasury_wallet_id", table_name="platform_treasury")
    op.drop_table("platform_treasury")

    op.drop_column("managed_agents", "agent_status")
    agent_moderation_enum.drop(op.get_bind(), checkfirst=True)

    op.drop_column("users", "role")
    user_role_enum.drop(op.get_bind(), checkfirst=True)
