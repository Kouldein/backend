"""empty message

Revision ID: 596a0e1031cf
Revises: bd7bae95281e
Create Date: 2021-12-07 01:05:53.004404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '596a0e1031cf'
down_revision = 'bd7bae95281e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('system',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('eventId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eventId'], ['events.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('userId', 'eventId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('system')
    # ### end Alembic commands ###