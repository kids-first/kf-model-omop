import os
import sys
import subprocess
from shutil import copyfile, rmtree

from sqlalchemy import create_engine

from kf_model_omop.config import (
    ROOT_DIR,
    CDM_REPO_URL,
    CDM_STANDARD_VOCAB_DIR,
    OMOP_VOCAB_TABLES
)
from kf_model_omop.model.models import Base
from kf_model_omop.utils.db import create_db, drop_db, _select_config

CREATE_TABLES_SCRIPT = 'OMOP CDM postgresql ddl.txt'
CREATE_PK_INDEX_SCRIPT = 'OMOP CDM postgresql pk indexes.txt'
CREATE_PK_SCRIPT = 'OMOP CDM postgresql pk.txt'
CREATE_INDEX_SCRIPT = 'OMOP CDM postgresql indexes.txt'
CREATE_CONSTRAINTS_SCRIPT = 'OMOP CDM postgresql constraints.txt'
VOCAB_LOAD_SCRIPT = 'OMOP CDM vocabulary load - PostgreSQL.sql'
SCRIPTS_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'scripts')


def create_omop(config_name=None, refresh=True, from_schema=False,
                with_pk=False, with_constraints=False, with_index=False,
                with_standard_vocab=False):
    """
    Drop db, create new omop db, then create tables, indices, and constraints

    :param config_name: a dict key which specifies which Config class to select
    in config.config dict. The Config class encapsulates all db parameters such
    as user, pw, host, port, and name of the db. See config.py for more info.
    :param refresh: boolean specifying whether to refresh the init-db
    postgres scripts
    """
    # Download the latest OMOP CDM postgres schema
    if refresh:
        refresh_pg_scripts()

    # Drop db and create new one
    drop_db(config_name)
    create_db(config_name)

    # Initialize db - create tables, indices, constraints
    config = _select_config(config_name)
    uri = config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(uri)

    print(f'Setting up new OMOP db at {config.PG_HOST}/{config.PG_NAME}...')

    # From models
    if not from_schema:
        Base.metadata.create_all(engine)

        # Load standard vocab
        if with_standard_vocab:
            load_standard_vocab(engine=engine)

    # Directly from postgres scripts
    else:
        # Only run if required postgres scripts exist
        _check_for_scripts()

        # Execute each sql script needed to setup db
        with engine.connect() as conn:
            # Tables
            create_tables(conn=conn)

            # Primary keys
            if with_pk:
                create_pk(conn=conn)

            # Constraints
            if with_constraints:
                create_constraints(conn=conn)

            # Load standard vocab
            if with_standard_vocab:
                load_standard_vocab(engine=engine)

            # Indices
            if with_index:
                create_index(conn=conn)


def refresh_pg_scripts(url=CDM_REPO_URL):
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
    cmd = (f'git clone {url} {model_dir}')
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

    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if not (f.endswith('.txt') or f.endswith('.sql')):
                continue
            source_file = os.path.join(root, f)
            dest_file = os.path.join(dest_dir, os.path.basename(source_file))
            copyfile(source_file, dest_file)

    # Delete model dir
    rmtree(model_dir)

    print('Refresh Complete!')


def create_tables(config_name=None, conn=None):
    exec_pg_script(CREATE_TABLES_SCRIPT, conn=conn)


def create_index(config_name=None, conn=None):
    exec_pg_script(CREATE_INDEX_SCRIPT, conn=conn)


def create_pk(config_name=None, conn=None):
    exec_pg_script(CREATE_PK_SCRIPT, conn=conn)


def create_constraints(config_name=None, conn=None):
    exec_pg_script(CREATE_CONSTRAINTS_SCRIPT, conn=conn)


def load_standard_vocab(config_name=None, engine=None, include_only=None):
    """
    Load standard vocabularies
    """
    if not engine:
        engine = _create_engine(config_name)

    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()

    # Disable triggers and constraints
    set_session_replication = 'set session_replication_role = {}; '
    cursor.execute(set_session_replication.format('replica'))

    # Delete current data
    delete_tables = '\n'.join([f'delete from {table_name};'
                               for table_name in OMOP_VOCAB_TABLES])

    print(f'Deleting standard vocabulary ...\n{delete_tables}')
    cursor.execute(delete_tables)

    # Load standard vocabulary
    for fname in os.listdir(CDM_STANDARD_VOCAB_DIR):
        table_name = fname.split('.')[0].lower()
        if table_name not in OMOP_VOCAB_TABLES:
            continue
        if (include_only is not None) and (table_name not in include_only):
            continue

        copy_sql = (f"COPY {table_name} FROM STDIN WITH DELIMITER E'\t' "
                    "CSV HEADER QUOTE E'\b' ;")

        filepath = os.path.join(CDM_STANDARD_VOCAB_DIR, fname)
        file_obj = open(filepath, 'r')

        print(f'Loading standard vocabulary for {table_name}')
        cursor.copy_expert(copy_sql, file=file_obj)
        raw_conn.commit()

    # Enable triggers and constraints
    cursor.execute(set_session_replication.format('origin'))

    cursor.close()
    raw_conn.close()

    print('\nStandard vocabulary loading complete!')


def exec_pg_script(filename, config_name=None, conn=None):
    """
    Execute postgres script
    """
    close_at_completion = False

    # Create a connection if it wasn't passed in
    if not conn:
        close_at_completion = True
        engine = _create_engine(config_name)
        conn = engine.connect()

    script_dir = os.path.join(SCRIPTS_DIR, 'postgres')
    filepath = os.path.join(script_dir, filename)

    print(f'\tExecuting {filepath}')

    with open(filepath, 'r') as pg_script:
        init_script = pg_script.read()

    conn.execute(init_script)
    conn.execute('commit')

    # Only close the connection if it was created here
    if close_at_completion:
        conn.close()


def _create_engine(config_name=None):
    """
    Helper method to create an engine instance
    """
    config = _select_config(config_name)
    uri = config.SQLALCHEMY_DATABASE_URI
    return create_engine(uri)


def _check_for_scripts():
    """
    Checks for existence of necessary Postgres scripts. Exits if none are found
    """
    script_dir = os.path.join(SCRIPTS_DIR, 'postgres')

    if len(os.listdir(script_dir)) < 2:
        print(f'\nError! No OMOP Postgres scripts found in {script_dir}. '
              'You need to to run create-omop with the refresh_all flag to '
              'download latest scripts.')
        sys.exit()
