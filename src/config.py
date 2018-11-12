import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CDM_REPO_URL = 'git@github.com:kids-first/CommonDataModel.git'
APP_CONFIG_ENV_VAR = 'OMOP_CONFIG'


class Config:
    DB_NAME = 'omop'
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_PORT', 5432)
    PG_NAME = os.environ.get('PG_NAME', DB_NAME)
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
    DB_NAME = 'test'
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_TEMPLATE.format(user='postgres',
                                                            pw='',
                                                            host='localhost',
                                                            port=5432,
                                                            db=DB_NAME)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
