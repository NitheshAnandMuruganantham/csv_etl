"""empty message

Revision ID: 253e6cdeaa39
Revises: 29922f54adab
Create Date: 2023-08-25 19:01:41.113252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '253e6cdeaa39'
down_revision = '29922f54adab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('output_data',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('file_id', sa.BigInteger(), nullable=False),
    sa.Column('data_id', sa.BigInteger(), nullable=False),
    sa.Column('schema_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('pid', sa.String(), nullable=True),
    sa.Column('org_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['data_id'], ['uploads.id'], ),
    sa.ForeignKeyConstraint(['file_id'], ['uploads.id'], ),
    sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['schema_id'], ['schema_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('output_data')
    # ### end Alembic commands ###