"""added cd_ratio, th_flux columns of TEXT type

Revision ID: ba5ca6764ff7
Revises: 1170444df7ff
Create Date: 2021-12-03 18:44:29.606928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba5ca6764ff7'
down_revision = '1170444df7ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foil_experiments', sa.Column('cd_ratio', sa.Text(), nullable=True))
    op.add_column('foil_experiments', sa.Column('th_flux', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('foil_experiments', 'th_flux')
    op.drop_column('foil_experiments', 'cd_ratio')
    # ### end Alembic commands ###