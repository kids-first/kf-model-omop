import uuid
import random
import base32_crockford as b32


def uuid_generator():
    """
    Returns a stringified uuid of 36 characters
    """
    return str(uuid.uuid4())


def kf_id_generator(table_name):
    """
    Returns a function to generator
    (Crockford)[http://www.crockford.com/wrmg/base32.html] base 32
    encoded number up to 8 characters left padded with 0 and prefixed with
    the entity table name and delimited by an underscore

    Ex:
    'PERSON_0004PEDE'
    'SPECIMEN_D167JSHP'
    'DIAGNOSIS_ZZZZZZZZ'
    """
    prefix = table_name.upper()

    def generator():
        return '{0}_{1:0>8}'.format(prefix,
                                    b32.encode(random.randint(0, 32**8-1)))

    return generator
