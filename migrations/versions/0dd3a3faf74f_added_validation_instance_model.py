"""added validation instance model

Revision ID: 0dd3a3faf74f
Revises: 928f37155aab
Create Date: 2023-10-09 14:13:22.655679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dd3a3faf74f'
down_revision = '928f37155aab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('validation_instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_At', sa.BigInteger(), nullable=True),
    sa.Column('picked_at', sa.BigInteger(), nullable=True),
    sa.Column('transformed_start_time', sa.BigInteger(), nullable=True),
    sa.Column('transform_end_time', sa.BigInteger(), nullable=True),
    sa.Column('map_start_time', sa.BigInteger(), nullable=True),
    sa.Column('map_end_time', sa.BigInteger(), nullable=True),
    sa.Column('csv_read_time', sa.BigInteger(), nullable=True),
    sa.Column('csv_size', sa.Integer(), nullable=True),
    sa.Column('csv_row_len', sa.Integer(), nullable=True),
    sa.Column('upload_start', sa.BigInteger(), nullable=True),
    sa.Column('upload_end', sa.BigInteger(), nullable=True),
    sa.Column('pull_start', sa.BigInteger(), nullable=True),
    sa.Column('pull_end', sa.BigInteger(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('validation_status', sa.Integer(), nullable=True),
    sa.Column('transform_status', sa.Integer(), nullable=True),
    sa.Column('map_status', sa.Integer(), nullable=True),
    sa.Column('end_time', sa.BigInteger(), nullable=True),
    sa.Column('upload_id', sa.Integer(), nullable=True),
    sa.Column('schema_id', sa.Integer(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('schema', sa.JSON(), nullable=True),
    sa.Column('progress_percentage', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['schema_id'], ['schema_data.id'], ),
    sa.ForeignKeyConstraint(['upload_id'], ['uploads.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('validation_instance')
    # ### end Alembic commands ###