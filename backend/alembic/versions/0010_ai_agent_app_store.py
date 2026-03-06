"""ai agent app store

Revision ID: 0010_ai_agent_app_store
Revises: 0009_auth_api_keys_tasks_notifications_analytics
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0010_ai_agent_app_store"
down_revision = "0009_auth_api_keys_tasks_notifications_analytics"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("managed_agents", sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("managed_agents", sa.Column("price_per_run", sa.Numeric(18, 4), nullable=False, server_default="1"))
    op.add_column("managed_agents", sa.Column("price_per_month", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("category", sa.String(length=64), nullable=True))
    op.add_column("managed_agents", sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("managed_agents", sa.Column("rating", sa.Numeric(5, 2), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("total_revenue", sa.Numeric(18, 4), nullable=False, server_default="0"))
    op.add_column("managed_agents", sa.Column("created_by_user_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_managed_agents_created_by_user_id", "managed_agents", "users", ["created_by_user_id"], ["id"])
    op.create_index("ix_managed_agents_category", "managed_agents", ["category"], unique=False)
    op.create_index("ix_managed_agents_created_by_user_id", "managed_agents", ["created_by_user_id"], unique=False)

    op.execute("UPDATE managed_agents SET created_by_user_id = owner_user_id WHERE created_by_user_id IS NULL")
    op.alter_column("managed_agents", "created_by_user_id", nullable=False)

    op.create_table(
        "agent_store_listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("price_per_run", sa.Numeric(18, 4), nullable=False),
        sa.Column("price_per_month", sa.Numeric(18, 4), nullable=False),
        sa.Column("rating", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_store_listings_agent_id", "agent_store_listings", ["agent_id"], unique=True)
    op.create_index("ix_agent_store_listings_category", "agent_store_listings", ["category"], unique=False)

    op.create_table(
        "installed_agents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("installed_at", sa.DateTime(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("user_id", "agent_id", name="uq_installed_agents_user_agent"),
    )
    op.create_index("ix_installed_agents_user_id", "installed_agents", ["user_id"], unique=False)
    op.create_index("ix_installed_agents_agent_id", "installed_agents", ["agent_id"], unique=False)

    op.create_table(
        "agent_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("managed_agents.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("review", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("agent_id", "user_id", name="uq_agent_reviews_agent_user"),
    )
    op.create_index("ix_agent_reviews_agent_id", "agent_reviews", ["agent_id"], unique=False)
    op.create_index("ix_agent_reviews_user_id", "agent_reviews", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_agent_reviews_user_id", table_name="agent_reviews")
    op.drop_index("ix_agent_reviews_agent_id", table_name="agent_reviews")
    op.drop_table("agent_reviews")

    op.drop_index("ix_installed_agents_agent_id", table_name="installed_agents")
    op.drop_index("ix_installed_agents_user_id", table_name="installed_agents")
    op.drop_table("installed_agents")

    op.drop_index("ix_agent_store_listings_category", table_name="agent_store_listings")
    op.drop_index("ix_agent_store_listings_agent_id", table_name="agent_store_listings")
    op.drop_table("agent_store_listings")

    op.drop_index("ix_managed_agents_created_by_user_id", table_name="managed_agents")
    op.drop_index("ix_managed_agents_category", table_name="managed_agents")
    op.drop_constraint("fk_managed_agents_created_by_user_id", "managed_agents", type_="foreignkey")
    op.drop_column("managed_agents", "created_by_user_id")
    op.drop_column("managed_agents", "total_revenue")
    op.drop_column("managed_agents", "rating")
    op.drop_column("managed_agents", "tags")
    op.drop_column("managed_agents", "category")
    op.drop_column("managed_agents", "price_per_month")
    op.drop_column("managed_agents", "price_per_run")
    op.drop_column("managed_agents", "is_published")
