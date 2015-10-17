from django.core.management.base import NoArgsCommand
from django.db import transaction
from askbot.models import User
from askbot.utils.db import commit_manually


class Command(NoArgsCommand):
    @commit_manually
    def handle_noargs(self, **options):
        for user in User.objects.all():
            user.add_missing_askbot_subscriptions()
            transaction.commit()

