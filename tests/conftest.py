import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as config_dict
from model.models import Base
from utils.db import drop_tables

config = config_dict.get('testing')


@pytest.fixture(scope='session')
def db_session():
    # Drop all tables in test db and create new tables
    drop_tables(config_name='testing')

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

    # Start a session
    Session = sessionmaker()
    session = Session(bind=engine)

    yield session

    # Teardown
    session.close()
