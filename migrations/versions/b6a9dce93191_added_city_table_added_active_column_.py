"""Added City Table, Added Active Column for Account

Revision ID: b6a9dce93191
Revises: 80bdc90879e6
Create Date: 2022-01-08 09:35:08.628336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6a9dce93191'
down_revision = '80bdc90879e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'country_id', name='UX_name_country')
    )
    op.add_column('account', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('team', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'name')
    op.drop_column('account', 'active')
    op.drop_table('city')
    # ### end Alembic commands ###