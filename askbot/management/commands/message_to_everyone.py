from __future__ import print_function
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
import sys

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        msg = None
        if msg is None:
            print('to run this command, please first edit the file %s' % __file__)
            sys.exit(1)
        for u in User.objects.all():
            message = msg % u.username
            u.message_set.create(message=message)

