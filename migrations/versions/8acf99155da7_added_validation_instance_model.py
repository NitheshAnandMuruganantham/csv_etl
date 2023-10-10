"""added validation instance model

Revision ID: 8acf99155da7
Revises: 66386b7103a4
Create Date: 2023-10-10 20:02:12.991662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8acf99155da7'
down_revision = '66386b7103a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('validation_instance', sa.Column('created_at', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('validation_instance', 'created_at')
    # ### end Alembic commands ###