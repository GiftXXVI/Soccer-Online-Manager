"""Added Transfers Table

Revision ID: 690a29487c41
Revises: 845998a331bd
Create Date: 2022-01-09 05:08:42.074944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '690a29487c41'
down_revision = '845998a331bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('from_team_id', sa.Integer(), nullable=False),
    sa.Column('to_team_id', sa.Integer(), nullable=False),
    sa.Column('transfer_value', sa.Numeric(), nullable=False),
    sa.Column('value_increase', sa.Integer(), nullable=True),
    sa.Column('date_listed', sa.DateTime(), nullable=False),
    sa.Column('date_completed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['from_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.ForeignKeyConstraint(['to_team_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transfer')
    # ### end Alembic commands ###
