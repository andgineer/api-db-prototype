"""first

Revision ID: d45173a71b32
Revises: 
Create Date: 2019-01-28 16:48:40.964023

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection
import logging


# revision identifiers, used by Alembic.
revision = 'd45173a71b32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    log = logging.getLogger('alembic.runtime.migration')
    log.debug('First DB revision alembic script')

    config = op.get_context().config
    insp = reflection.Inspector.from_engine(config.attributes['connection'])
    table_names = insp.get_table_names()
    if 'users' in table_names:
        log.info('There is "users" table in the DB - assumes that this DB revision was applied and skip it.')
        return

    op.create_table('users',
    sa.Column('created_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('projects_collaborators',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('project_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects_collaborators')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
