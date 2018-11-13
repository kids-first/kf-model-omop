
from model.models import Location


def test_model(db_session):
    # Basic model test to make sure things are working
    loc = Location(city='Philadelphia')

    db_session.add(loc)
    db_session.commit()

    assert db_session.query(Location).count() == 1
    assert db_session.query(Location).first().kf_id
