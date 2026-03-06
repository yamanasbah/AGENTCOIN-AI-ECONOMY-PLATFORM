"""auth, api keys, tasks, notifications and autonomous fields

Revision ID: 0009_auth_api_keys_tasks_notifications_analytics
Revises: 0008_agent_economy_profit_distribution
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0009_auth_api_keys_tasks_notifications_analytics"
down_revision = "0008_agent_economy_profit_distribution"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("username", sa.String(length=120), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))

    op.execute("UPDATE users SET password_hash = hashed_password WHERE password_hash IS NULL")
    op.execute("UPDATE users SET username = split_part(email, '@', 1) || '_' || id::text WHERE username IS NULL")

    op.alter_column("users", "password_hash", nullable=False)
    op.alter_column("users", "username", nullable=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "api_keys",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_api_keys_user_id", "api_keys", ["user_id"], unique=False)
    op.create_index("ix_api_keys_key", "api_keys", ["key"], unique=True)

    op.add_column("managed_agents", sa.Column("is_autonomous", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("managed_agents", sa.Column("run_interval_seconds", sa.Integer(), nullable=False, server_default="300"))

    op.create_table(
        "agent_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("task_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_agent_tasks_agent_id", "agent_tasks", ["agent_id"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("ix_agent_tasks_agent_id", table_name="agent_tasks")
    op.drop_table("agent_tasks")

    op.drop_column("managed_agents", "run_interval_seconds")
    op.drop_column("managed_agents", "is_autonomous")

    op.drop_index("ix_api_keys_key", table_name="api_keys")
    op.drop_index("ix_api_keys_user_id", table_name="api_keys")
    op.drop_table("api_keys")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "is_active")
    op.drop_column("users", "username")
    op.drop_column("users", "password_hash")
