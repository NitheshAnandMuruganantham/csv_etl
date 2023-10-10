"""added validation instance model

Revision ID: a585fc79f307
Revises: 86cb96443b34
Create Date: 2023-10-10 20:30:44.307597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a585fc79f307'
down_revision = '86cb96443b34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('validation_instance', sa.Column('transformation_end_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('cleanup_start_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('read_csv_start_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('mapping_end_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('read_csv_end_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('mapping_start_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('file_pull_end_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('transformation_start_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('cleanup_end_time', sa.BigInteger(), nullable=True))
    op.add_column('validation_instance', sa.Column('file_pull_start_time', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('validation_instance', 'file_pull_start_time')
    op.drop_column('validation_instance', 'cleanup_end_time')
    op.drop_column('validation_instance', 'transformation_start_time')
    op.drop_column('validation_instance', 'file_pull_end_time')
    op.drop_column('validation_instance', 'mapping_start_time')
    op.drop_column('validation_instance', 'read_csv_end_time')
    op.drop_column('validation_instance', 'mapping_end_time')
    op.drop_column('validation_instance', 'read_csv_start_time')
    op.drop_column('validation_instance', 'cleanup_start_time')
    op.drop_column('validation_instance', 'transformation_end_time')
    # ### end Alembic commands ###