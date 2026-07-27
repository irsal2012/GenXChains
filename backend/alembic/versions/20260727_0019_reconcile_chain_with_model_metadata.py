"""reconcile migration chain with model metadata

Closes the drift between what the migration chain builds and what the models
declare. Before this revision a database built by `alembic upgrade head` did
not match one built by `Base.metadata.create_all()`, so dev/test and production
ran on subtly different schemas.

Reconciled here:
- indexes the models declare but no revision ever created
- created_at/updated_at nullability on the inventory policy tables
- simulation_runs.simulation_id, which the model marks unique but the chain
  created as a non-unique index, allowing duplicate simulation ids
- drops ix_agentic_sched_rec_source_rec, made redundant by the column-level
  index on the same single column

Revision ID: 20260727_0019
Revises: 20260727_0018
Create Date: 2026-07-27
"""
from alembic import op
import sqlalchemy as sa


revision = "20260727_0019"
down_revision = "20260727_0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('agentic_schedule_recommendations', schema=None) as batch_op:
        batch_op.drop_index('ix_agentic_sched_rec_source_rec')
        batch_op.create_index(batch_op.f('ix_agentic_schedule_recommendations_period'), ['period'], unique=False)
        batch_op.create_index(batch_op.f('ix_agentic_schedule_recommendations_product_id'), ['product_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_agentic_schedule_recommendations_source_recommendation_id'), ['source_recommendation_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_agentic_schedule_recommendations_supply_plan_id'), ['supply_plan_id'], unique=False)

    with op.batch_alter_table('forecast_jobs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_forecast_jobs_id'), ['id'], unique=False)

    with op.batch_alter_table('inventory_policy_exceptions', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.create_index(batch_op.f('ix_inventory_policy_exceptions_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_inventory_policy_exceptions_inventory_id'), ['inventory_id'], unique=False)

    with op.batch_alter_table('inventory_policy_recommendations', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.create_index(batch_op.f('ix_inventory_policy_recommendations_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_inventory_policy_recommendations_inventory_id'), ['inventory_id'], unique=False)

    with op.batch_alter_table('inventory_policy_runs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_inventory_policy_runs_id'), ['id'], unique=False)

    with op.batch_alter_table('production_schedules', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_production_schedules_period'), ['period'], unique=False)
        batch_op.create_index(batch_op.f('ix_production_schedules_product_id'), ['product_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_production_schedules_supply_plan_id'), ['supply_plan_id'], unique=False)

    with op.batch_alter_table('simulation_runs', schema=None) as batch_op:
        batch_op.drop_index('ix_simulation_runs_simulation_id')
        batch_op.create_index(batch_op.f('ix_simulation_runs_simulation_id'), ['simulation_id'], unique=True)



def downgrade() -> None:
    with op.batch_alter_table('simulation_runs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_simulation_runs_simulation_id'))
        batch_op.create_index('ix_simulation_runs_simulation_id', ['simulation_id'], unique=False)

    with op.batch_alter_table('production_schedules', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_production_schedules_supply_plan_id'))
        batch_op.drop_index(batch_op.f('ix_production_schedules_product_id'))
        batch_op.drop_index(batch_op.f('ix_production_schedules_period'))

    with op.batch_alter_table('inventory_policy_runs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_inventory_policy_runs_id'))

    with op.batch_alter_table('inventory_policy_recommendations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_inventory_policy_recommendations_inventory_id'))
        batch_op.drop_index(batch_op.f('ix_inventory_policy_recommendations_id'))
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('inventory_policy_exceptions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_inventory_policy_exceptions_inventory_id'))
        batch_op.drop_index(batch_op.f('ix_inventory_policy_exceptions_id'))
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('forecast_jobs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_forecast_jobs_id'))

    with op.batch_alter_table('agentic_schedule_recommendations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_agentic_schedule_recommendations_supply_plan_id'))
        batch_op.drop_index(batch_op.f('ix_agentic_schedule_recommendations_source_recommendation_id'))
        batch_op.drop_index(batch_op.f('ix_agentic_schedule_recommendations_product_id'))
        batch_op.drop_index(batch_op.f('ix_agentic_schedule_recommendations_period'))
        batch_op.create_index('ix_agentic_sched_rec_source_rec', ['source_recommendation_id'], unique=False)

