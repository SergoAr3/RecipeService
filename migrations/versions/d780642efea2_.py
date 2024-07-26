"""

Revision ID: d780642efea2
Revises: a58749a0f48d
Create Date: 2024-07-21 00:28:57.855089

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd780642efea2'
down_revision = 'a58749a0f48d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('image_step_step_id_fkey', 'image_step', type_='foreignkey')
    op.create_foreign_key(None, 'image_step', 'step', ['step_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image_step', type_='foreignkey')
    op.create_foreign_key('image_step_step_id_fkey', 'image_step', 'step', ['step_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
