"""ai agent network

Revision ID: 0012_ai_agent_network
Revises: 0011_platform_control_center
Create Date: 2026-03-06 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0012_ai_agent_network"
down_revision = "0011_platform_control_center"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_capabilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("capability_name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["managed_agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_capabilities_agent_id", "agent_capabilities", ["agent_id"], unique=False)
    op.create_index("ix_agent_capabilities_capability_name", "agent_capabilities", ["capability_name"], unique=False)

    op.create_table(
        "agent_workflows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "workflow_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_prompt", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["managed_agents.id"]),
        sa.ForeignKeyConstraint(["workflow_id"], ["agent_workflows.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_steps_agent_id", "workflow_steps", ["agent_id"], unique=False)
    op.create_index("ix_workflow_steps_workflow_id", "workflow_steps", ["workflow_id"], unique=False)

    op.create_table(
        "agent_reputation",
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("tasks_completed", sa.Integer(), nullable=False),
        sa.Column("success_rate", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["managed_agents.id"]),
        sa.PrimaryKeyConstraint("agent_id"),
    )

    op.create_table(
        "agent_schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cron_expression", sa.String(length=120), nullable=False),
        sa.Column("task_prompt", sa.Text(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["managed_agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_schedules_agent_id", "agent_schedules", ["agent_id"], unique=False)

    op.add_column("agent_tasks", sa.Column("requester_agent_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("agent_tasks", sa.Column("worker_agent_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("agent_tasks", sa.Column("task_description", sa.Text(), nullable=True))
    op.add_column("agent_tasks", sa.Column("payment_amount", sa.Numeric(precision=18, scale=4), nullable=False, server_default="0"))
    op.add_column("agent_tasks", sa.Column("completed_at", sa.DateTime(), nullable=True))

    op.create_index("ix_agent_tasks_requester_agent_id", "agent_tasks", ["requester_agent_id"], unique=False)
    op.create_index("ix_agent_tasks_worker_agent_id", "agent_tasks", ["worker_agent_id"], unique=False)
    op.create_foreign_key("fk_agent_tasks_requester_agent_id", "agent_tasks", "managed_agents", ["requester_agent_id"], ["id"])
    op.create_foreign_key("fk_agent_tasks_worker_agent_id", "agent_tasks", "managed_agents", ["worker_agent_id"], ["id"])

    op.execute("UPDATE agent_tasks SET worker_agent_id = agent_id, task_description = COALESCE(payload->>'input', ''), payment_amount = 0")


def downgrade() -> None:
    op.drop_constraint("fk_agent_tasks_worker_agent_id", "agent_tasks", type_="foreignkey")
    op.drop_constraint("fk_agent_tasks_requester_agent_id", "agent_tasks", type_="foreignkey")
    op.drop_index("ix_agent_tasks_worker_agent_id", table_name="agent_tasks")
    op.drop_index("ix_agent_tasks_requester_agent_id", table_name="agent_tasks")
    op.drop_column("agent_tasks", "completed_at")
    op.drop_column("agent_tasks", "payment_amount")
    op.drop_column("agent_tasks", "task_description")
    op.drop_column("agent_tasks", "worker_agent_id")
    op.drop_column("agent_tasks", "requester_agent_id")

    op.drop_index("ix_agent_schedules_agent_id", table_name="agent_schedules")
    op.drop_table("agent_schedules")

    op.drop_table("agent_reputation")

    op.drop_index("ix_workflow_steps_workflow_id", table_name="workflow_steps")
    op.drop_index("ix_workflow_steps_agent_id", table_name="workflow_steps")
    op.drop_table("workflow_steps")

    op.drop_table("agent_workflows")

    op.drop_index("ix_agent_capabilities_capability_name", table_name="agent_capabilities")
    op.drop_index("ix_agent_capabilities_agent_id", table_name="agent_capabilities")
    op.drop_table("agent_capabilities")
