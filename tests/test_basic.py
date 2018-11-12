
from model.models import *
from common import ModelTestCase


class Test(ModelTestCase):

    def test_model(self):
        # Basic model test to make sure things are working
        loc = Location(city='Philadelphia')

        self.session.add(loc)
        self.session.commit()

        assert self.session.query(Location).count() == 1
        assert self.session.query(Location).first().kf_id
