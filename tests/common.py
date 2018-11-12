import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as config_dict
from model.models import Base
from db import drop_tables

config = config_dict.get('testing')


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        drop_tables(config=config, engine=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
