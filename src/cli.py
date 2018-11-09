import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Simple CLI for interacting with Kids First OMOP database
    """
    pass


@click.command()
@click.option('--refresh_schema',
              default=False,
              is_flag=True,
              help='A flag specifying whether to download and use the latest '
              'OMOP CommonDataModel postgres schema when creating the db')
def init_db(refresh_schema):
    """
    Drop current OMOP db, create new OMOP db, then create tables, indices,
    and constraints
    """
    from db import init_db

    init_db(refresh_schema)


cli.add_command(init_db)
