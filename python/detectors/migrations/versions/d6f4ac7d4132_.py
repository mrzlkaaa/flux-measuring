"""empty message

Revision ID: d6f4ac7d4132
Revises: 
Create Date: 2021-11-16 10:47:46.179286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6f4ac7d4132'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('experiment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('irradiation_finished', sa.DateTime(), nullable=True),
    sa.Column('irradiation_time', sa.Float(), nullable=True),
    sa.Column('power', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sample',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.Column('cooling_finished', sa.DateTime(), nullable=True),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('cooling_time', sa.Float(), nullable=True),
    sa.Column('measuring_time', sa.Float(), nullable=True),
    sa.Column('mass', sa.Float(), nullable=True),
    sa.Column('activity', sa.Float(), nullable=True),
    sa.Column('exp_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exp_id'], ['experiment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sample')
    op.drop_table('experiment')
    # ### end Alembic commands ###
