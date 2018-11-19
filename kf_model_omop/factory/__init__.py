from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config as config_dict
from config import Config


@contextmanager
def scoped_session(config_name='development',
                   host=None, port=None, db_name=None, user=None, pw=None):
    """
    Provide a transactional scope around a series of operations

    Create a connection to the database, then create a context managed session
    that handles session life cycle managementself.

    See https://docs.sqlalchemy.org/en/latest/orm/session_basics.html for more
    information on SQLAlchemy db sessions.

    If you would like to use a preset group of db parameters use the
    config_name param. Possible values are: 'development', 'testing'.

    This is a key in the dict config.config. The value will
    be the Config class which encapsulates all of the db parameters.

    :param config_name: a string specifying which Config class to use.
    Config objects encapsulate all db parameters for a particular mode of
    operation like development, testing, etc.
    :param host: hostname of Postgres db
    :param port: prot of Postgres db
    :param db_name: name of db
    :param user: user to connect to Postgres db with
    :param pw: password to connect to Postgres db with
    """

    # Create engine
    config = config_dict.get(config_name)
    uri = Config.DB_URI_TEMPLATE.format(user=user or config.PG_USER,
                                        pw=pw or config.PG_PASS,
                                        host=host or config.PG_HOST,
                                        port=port or config.PG_PORT,
                                        db=db_name or config.PG_NAME)
    engine = create_engine(uri)

    # Start a session
    Session = sessionmaker()
    session = Session(bind=engine)

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
