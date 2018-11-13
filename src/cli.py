import os
import sys
from shutil import copyfile

import click

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
              'OMOP CommonDataModel postgres schema when creating the db.'
              'This option will only take effect if the flag --from_models '
              'is present')
@click.option('--from_models',
              default=True,
              show_default=True,
              is_flag=True,
              help='A flag specifying whether to create the OMOP tables from '
              'defined ORM models or from the OMOP Postgres scripts.')
def create_omop(refresh_all, from_models):
    """
    Drop current db, create new db, then create OMOP tables, indices,
    and constraints

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from db import create_omop

    create_omop(from_models=from_models, refresh=refresh_all)


@click.command(name='drop-db')
def drop_db():
    """
    Drop db regardless of the active connections

    All db parameters such as user, pw, host, port, and name of the db are
    controlled through environment variables. See config.py for more info.
    """
    from db import drop_db

    drop_db()


@click.command()
@click.option('-o', '--output_filepath',
              default=os.path.join(os.getcwd(), 'erd.png'),
              show_default=True,
              type=click.Path(file_okay=True, dir_okay=False),
              help='The location of the generated ERD file')
def erd(output_filepath):
    """
    Generate an entity relationship diagram from the OMOP database
    """
    from db import erd

    erd(filepath=output_filepath)


@click.command('code-template')
@click.option('-o', '--output_dir',
              default=os.getcwd(),
              show_default=True,
              type=click.Path(file_okay=False, dir_okay=True),
              help='The directory where the py file will be generated')
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


cli.add_command(create_omop)
cli.add_command(drop_db)
cli.add_command(erd)
cli.add_command(generate_code_template)
