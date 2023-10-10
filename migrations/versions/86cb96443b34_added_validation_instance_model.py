"""added validation instance model

Revision ID: 86cb96443b34
Revises: 75196342676f
Create Date: 2023-10-10 20:25:30.350722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86cb96443b34'
down_revision = '75196342676f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('validation_instance', sa.Column('output_status', sa.Integer(), nullable=True))
    op.add_column('validation_instance', sa.Column('mapping_status', sa.Integer(), nullable=True))
    op.add_column('validation_instance', sa.Column('cleanup_status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('validation_instance', 'cleanup_status')
    op.drop_column('validation_instance', 'mapping_status')
    op.drop_column('validation_instance', 'output_status')
    # ### end Alembic commands ###