import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as config_dict
from model.models import Base
from db import drop_tables

config = config_dict.get('testing')


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        # Drop all tables in test db and create new tables
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        drop_tables(config=config)
        Base.metadata.create_all(self.engine)
        # Start a session
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
