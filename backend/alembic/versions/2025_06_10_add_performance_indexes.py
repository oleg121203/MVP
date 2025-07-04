"""Add performance indexes for CRMLead and PriceData

Revision ID: 2025_06_10_perf_indexes
Revises: 2025_06_10
Create Date: 2025-06-10 17:30:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2025_06_10_perf_indexes'
down_revision = '2025_06_10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_crmlead_status_created', 'crm_leads', ['status', 'created_at'], unique=False)
    op.create_index('idx_crmlead_email_status', 'crm_leads', ['email', 'status'], unique=False)
    op.create_index('idx_pricedata_product_timestamp', 'price_data', ['product_id', 'timestamp'], unique=False)
    op.create_index('idx_pricedata_source_timestamp', 'price_data', ['source', 'timestamp'], unique=False)
    op.create_index('idx_pricedata_price_range', 'price_data', ['price'], unique=False)
    op.alter_column('crm_leads', 'status', existing_type=sa.String(), nullable=False, existing_server_default='New')
    op.alter_column('crm_leads', 'created_at', existing_type=sa.DateTime(), nullable=False, existing_server_default=sa.func.now())
    op.alter_column('price_data', 'price', existing_type=sa.Float(), nullable=False)
    op.alter_column('price_data', 'timestamp', existing_type=sa.DateTime(), nullable=False)
    op.alter_column('price_data', 'source', existing_type=sa.String(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_crmlead_status_created', table_name='crm_leads')
    op.drop_index('idx_crmlead_email_status', table_name='crm_leads')
    op.drop_index('idx_pricedata_product_timestamp', table_name='price_data')
    op.drop_index('idx_pricedata_source_timestamp', table_name='price_data')
    op.drop_index('idx_pricedata_price_range', table_name='price_data')
    op.alter_column('crm_leads', 'status', existing_type=sa.String(), nullable=True, existing_server_default='New')
    op.alter_column('crm_leads', 'created_at', existing_type=sa.DateTime(), nullable=True, existing_server_default=sa.func.now())
    op.alter_column('price_data', 'price', existing_type=sa.Float(), nullable=True)
    op.alter_column('price_data', 'timestamp', existing_type=sa.DateTime(), nullable=True)
    op.alter_column('price_data', 'source', existing_type=sa.String(), nullable=True)
    # ### end Alembic commands ###
