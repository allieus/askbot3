from django.db import connection
from django.db import transaction


def table_exists(table_name):
    cursor = connection.cursor()
    return table_name in connection.introspection.get_table_list(cursor)


def commit_manually(fn):
    def wrap(*args, **kwargs):
        transaction.set_autocommit(False)
        try:
            return fn(*args, **kwargs)
        finally:
            transaction.set_autocommit(True)
    return wrap

