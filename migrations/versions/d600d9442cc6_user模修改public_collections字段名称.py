"""User模修改public_collections字段名称

Revision ID: d600d9442cc6
Revises: 4f8b4aeb9460
Create Date: 2021-12-07 16:18:26.233333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd600d9442cc6'
down_revision = '4f8b4aeb9460'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('public_collections', sa.Boolean(), nullable=True))
    op.drop_column('user', 'show_collections')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('show_collections', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('user', 'public_collections')
    # ### end Alembic commands ###
