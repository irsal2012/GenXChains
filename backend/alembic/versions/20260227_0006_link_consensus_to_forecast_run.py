"""link forecast consensus rows to forecast run audits

Revision ID: 20260227_0006
Revises: 20260227_0005
Create Date: 2026-02-27 22:10:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260227_0006"
down_revision = "20260227_0005"
branch_labels = None
depends_on = None


# Foreign keys and unique constraints cannot be ALTERed in place on SQLite, so
# every constraint change here goes through batch mode (copy-and-move). Batch
# mode is portable — on PostgreSQL it emits plain ALTER statements.
def upgrade() -> None:
    with op.batch_alter_table("forecast_consensus") as batch_op:
        batch_op.add_column(
            sa.Column("forecast_run_audit_id", sa.Integer(), nullable=True),
        )
        batch_op.create_foreign_key(
            "fk_forecast_consensus_run_audit",
            "forecast_run_audits",
            ["forecast_run_audit_id"],
            ["id"],
            ondelete="CASCADE",
        )
        batch_op.drop_constraint(
            "uq_forecast_consensus_product_period_version",
            type_="unique",
        )
        batch_op.create_unique_constraint(
            "uq_forecast_consensus_run_period_version",
            ["forecast_run_audit_id", "period", "version"],
        )

    op.create_index(
        "ix_forecast_consensus_forecast_run_audit_id",
        "forecast_consensus",
        ["forecast_run_audit_id"],
        unique=False,
    )
    op.create_index(
        "ix_forecast_consensus_run_period",
        "forecast_consensus",
        ["forecast_run_audit_id", "period"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_forecast_consensus_run_period", table_name="forecast_consensus")
    op.drop_index("ix_forecast_consensus_forecast_run_audit_id", table_name="forecast_consensus")

    with op.batch_alter_table("forecast_consensus") as batch_op:
        batch_op.drop_constraint(
            "uq_forecast_consensus_run_period_version",
            type_="unique",
        )
        batch_op.create_unique_constraint(
            "uq_forecast_consensus_product_period_version",
            ["product_id", "period", "version"],
        )
        batch_op.drop_constraint(
            "fk_forecast_consensus_run_audit",
            type_="foreignkey",
        )
        batch_op.drop_column("forecast_run_audit_id")
