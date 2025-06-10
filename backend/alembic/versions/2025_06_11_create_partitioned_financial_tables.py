'''Create partitioned financial tables

Revision ID: 2025_06_11_partition_financial
Revises: 2025_06_11_enhance_financial_models
Create Date: 2025-06-11 00:00:00.000000
'''
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

# Revision identifiers, used by Alembic.
revision = '2025_06_11_partition_financial'
down_revision = '2025_06_11_enhance_financial_models'
branch_labels = None
depends_on = None

def upgrade():
    # Create parent table for financial transactions with partitioning
    op.execute("""
        CREATE TABLE IF NOT EXISTS financial_transaction_parent (
            id SERIAL PRIMARY KEY,
            project_id INTEGER NOT NULL,
            amount NUMERIC(12, 2) NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            category VARCHAR(100),
            vendor VARCHAR(100),
            payment_method VARCHAR(50),
            cost_center VARCHAR(50),
            CONSTRAINT fk_project
                FOREIGN KEY (project_id) 
                REFERENCES financial_project(id)
                ON DELETE CASCADE
        ) PARTITION BY RANGE (created_at);
    """)

    # Create index on partition column
    op.create_index('idx_financial_transaction_parent_created_at', 'financial_transaction_parent', ['created_at'], unique=False)

    # Create partitions for past 12 months and next 12 months
    from datetime import datetime, timedelta
    current_date = datetime.now()
    start_date = current_date - timedelta(days=365)  # 12 months back

    for i in range(24):  # 24 months total (12 past, 12 future)
        month_date = start_date + timedelta(days=30 * i)
        start_str = month_date.strftime('%Y-%m-01')
        end_month = month_date + timedelta(days=30)
        end_str = end_month.strftime('%Y-%m-01')
        partition_name = f'financial_transaction_{month_date.strftime("%Y_%m")}'
        
        op.execute(f"""
            CREATE TABLE IF NOT EXISTS {partition_name} 
            PARTITION OF financial_transaction_parent 
            FOR VALUES FROM ('{start_str}') TO ('{end_str}');
        """)
        
        # Create additional indexes on partition for common queries
        op.create_index(f'idx_{partition_name}_created_at', partition_name, ['created_at'], unique=False)
        op.create_index(f'idx_{partition_name}_project_id', partition_name, ['project_id'], unique=False)

    # If old financial_transaction table exists, move data to new structure
    # First, check if table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'financial_transaction' in inspector.get_table_names():
        # Move data to parent table (which will route to appropriate partitions)
        op.execute("""
            INSERT INTO financial_transaction_parent
            SELECT * FROM financial_transaction;
        """)
        
        # Drop old table
        op.drop_table('financial_transaction')


def downgrade():
    # Create a non-partitioned table to hold all data
    op.create_table(
        'financial_transaction',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('transaction_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('category', sa.String(100)),
        sa.Column('vendor', sa.String(100)),
        sa.Column('payment_method', sa.String(50)),
        sa.Column('cost_center', sa.String(50)),
        sa.ForeignKeyConstraint(['project_id'], ['financial_project.id'], ondelete='CASCADE')
    )

    # Move data back from partitions to single table if parent table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'financial_transaction_parent' in inspector.get_table_names():
        op.execute("""
            INSERT INTO financial_transaction
            SELECT * FROM financial_transaction_parent;
        """)

        # Drop all partitions and parent table
        from datetime import datetime, timedelta
        current_date = datetime.now()
        start_date = current_date - timedelta(days=365)  # 12 months back

        for i in range(24):  # 24 months total
            month_date = start_date + timedelta(days=30 * i)
            partition_name = f'financial_transaction_{month_date.strftime("%Y_%m")}'
            op.execute(f"DROP TABLE IF EXISTS {partition_name} CASCADE")

        op.drop_table('financial_transaction_parent')
