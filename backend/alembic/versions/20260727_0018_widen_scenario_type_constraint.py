"""Widen ck_scenarios_type to cover best_case / worst_case.

The SPA offers five scenario types (`ScenarioType` in frontend/src/types),
but the check constraint only permitted three — selecting "Best case" or
"Worst case" failed at the database with an IntegrityError.

Revision ID: 20260727_0018
Revises: 20260317_0017
"""
from alembic import op

revision = "20260727_0018"
down_revision = "20260317_0017"
branch_labels = None
depends_on = None

NEW_TYPES = "('what_if', 'baseline', 'stress_test', 'best_case', 'worst_case')"
OLD_TYPES = "('what_if', 'baseline', 'stress_test')"


def upgrade() -> None:
    with op.batch_alter_table("scenarios") as batch_op:
        batch_op.drop_constraint("ck_scenarios_type", type_="check")
        batch_op.create_check_constraint(
            "ck_scenarios_type",
            f"scenario_type IN {NEW_TYPES}",
        )


def downgrade() -> None:
    # Rows using the widened values would violate the narrower constraint.
    op.execute(
        "UPDATE scenarios SET scenario_type = 'what_if' "
        "WHERE scenario_type IN ('best_case', 'worst_case')"
    )
    with op.batch_alter_table("scenarios") as batch_op:
        batch_op.drop_constraint("ck_scenarios_type", type_="check")
        batch_op.create_check_constraint(
            "ck_scenarios_type",
            f"scenario_type IN {OLD_TYPES}",
        )
