import os

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

from config import config as config_dict
from config import (
    ROOT_DIR,
    APP_CONFIG_ENV_VAR,
)

SCRIPTS_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'scripts')


def drop_db(config_name=None):
    """
    Drop all active connections and drop database
    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    """
    config = _select_config(config_name)

    # Read sql to drop active connections
    drop_conns_file = os.path.join(SCRIPTS_DIR, 'postgres', 'drop_conns.txt')
    with open(drop_conns_file) as f:
        drop_conns_sql_str = f.read()
        drop_conns_sql_str = drop_conns_sql_str.format(
            DB_NAME=config.PG_NAME)

    # Create db conn
    uri = config.DB_URI_TEMPLATE.format(user=config.PG_USER,
                                        pw=config.PG_PASS,
                                        host=config.PG_HOST,
                                        port=config.PG_PORT,
                                        db='postgres')
    engine = create_engine(uri)
    with engine.connect() as conn:
        conn.execute('commit')

        # Drop connections
        print(f'Dropping all connections to {config.PG_NAME} db ...')
        conn.execute(drop_conns_sql_str)

        # Drop database
        print(f'Dropping db {config.PG_NAME} ...')
        conn.execute(f'drop database if exists "{config.PG_NAME}"')
        conn.execute('commit')


def create_db(config_name=None):
    """
    Create new database

    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    """
    config = _select_config(config_name)

    # Create db conn
    uri = config.DB_URI_TEMPLATE.format(user=config.PG_USER,
                                        pw=config.PG_PASS,
                                        host=config.PG_HOST,
                                        port=config.PG_PORT,
                                        db='postgres')

    print(f'Creating new db {config.PG_NAME}...')

    engine = create_engine(uri)
    with engine.connect() as conn:
        # Create new db
        conn.execute('commit')
        conn.execute(f'create database "{config.PG_NAME}"')


def erd(config_name=None, filepath=None):
    """
    Generate an entity relationship diagram from the database

    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    :param filepath: Path to output ERD file
    """
    config = _select_config(config_name)

    doc_dir = os.path.join(os.path.dirname(ROOT_DIR), 'docs')
    if not filepath:
        filepath = os.path.join(doc_dir, 'erd.png')

    # Draw from database
    from eralchemy import render_er
    print(f'Generating ERD for {config.PG_HOST}/{config.PG_NAME} ...')
    render_er(config.SQLALCHEMY_DATABASE_URI, filepath)

    print(f'Entity relationship diagram generated: {filepath}')


def drop_tables(config_name=None):
    """
    Drop all tables despite existing constraints

    Source https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/DropEverything # noqa E501

    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    """
    config = _select_config(config_name)

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    conn = engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


def list_tables(config_name=None):
    """
    A convenience method to list tables in the database

    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    """
    from utils.db import _select_config
    from sqlalchemy import create_engine, inspect

    config = _select_config(config_name=None)
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    inspector = inspect(engine)
    print(f'Listing tables for {config.PG_HOST}/{config.PG_NAME}')

    return inspector.get_table_names()


def _select_config(config_name):
    """
    Get the operating mode from the environment var, then use that to
    select the Config class. If the environment var is not defined, default
    to the 'development' mode.
    """
    if config_name:
        return config_dict.get(config_name, 'default')
    else:
        return config_dict.get(os.getenv(APP_CONFIG_ENV_VAR) or
                               'development')
