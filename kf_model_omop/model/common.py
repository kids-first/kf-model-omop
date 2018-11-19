from datetime import datetime

import sqlalchemy as db
import sqlalchemy.types as types
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID

from kf_model_omop.model.id_service import kf_id_generator, uuid_generator


class KfId(types.TypeDecorator):
    """
    A kids first id type
    """
    impl = types.String

    def __init__(self, *args, **kwargs):
        kwargs['length'] = 50
        super(KfId, self).__init__(*args, **kwargs)


class IDMixin:
    """
    Defines base ID columns common on all Kids First tables
    """
    __prefix__ = '__'

    @declared_attr
    def kf_id(cls):
        kf_id = db.Column(KfId(), unique=True,
                          doc="ID assigned by Kids First",
                          default=kf_id_generator(cls.__tablename__))
        return kf_id

    uuid = db.Column(UUID(), unique=True, default=uuid_generator)


class TimestampMixin:
    """
    Defines the common timestammp columns on all Kids First tables
    """
    created_at = db.Column(db.DateTime(), default=datetime.now,
                           doc="Time of object creation")
    modified_at = db.Column(db.DateTime(), default=datetime.now,
                            onupdate=datetime.now,
                            doc="Time of last modification")


class ModelMixins(IDMixin, TimestampMixin):
    """
    Defines base SQlAlchemy model class
    :param visible: Flags visibility of data from the dataservice
    """
    pass
