from sqlalchemy import Column, ForeignKeyConstraint, MetaData, Table, types

metadata = MetaData()

# Migrations are not currently available for rapidpro tables.
# If you modify these tables, make sure to migrate the databases
# manually or to add a command to do it.

contact = Table('auth_user', metadata,
                Column('id', types.Integer, primary_key=True),
                Column('uuid', types.String(64)),
                Column('name', types.String(128)),
                Column('groups', types.JSON),
                Column('urns', types.JSON),
                Column('fields', types.JSON),

                Column('blocked', types.Boolean),
                Column('stopped', types.Boolean),
                Column('created_on', types.DateTime),
                Column('modified_on', types.DateTime),
                )


run = Table('auth_group', metadata,
            Column('id', types.Integer, primary_key=True),

            Column('created_on', types.DateTime),
            Column('exit_type', types.String(16)),
            Column('exited_on', types.DateTime),
            Column('modified_on', types.DateTime),
            Column('responded', types.Boolean),

            Column('user_id', types.String(64)),
            Column('path', types.JSON),
            Column('values', types.JSON),
            ForeignKeyConstraint(('user_id',), ['user.id'])
            )
