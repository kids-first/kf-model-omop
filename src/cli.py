from pprint import pprint
import os
import sys
from shutil import copyfile

import click

from utils.misc import time_it

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Simple CLI for interacting with Kids First OMOP database
    """
    pass


@click.command(name='create-omop')
@click.option('--refresh_all',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to download and use the latest '
              'OMOP CommonDataModel postgres schema when creating the db.')
@click.option('--from_schema',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to create the OMOP tables from '
              'defined ORM models or from the OMOP Postgres scripts.')
@click.option('--with_pk',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to add primary keys in OMOP db '
              'after creating the tables')
@click.option('--with_constraints',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to apply constraints to OMOP db '
              'after creating the tables')
@click.option('--with_index',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to add indices in OMOP db '
              'after creating the tables')
@click.option('--with_standard_vocab',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to populate the database '
              'with the OMOP standard vocabulary after its been created')
@time_it
def create_omop(refresh_all, from_schema, with_pk, with_constraints,
                with_index, with_standard_vocab):
    """
    Drop current db, create a new db with the OMOP tablesself.
    Optionally apply constraints, create indices or load the db with
    OMOP standard vocabulary.

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from omop import create_omop

    create_omop(refresh=refresh_all,
                from_schema=from_schema,
                with_pk=with_pk,
                with_constraints=with_constraints,
                with_index=with_index,
                with_standard_vocab=with_standard_vocab)


@click.command(name='drop-db')
@time_it
def drop_db():
    """
    Drop db regardless of the active connections

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from utils.db import drop_db

    drop_db()


@click.command()
@click.option('-o', '--output_filepath',
              default=os.path.join(os.getcwd(), 'erd.png'),
              show_default=True,
              type=click.Path(file_okay=True, dir_okay=False),
              help='The location of the generated ERD file')
@time_it
def erd(output_filepath):
    """
    Generate an entity relationship diagram from the OMOP database

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from utils.db import erd

    erd(filepath=output_filepath)


@click.command('code-template')
@click.option('-o', '--output_dir',
              default=os.getcwd(),
              show_default=True,
              type=click.Path(file_okay=False, dir_okay=True),
              help='The directory where the py file will be generated')
@time_it
def generate_code_template(output_dir):
    """
    Generate a .py file with template code for connecting to the DB and
    loading data in via the ORM models.
    """
    fname = 'loader.py'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    source_path = os.path.join(root_dir, 'factory', 'code_template.py')
    dest_path = os.path.join(output_dir, fname)

    if os.path.isfile(dest_path):
        print(f'Error {dest_path} already exists! '
              'Aborting to avoid overwrite!')
        sys.exit()
    else:
        copyfile(source_path, dest_path)

        print('Generated a template Python module to load data into db via '
              f'OMOP SQLAlchemy models. \nLocated at {dest_path}')


@click.command('list-tables')
@time_it
def list_tables():
    """
    List tables in the database. Convenience method for sanity checks.

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from utils.db import list_tables

    pprint(list_tables())


@click.command('autogen-models')
@click.option('--refresh_all',
              default=False,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to download and use the latest '
              'OMOP CommonDataModel postgres schema when creating the db.')
@time_it
def auto_gen_models(refresh_all):
    """
    Autogenerate the OMOP SQLAlchemy models
    """
    from factory import utils
    utils.auto_gen_models(refresh_schema=refresh_all)


@click.command('load-standard-vocab')
@time_it
def load_standard_vocab():
    """
    Load the standard vocabulary into OMOP db
    """
    from omop import load_standard_vocab
    load_standard_vocab()


@click.command('create-constraints')
@time_it
def create_constraints():
    """
    Apply the constraints to the OMOP database. Constraints require that the
    index has been created.
    """
    from omop import create_constraints
    create_constraints()


@click.command('create-index')
@time_it
def create_index():
    """
    Create indices in OMOP database
    """
    from omop import create_index
    create_index()


@click.command('create-pk')
@time_it
def create_pk():
    """
    Create primary keys in OMOP database
    """
    from omop import create_pk
    create_pk()


cli.add_command(create_omop)
cli.add_command(drop_db)
cli.add_command(erd)
cli.add_command(generate_code_template)
cli.add_command(list_tables)
cli.add_command(auto_gen_models)
cli.add_command(load_standard_vocab)
cli.add_command(create_constraints)
cli.add_command(create_index)
cli.add_command(create_pk)
