"""first

Revision ID: d45173a71b32
Revises:
Create Date: 2019-01-28 16:48:40.964023

"""
import logging

from sqlalchemy.engine import reflection

from alembic import op

log = logging.getLogger("alembic.runtime.migration")


# revision identifiers, used by Alembic.
revision = "d45173a71b32"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    log = logging.getLogger("alembic.runtime.migration")
    log.debug("First DB revision alembic script")

    config = op.get_context().config
    insp = reflection.Inspector.from_engine(config.attributes["connection"])
    table_names = insp.get_table_names()
    if "users" in table_names:
        log.info(
            'There is "users" table in the DB - assumes that this DB revision was applied and skip it.'
        )
        return

    # template for app object-independent way of migration
    # oldAccount = sa.Table(
    #     'accounts',
    #     sa.MetaData(),
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('projects_access', sa.VARCHAR(length=4)),
    #     sa.Column('license_info_id', sa.Integer)

    # bind = op.get_bind()
    # session = orm.Session(bind=bind)
    #
    # for old_account in bind.execute(oldAccount.select()):
    #     bind.execute(
    #         oldAccount.update().where(
    #             oldAccount.c.id == old_account.id
    #         ).values(
    #             license_info_id=license_info.id
    #         )
    #     )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("projects_collaborators")
    op.drop_table("projects")
    op.drop_table("users")
    # ### end Alembic commands ###
