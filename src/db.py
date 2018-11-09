import os
import subprocess
from shutil import copyfile, rmtree

from sqlalchemy import create_engine

from config import DevelopmentConfig as config
from config import ROOT_DIR

INIT_DB_SCRIPTS = ['OMOP CDM postgresql ddl.txt',
                   'OMOP CDM postgresql pk indexes.txt',
                   'OMOP CDM postgresql constraints.txt']


def refresh_pg_scripts():
    """
    Delete current OMOP CDM postgres scripts and download latest
    from OHSDI CommonDataModel git repository
    """
    print('Preparing to refresh OMOP CommonDataModel postgres schema ...')

    model_dir = os.path.join(ROOT_DIR, 'scripts', 'model')

    # Delete repo if exists
    if os.path.isdir(model_dir):
        rmtree(model_dir)

    # Clone fresh repo
    cmd = (f'git clone {config.CDM_REPO_URL} {model_dir}')
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
    dest_dir = os.path.join(ROOT_DIR, 'scripts', 'postgres')

    for pg_script in INIT_DB_SCRIPTS:
        source_file = os.path.join(source_dir, pg_script)
        dest_file = os.path.join(dest_dir, pg_script)
        copyfile(source_file, dest_file)

    # Delete model dir
    rmtree(model_dir)

    print('Refresh Complete!')


def init_db(refresh=True):
    """
    Drop db, create new db, then create tables, indices, and constraints

    :param refresh: boolean specifying whether to refresh the init-db
    postgres scripts
    """
    # Download the latest OMOP CDM postgres schema
    if refresh:
        refresh_pg_scripts()

    # Drop db and create new one
    drop_and_create_db()

    # Initialize db - create tables, indices, constraints
    uri = config.SQLALCHEMY_DATABASE_URI
    print(f'Setting up new {config.DB_NAME} db at {uri}...')

    engine = create_engine(uri)
    with engine.connect() as conn:
        script_dir = os.path.join(ROOT_DIR, 'scripts', 'postgres')
        # Execute each sql script needed to setup db
        for fname in INIT_DB_SCRIPTS:
            filepath = os.path.join(script_dir, fname)

            print(f'\tExecuting {filepath}')

            with open(filepath, 'r') as pg_script:
                init_script = pg_script.read()

            conn.execute(init_script)
            conn.execute('commit')


def drop_and_create_db():
    """
    Drop omop database regardless of existing connections
    Create new omop database
    """
    # Read sql in
    drop_conns_file = os.path.join(ROOT_DIR, 'scripts',
                                   'postgres', 'drop_conns.txt')
    with open(drop_conns_file) as f:
        drop_conns_sql_str = f.read()
        drop_conns_sql_str = drop_conns_sql_str.format(
            DB_NAME=config.DB_NAME)

    # Create conn
    uri = config.DB_URI_TEMPLATE.format(user='postgres',
                                        pw='',
                                        host=config.PG_HOST,
                                        port=config.PG_PORT,
                                        db='postgres')
    engine = create_engine(uri)
    with engine.connect() as conn:
        conn.execute('commit')

        # Drop connections
        print(f'Dropping {config.DB_NAME} db and creating new one ...')
        conn.execute(drop_conns_sql_str)

        # Drop and create database
        conn.execute(f'drop database if exists {config.DB_NAME}')
        conn.execute('commit')
        conn.execute(f'create database {config.DB_NAME}')


def erd(filepath=None):
    doc_dir = os.path.join(os.path.dirname(ROOT_DIR), 'docs')
    if not filepath:
        filepath = os.path.join(doc_dir, 'erd.png')

    # Draw from database
    from eralchemy import render_er
    render_er(config.SQLALCHEMY_DATABASE_URI, filepath)

    print(f'Entity relationship diagram generated: {filepath}')


def clear_db():
    pass
