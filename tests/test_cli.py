import os

from sqlalchemy import inspect, create_engine
from click.testing import CliRunner

from kf_model_omop import cli
from kf_model_omop.config import config as config_dict, APP_CONFIG_ENV_VAR
from kf_model_omop.factory.utils import auto_gen_models

env = {APP_CONFIG_ENV_VAR: 'testing'}


def test_create_omop():
    """
    Test create omop db
    """
    runner = CliRunner()
    result = runner.invoke(cli.create_omop, [], env=env)

    assert result.exit_code == 0

    config = config_dict.get('testing')

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    inspector = inspect(engine)

    assert len(inspector.get_table_names()) == 37


def test_code_template(tmpdir):
    """
    Test cli command code-template
    """
    # Create temp file
    fn = tmpdir.mkdir("data")
    expected_file = os.path.join(str(fn), 'loader.py')

    # Gen code template
    runner = CliRunner()
    result = runner.invoke(cli.generate_code_template,
                           ['-o', str(fn)], env=env)

    assert result.exit_code == 0
    assert os.path.isfile(expected_file)

    # Update file
    with open(expected_file, 'w') as f:
        f.write('print("hello world!")')

    # Try to generate file again
    result = runner.invoke(cli.generate_code_template,
                           ['-o', str(fn)], env=env)

    assert 'already exists' in result.stdout
    assert result.exit_code == 0

    # Check file
    with open(expected_file, 'r') as f:
        assert 'hello world!' in f.read()


def test_list_tables():
    """
    Test list tables
    """
    runner = CliRunner()
    result = runner.invoke(cli.list_tables, [], env=env)

    assert 'concept' in result.stdout
    assert result.exit_code == 0


def test_auto_gen_models(tmpdir_factory):
    """
    Test cli command code-template
    """
    # Create temp file
    fn = tmpdir_factory.mktemp("data").join('models.py')
    expected_file = str(fn)

    # Autogen models
    auto_gen_models(config_name='testing', refresh_schema=True,
                    model_filepath=expected_file)

    assert os.path.isfile(expected_file)

    # Check content
    with open(expected_file, 'r') as f:
        content = f.read()
        # assert 'ModelMixins' in content
        assert 'metadata' in content
