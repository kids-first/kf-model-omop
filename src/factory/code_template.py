"""
An example module that loads a Location into the OMOP database

This is a simple example that shows how to use the scoped_session provided by
the kf-model-omop library. The scoped_session handles db session lifecycle
management so that the caller simply has to worry about the loading code.
"""

from model.models import *
from factory import scoped_session


# Use the context managed session to interact with DB
with scoped_session() as session:
    # Test load
    loc = Location(city='Philadelphia')

    session.add(loc)
    session.commit()

    assert session.query(Location).count() == 1
