"""empty message

Revision ID: 2a50347e3993
Revises: 73c1c2f3fe83
Create Date: 2022-07-27 17:03:58.382527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a50347e3993'
down_revision = '73c1c2f3fe83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('project_owner_id_fkey', 'project', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('project_owner_id_fkey', 'project', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###