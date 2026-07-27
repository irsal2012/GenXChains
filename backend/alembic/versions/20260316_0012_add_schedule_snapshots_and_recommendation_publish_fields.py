"""add schedule snapshots and recommendation publish/modify fields

Revision ID: 20260316_0012
Revises: 20260316_0011
Create Date: 2026-03-16 20:12:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260316_0012"
down_revision = "20260316_0011"
branch_labels = None
depends_on = None


# SQLite cannot ALTER constraints in place, so the column/constraint changes to
# agentic_schedule_recommendations run in batch mode (copy-and-move). Batch mode
# is portable: on PostgreSQL it emits ordinary ALTER statements.
def upgrade() -> None:
    with op.batch_alter_table("agentic_schedule_recommendations") as batch_op:
        batch_op.add_column(sa.Column("published_by", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("published_at", sa.DateTime(), nullable=True))
        batch_op.add_column(
            sa.Column("source_recommendation_id", sa.String(length=64), nullable=True)
        )
        batch_op.add_column(
            sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1")
        )

        batch_op.create_foreign_key(
            "fk_agentic_sched_rec_published_by",
            "users",
            ["published_by"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "fk_agentic_sched_rec_source_recommendation",
            "agentic_schedule_recommendations",
            ["source_recommendation_id"],
            ["recommendation_id"],
        )

        batch_op.drop_constraint("ck_agentic_sched_rec_state", type_="check")
        batch_op.create_check_constraint(
            "ck_agentic_sched_rec_state_v2",
            "state IN ('RECEIVED', 'CLASSIFIED', 'PLANNED', 'VALIDATED', 'OPTIMIZED', 'SIMULATED', "
            "'PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'PUBLISHED', 'FAILED')",
        )
        batch_op.alter_column("state", server_default="SIMULATED")

        batch_op.drop_constraint("ck_agentic_sched_rec_status", type_="check")
        batch_op.create_check_constraint(
            "ck_agentic_sched_rec_status_v2",
            "status IN ('pending_approval', 'approved', 'rejected', 'published')",
        )

    op.create_index(
        "ix_agentic_sched_rec_source_rec",
        "agentic_schedule_recommendations",
        ["source_recommendation_id"],
        unique=False,
    )
    op.create_index(
        "ix_agentic_sched_rec_revision",
        "agentic_schedule_recommendations",
        ["recommendation_id", "revision_number"],
        unique=False,
    )

    op.create_table(
        "production_schedule_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("supply_plan_id", sa.Integer(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("recommendation_id", sa.String(length=64), nullable=True),
        sa.Column("snapshot_json", sa.Text(), nullable=False),
        sa.Column("published_by", sa.Integer(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["published_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["supply_plan_id"], ["supply_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("supply_plan_id", "version_number", name="uq_schedule_snapshot_supply_plan_version"),
    )
    op.create_index("ix_production_schedule_snapshots_id", "production_schedule_snapshots", ["id"], unique=False)
    op.create_index(
        "ix_schedule_snapshot_supply_plan",
        "production_schedule_snapshots",
        ["supply_plan_id"],
        unique=False,
    )
    op.create_index(
        "ix_schedule_snapshot_recommendation",
        "production_schedule_snapshots",
        ["recommendation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_schedule_snapshot_recommendation", table_name="production_schedule_snapshots")
    op.drop_index("ix_schedule_snapshot_supply_plan", table_name="production_schedule_snapshots")
    op.drop_index("ix_production_schedule_snapshots_id", table_name="production_schedule_snapshots")
    op.drop_table("production_schedule_snapshots")

    op.drop_index("ix_agentic_sched_rec_revision", table_name="agentic_schedule_recommendations")
    op.drop_index("ix_agentic_sched_rec_source_rec", table_name="agentic_schedule_recommendations")

    with op.batch_alter_table("agentic_schedule_recommendations") as batch_op:
        batch_op.drop_constraint("ck_agentic_sched_rec_status_v2", type_="check")
        batch_op.create_check_constraint(
            "ck_agentic_sched_rec_status",
            "status IN ('pending_approval', 'approved', 'rejected')",
        )

        batch_op.alter_column("state", server_default="PENDING_APPROVAL")
        batch_op.drop_constraint("ck_agentic_sched_rec_state_v2", type_="check")
        batch_op.create_check_constraint(
            "ck_agentic_sched_rec_state",
            "state IN ('RECEIVED', 'CLASSIFIED', 'PENDING_APPROVAL', 'APPROVED', 'REJECTED')",
        )

        batch_op.drop_constraint("fk_agentic_sched_rec_source_recommendation", type_="foreignkey")
        batch_op.drop_constraint("fk_agentic_sched_rec_published_by", type_="foreignkey")

        batch_op.drop_column("revision_number")
        batch_op.drop_column("source_recommendation_id")
        batch_op.drop_column("published_at")
    op.drop_column("agentic_schedule_recommendations", "published_by")
