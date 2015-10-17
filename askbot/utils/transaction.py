"""Utilities for working with database transactions"""
from django.conf import settings as django_settings
from django.db import connection
from django.db.transaction import atomic


class DummyTransaction(object):
    """Dummy transaction class
    that can be imported instead of the django
    transaction management and debug issues
    inside the code running inside the transaction blocks
    """
    @classmethod
    def commit(cls):
        pass

    @classmethod
    def commit_manually(cls, func):
        def decorated(*args, **kwargs):
            func(*args, **kwargs)
        return decorated

# a utility instance to use instead of the normal transaction object
dummy_transaction = DummyTransaction()


def defer_celery_task(task, **kwargs):
    if django_settings.CELERY_ALWAYS_EAGER:
        return task.apply_async(**kwargs)
    else:
        return defer(task.apply_async, **kwargs)


def defer(f, *args, **kwargs):
    with atomic():
        connection.on_commit(lambda: f(*args, **kwargs))

