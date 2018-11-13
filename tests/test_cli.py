
from click.testing import CliRunner

import cli
from config import APP_CONFIG_ENV_VAR


def test_create_omop():
    """
    Test create omop db
    """
    env = {APP_CONFIG_ENV_VAR: 'testing'}
    runner = CliRunner()
    result = runner.invoke(cli.create_omop, [], env=env)

    assert result.exit_code == 0

    from sqlalchemy import inspect, create_engine
    from config import config as config_dict
    config = config_dict.get('testing')

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    inspector = inspect(engine)

    assert len(inspector.get_table_names()) == 37
