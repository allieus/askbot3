'''Copied from Django 1.3.1 source code, it will use this model to'''

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy


@python_2_unicode_compatible
class Message(models.Model):
    """
    The message system is a lightweight way to queue messages for given
    users. A message is associated with a User instance (so it is only
    applicable for registered users). There's no concept of expiration or
    timestamps. Messages are created by the Django admin after successful
    actions. For example, "The poll Foo was created successfully." is a
    message.
    """
    user = models.ForeignKey(User, related_name='_message_set')
    message = models.TextField(ugettext_lazy('message'))

    def __str__(self):
        return self.message

