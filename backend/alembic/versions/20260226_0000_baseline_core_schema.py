"""baseline core schema

Creates the core S&OP tables that every later revision assumes already exist.

Historically this project bootstrapped the core schema with
``Base.metadata.create_all()`` and started the Alembic chain at the
forecast_jobs table, so ``alembic upgrade head`` could never build a database
from empty — revision 20260227_0002 immediately tried to ALTER tables nothing
had created. That blocked production entirely, because config.py refuses to
start with AUTO_CREATE_TABLES enabled outside development.

This revision is the missing root. It deliberately reproduces the
*pre-hardening* shape of these tables: the unique/check constraints and
composite indexes added by 20260227_0002 are intentionally absent here so that
revision still performs the hardening it documents.

Revision ID: 20260226_0000
Revises:
Create Date: 2026-07-27
"""
from alembic import op
import sqlalchemy as sa

revision = "20260226_0000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('kpi_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('metric_name', sa.String(length=100), nullable=False),
    sa.Column('metric_category', sa.String(length=50), nullable=False),
    sa.Column('period', sa.Date(), nullable=False),
    sa.Column('value', sa.Numeric(precision=12, scale=4), nullable=False),
    sa.Column('target', sa.Numeric(precision=12, scale=4), nullable=True),
    sa.Column('previous_value', sa.Numeric(precision=12, scale=4), nullable=True),
    sa.Column('variance', sa.Numeric(precision=12, scale=4), nullable=True),
    sa.Column('variance_pct', sa.Numeric(precision=8, scale=4), nullable=True),
    sa.Column('trend', sa.String(length=20), nullable=True),
    sa.Column('unit', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_kpi_metrics_id'), 'kpi_metrics', ['id'], unique=False)
    op.create_index(op.f('ix_kpi_metrics_metric_name'), 'kpi_metrics', ['metric_name'], unique=False)
    op.create_index(op.f('ix_kpi_metrics_period'), 'kpi_metrics', ['period'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('department', sa.String(length=100), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('audit_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=50), nullable=False),
    sa.Column('entity_type', sa.String(length=50), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('old_values', sa.Text(), nullable=True),
    sa.Column('new_values', sa.Text(), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_entity_id'), 'audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_type'), 'audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_type', sa.String(length=50), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('mentions', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_entity_id'), 'comments', ['entity_id'], unique=False)
    op.create_index(op.f('ix_comments_entity_type'), 'comments', ['entity_type'], unique=False)
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('product_family', sa.String(length=100), nullable=True),
    sa.Column('unit_of_measure', sa.String(length=20), nullable=True),
    sa.Column('unit_cost', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('selling_price', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('lead_time_days', sa.Integer(), nullable=True),
    sa.Column('min_order_qty', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_sku'), 'products', ['sku'], unique=True)
    op.create_table('scenarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('scenario_type', sa.String(length=50), nullable=True),
    sa.Column('parameters', sa.Text(), nullable=False),
    sa.Column('base_demand_version', sa.Integer(), nullable=True),
    sa.Column('base_supply_version', sa.Integer(), nullable=True),
    sa.Column('results', sa.Text(), nullable=True),
    sa.Column('revenue_impact', sa.Numeric(precision=14, scale=2), nullable=True),
    sa.Column('margin_impact', sa.Numeric(precision=14, scale=2), nullable=True),
    sa.Column('inventory_impact', sa.Numeric(precision=14, scale=2), nullable=True),
    sa.Column('service_level_impact', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('approved_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenarios_id'), 'scenarios', ['id'], unique=False)
    op.create_table('sop_cycles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cycle_name', sa.String(length=255), nullable=False),
    sa.Column('period', sa.Date(), nullable=False),
    sa.Column('current_step', sa.Integer(), nullable=True),
    sa.Column('step_1_status', sa.String(length=20), nullable=True),
    sa.Column('step_1_due_date', sa.Date(), nullable=True),
    sa.Column('step_1_owner_id', sa.Integer(), nullable=True),
    sa.Column('step_2_status', sa.String(length=20), nullable=True),
    sa.Column('step_2_due_date', sa.Date(), nullable=True),
    sa.Column('step_2_owner_id', sa.Integer(), nullable=True),
    sa.Column('step_3_status', sa.String(length=20), nullable=True),
    sa.Column('step_3_due_date', sa.Date(), nullable=True),
    sa.Column('step_3_owner_id', sa.Integer(), nullable=True),
    sa.Column('step_4_status', sa.String(length=20), nullable=True),
    sa.Column('step_4_due_date', sa.Date(), nullable=True),
    sa.Column('step_4_owner_id', sa.Integer(), nullable=True),
    sa.Column('step_5_status', sa.String(length=20), nullable=True),
    sa.Column('step_5_due_date', sa.Date(), nullable=True),
    sa.Column('step_5_owner_id', sa.Integer(), nullable=True),
    sa.Column('decisions', sa.Text(), nullable=True),
    sa.Column('action_items', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('overall_status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['step_1_owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['step_2_owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['step_3_owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['step_4_owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['step_5_owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sop_cycles_id'), 'sop_cycles', ['id'], unique=False)
    op.create_table('demand_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('period', sa.Date(), nullable=False),
    sa.Column('region', sa.String(length=100), nullable=True),
    sa.Column('channel', sa.String(length=100), nullable=True),
    sa.Column('forecast_qty', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('adjusted_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('actual_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('consensus_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('confidence', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('approved_by', sa.Integer(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('version >= 1', name='ck_demand_plans_version_min_1'),
    sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demand_plans_id'), 'demand_plans', ['id'], unique=False)
    op.create_index(op.f('ix_demand_plans_period'), 'demand_plans', ['period'], unique=False)
    op.create_index(op.f('ix_demand_plans_product_id'), 'demand_plans', ['product_id'], unique=False)
    op.create_table('forecasts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('model_type', sa.String(length=50), nullable=False),
    sa.Column('period', sa.Date(), nullable=False),
    sa.Column('predicted_qty', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('lower_bound', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('upper_bound', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('confidence', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('mape', sa.Numeric(precision=8, scale=4), nullable=True),
    sa.Column('rmse', sa.Numeric(precision=12, scale=4), nullable=True),
    sa.Column('features_used', sa.Text(), nullable=True),
    sa.Column('model_version', sa.String(length=50), nullable=True),
    sa.Column('training_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forecasts_id'), 'forecasts', ['id'], unique=False)
    op.create_index(op.f('ix_forecasts_period'), 'forecasts', ['period'], unique=False)
    op.create_index(op.f('ix_forecasts_product_id'), 'forecasts', ['product_id'], unique=False)
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('on_hand_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('allocated_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('in_transit_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('safety_stock', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('reorder_point', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('max_stock', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('days_of_supply', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('last_receipt_date', sa.Date(), nullable=True),
    sa.Column('last_issue_date', sa.Date(), nullable=True),
    sa.Column('valuation', sa.Numeric(precision=14, scale=2), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_id'), 'inventory', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_product_id'), 'inventory', ['product_id'], unique=False)
    op.create_table('supply_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('period', sa.Date(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('planned_prod_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('actual_prod_qty', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('capacity_max', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('capacity_used', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('supplier_name', sa.String(length=255), nullable=True),
    sa.Column('lead_time_days', sa.Integer(), nullable=True),
    sa.Column('cost_per_unit', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('constraints', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('version >= 1', name='ck_supply_plans_version_min_1'),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supply_plans_id'), 'supply_plans', ['id'], unique=False)
    op.create_index(op.f('ix_supply_plans_period'), 'supply_plans', ['period'], unique=False)
    op.create_index(op.f('ix_supply_plans_product_id'), 'supply_plans', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_table("supply_plans")
    op.drop_table("inventory")
    op.drop_table("forecasts")
    op.drop_table("demand_plans")
    op.drop_table("sop_cycles")
    op.drop_table("scenarios")
    op.drop_table("products")
    op.drop_table("comments")
    op.drop_table("audit_logs")
    op.drop_table("users")
    op.drop_table("kpi_metrics")
    op.drop_table("categories")
