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
              type=click.Path(file_okay=True, dir_okay=False))
def erd(output_filepath):
    """
    Generate an entity relationship diagram from the OMOP database
    """
    from db import erd

    erd(filepath=output_filepath)


cli.add_command(create_omop)
cli.add_command(drop_db)
cli.add_command(erd)
