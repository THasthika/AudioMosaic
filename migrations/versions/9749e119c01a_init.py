"""init

Revision ID: 9749e119c01a
Revises: 
Create Date: 2023-06-22 14:08:07.009514

"""
from alembic import op
import sqlalchemy as sa
import app.utils.guid

# revision identifiers, used by Alembic.
revision = '9749e119c01a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasets',
                    sa.Column('id', app.utils.guid.GUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_datasets_id'), 'datasets', ['id'], unique=False)
    op.create_table('audio_samples',
                    sa.Column('id', app.utils.guid.GUID(), nullable=False),
                    sa.Column('path', sa.String(), nullable=True),
                    sa.Column('parent_id', app.utils.guid.GUID(),
                              nullable=True),
                    sa.Column('dataset_id', app.utils.guid.GUID(),
                              nullable=True),
                    sa.Column('processing_status', sa.Enum('QUEUED', 'PROCESSING', 'READY',
                                                           'ERROR', name='audiosampleprocessingstatus'), nullable=True),
                    sa.Column('approval_status', sa.Enum('PENDING', 'ACCEPTED',
                                                         'REJECTED', name='audiosampleapprovalstatus'), nullable=True),
                    sa.Column('sample_rate', sa.Integer(), nullable=True),
                    sa.Column('bit_rate', sa.Integer(), nullable=True),
                    sa.Column('duration', sa.Float(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
                    sa.ForeignKeyConstraint(
                        ['parent_id'], ['audio_samples.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_audio_samples_id'),
                    'audio_samples', ['id'], unique=False)
    op.create_table('labels',
                    sa.Column('id', app.utils.guid.GUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('dataset_id', app.utils.guid.GUID(),
                              nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('dataset_id', 'name')
                    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=False)
    op.create_table('audio_sample_labels',
                    sa.Column('id', app.utils.guid.GUID(), nullable=False),
                    sa.Column('label_id', app.utils.guid.GUID(),
                              nullable=True),
                    sa.Column('audio_sample_id',
                              app.utils.guid.GUID(), nullable=True),
                    sa.Column('is_sample_level', sa.Boolean(), nullable=True),
                    sa.Column('start_time', sa.Float(precision=10,
                                                     decimal_return_scale=2), nullable=True),
                    sa.Column('end_time', sa.Float(precision=10,
                                                   decimal_return_scale=2), nullable=True),
                    sa.ForeignKeyConstraint(['audio_sample_id'], [
                                            'audio_samples.id'], ),
                    sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audio_sample_labels')
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
    op.drop_index(op.f('ix_audio_samples_id'), table_name='audio_samples')
    op.drop_table('audio_samples')
    op.drop_index(op.f('ix_datasets_id'), table_name='datasets')
    op.drop_table('datasets')
    # ### end Alembic commands ###