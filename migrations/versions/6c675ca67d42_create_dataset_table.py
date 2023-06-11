"""Create Dataset Table

Revision ID: 6c675ca67d42
Revises: 
Create Date: 2023-06-10 17:01:04.529571

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '6c675ca67d42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataset',
                    sa.Column(
                        'name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dataset')
    # ### end Alembic commands ###