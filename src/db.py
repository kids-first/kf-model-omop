import os
import subprocess
from shutil import copyfile, rmtree

from sqlalchemy import create_engine

from config import config as config_dict
from config import ROOT_DIR, APP_CONFIG_ENV_VAR, CDM_REPO_URL

INIT_DB_SCRIPTS = ['OMOP CDM postgresql ddl.txt',
                   'OMOP CDM postgresql pk indexes.txt',
                   'OMOP CDM postgresql constraints.txt']

SCRIPTS_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'scripts')

mode = os.getenv(APP_CONFIG_ENV_VAR) or 'development'


def refresh_pg_scripts():
    """
    Delete current OMOP CDM postgres scripts and download latest
    from OHSDI CommonDataModel git repository
    """
    print('Preparing to refresh OMOP CommonDataModel postgres schema ...')

    model_dir = os.path.join(SCRIPTS_DIR, 'model')

    # Delete repo if exists
    if os.path.isdir(model_dir):
        rmtree(model_dir)

    # Clone fresh repo
    cmd = (f'git clone {CDM_REPO_URL} {model_dir}')
    output = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output_str = output.stdout.decode('utf-8')

    print(output_str)

    if output.returncode != 0:
        raise Exception(
            f'Error in refresh postgres scripts!\n\n{output_str}')

    # Copy pg scripts to scripts/postgres
    source_dir = os.path.join(model_dir, 'PostgreSQL')
    dest_dir = os.path.join(SCRIPTS_DIR, 'postgres')

    for pg_script in INIT_DB_SCRIPTS:
        source_file = os.path.join(source_dir, pg_script)
        dest_file = os.path.join(dest_dir, pg_script)
        copyfile(source_file, dest_file)

    # Delete model dir
    rmtree(model_dir)

    print('Refresh Complete!')


def create_and_init_db(config=None, refresh=True):
    """
    Drop db, create new omop db, then create tables, indices, and constraints

    :param refresh: boolean specifying whether to refresh the init-db
    postgres scripts
    """
    config = config or config_dict.get(mode)

    # Download the latest OMOP CDM postgres schema
    if refresh:
        refresh_pg_scripts()

    # Drop db and create new one
    drop_db(config)
    create_db(config)

    # Initialize db - create tables, indices, constraints
    uri = config.SQLALCHEMY_DATABASE_URI
    print(f'Setting up new OMOP db at {uri}...')

    engine = create_engine(uri)
    with engine.connect() as conn:
        script_dir = os.path.join(SCRIPTS_DIR, 'postgres')
        # Execute each sql script needed to setup db
        for fname in INIT_DB_SCRIPTS:
            filepath = os.path.join(script_dir, fname)

            print(f'\tExecuting {filepath}')

            with open(filepath, 'r') as pg_script:
                init_script = pg_script.read()

            conn.execute(init_script)
            conn.execute('commit')


def drop_db(config):
    """
    Drop all active connections and drop DB
    """
    # Read sql to drop active connections
    drop_conns_file = os.path.join(SCRIPTS_DIR, 'postgres', 'drop_conns.txt')
    with open(drop_conns_file) as f:
        drop_conns_sql_str = f.read()
        drop_conns_sql_str = drop_conns_sql_str.format(
            DB_NAME=config.DB_NAME)

    # Create db conn
    uri = config.DB_URI_TEMPLATE.format(user='postgres',
                                        pw='',
                                        host=config.PG_HOST,
                                        port=config.PG_PORT,
                                        db='postgres')
    engine = create_engine(uri)
    with engine.connect() as conn:
        conn.execute('commit')

        # Drop connections
        print(f'Dropping all connections to {config.DB_NAME} db ...')
        conn.execute(drop_conns_sql_str)

        # Drop database
        print(f'Dropping db {config.DB_NAME} ...')
        conn.execute(f'drop database if exists {config.DB_NAME}')
        conn.execute('commit')


def create_db(config):
    """
    Create new database
    """
    # Create db conn
    uri = config.DB_URI_TEMPLATE.format(user='postgres',
                                        pw='',
                                        host=config.PG_HOST,
                                        port=config.PG_PORT,
                                        db='postgres')

    print(f'Creating new db {config.DB_NAME}...')

    engine = create_engine(uri)
    with engine.connect() as conn:
        # Create new db
        conn.execute('commit')
        conn.execute(f'create database {config.DB_NAME}')


def erd(config=None, filepath=None):
    """
    Generate an entity relationship diagram from the database
    """
    config = config or config_dict.get(mode)

    doc_dir = os.path.join(os.path.dirname(ROOT_DIR), 'docs')
    if not filepath:
        filepath = os.path.join(doc_dir, 'erd.png')

    # Draw from database
    from eralchemy import render_er
    print(config.SQLALCHEMY_DATABASE_URI)
    render_er(config.SQLALCHEMY_DATABASE_URI, filepath)

    print(f'Entity relationship diagram generated: {filepath}')
