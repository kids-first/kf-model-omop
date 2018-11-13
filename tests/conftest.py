import pytest
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as config_dict
from model.models import Base
from db import drop_tables

config = config_dict.get('testing')


@pytest.fixture(scope='session')
def db_session():
    # Drop all tables in test db and create new tables
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    drop_tables(config=config)
    Base.metadata.create_all(engine)

    # Start a session
    session = sessionmaker(bind=engine)()
    yield session

    # Teardown
    session.close()
