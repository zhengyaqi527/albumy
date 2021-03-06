"""增加通知

Revision ID: 6507a07254c2
Revises: aaef6453ab3c
Create Date: 2021-12-03 20:01:37.384122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6507a07254c2'
down_revision = 'aaef6453ab3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_table('notification')
    # ### end Alembic commands ###
