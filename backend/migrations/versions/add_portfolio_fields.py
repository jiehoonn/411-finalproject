from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add balance column to user table
    op.add_column('user', sa.Column('balance', sa.Float(), nullable=False, server_default='10000.0'))
    
    # Create stocks table
    op.create_table(
        'stock',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('symbol', sa.String(10), nullable=False),
        sa.Column('shares', sa.Float(), nullable=False),
        sa.Column('purchase_price', sa.Float(), nullable=False)
    )
    
    # Create index for faster lookups
    op.create_index('idx_user_stocks', 'stock', ['user_id', 'symbol'])

def downgrade():
    op.drop_index('idx_user_stocks')
    op.drop_table('stock')
    op.drop_column('user', 'balance')
