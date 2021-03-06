import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_FILE_PATH = os.path.join(os.path.join(ROOT_DIR, 'model'), 'models.py')
CDM_REPO_URL = 'git@github.com:kids-first/CommonDataModel.git'
CDM_STANDARD_VOCAB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(ROOT_DIR)),
    'data', 'omop', 'standard_vocab')
APP_CONFIG_ENV_VAR = 'OMOP_CONFIG'
OMOP_VOCAB_TABLES = {'domain',
                     'concept_class',
                     'concept_ancestor',
                     'drug_strength',
                     'relationship',
                     'vocabulary',
                     'concept',
                     'concept_relationship',
                     'concept_synonym'}


class Config:
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_PORT', 5432)
    PG_NAME = os.environ.get('PG_NAME', 'omop')
    PG_USER = os.environ.get('PG_USER', 'postgres')
    PG_PASS = os.environ.get('PG_PASS', '')
    SQLALCHEMY_ECHO = False
    DB_URI_TEMPLATE = 'postgres://{user}:{pw}@{host}:{port}/{db}'
    SQLALCHEMY_DATABASE_URI = DB_URI_TEMPLATE.format(user=PG_USER,
                                                     pw=PG_PASS,
                                                     host=PG_HOST,
                                                     port=PG_PORT,
                                                     db=PG_NAME)


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    PG_NAME = 'test'
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_TEMPLATE.format(
        user=Config.PG_USER,
        pw=Config.PG_PASS,
        host=Config.PG_HOST,
        port=Config.PG_PORT,
        db=PG_NAME)


class TempConfig(Config):
    PG_NAME = 'temp'
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_TEMPLATE.format(
        user=Config.PG_USER,
        pw=Config.PG_PASS,
        host=Config.PG_HOST,
        port=Config.PG_PORT,
        db=PG_NAME)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "temp": TempConfig,
    "default": DevelopmentConfig
}
