import os
import subprocess

from kf_model_omop.utils.db import _select_config
from kf_model_omop.config import MODELS_FILE_PATH, ROOT_DIR


def auto_gen_models(config_name=None, refresh_schema=False,
                    model_filepath=MODELS_FILE_PATH):
    """
    Autogenerate the OMOP SQLAlchemy models

    Use sqlacodegen to generate models from the db. Then apply customizations
    to the models (i.e. add Kids First IDs, etc)
    """
    print('\nAuto-generating models ...\n')

    # Auto generate models from temp db
    generate_models_from_db(model_filepath, config_name)

    # Inject customizations into the models Python module
    customize_models(model_filepath)

    print(f'\nComplete - generated models: {model_filepath}')


def generate_models_from_db(model_filepath, config_name=None):
    """
    Use sqlacodegen to generate SQLAlchemy models Python module from Postgres
    """

    config = _select_config(config_name=config_name)

    cmd = (f'sqlacodegen {config.SQLALCHEMY_DATABASE_URI} '
           f'--outfile {model_filepath}')
    output = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output_str = output.stdout.decode('utf-8')

    print(output_str)

    if output.returncode != 0:
        raise Exception(
            f'Error in auto_gen_models!\n\n{output_str}')


def customize_models(model_filepath):
    """
    Modify models.py generated by generate_models_from_db with customizations

    Make all models inherit Base and ModelMixins
    Fix bug ConceptClas -> ConceptClass
    Add module docstring
    """
    # Find/replace things
    with open(model_filepath, 'r') as models_file:
        models_txt = models_file.read()
        models_txt = models_txt.replace('ConceptClas', 'ConceptClass')
        # models_txt = models_txt.replace('(Base)', '(Base, ModelMixins)')

    # Insert docstring and imports
    template_path = os.path.join(ROOT_DIR, 'factory', 'model_template.txt')
    with open(template_path, 'r') as template_file:
        customized_models_code = template_file.read()
        customized_models_code = customized_models_code.format(
            models=models_txt)

    # Update models.py
    with open(model_filepath, 'w') as models_file:
        models_file.write(customized_models_code)