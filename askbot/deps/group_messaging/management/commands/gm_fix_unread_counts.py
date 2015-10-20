from django.core.management.base import NoArgsCommand
from askbot.models import User
from askbot.utils.console import ProgressBar
from group_messaging.models import UnreadInboxCounter
from django.db import transaction
from askbot.utils.db import commit_manually

class Command(NoArgsCommand):

    @commit_manually
    def handle_noargs(self, *args, **kwargs):
        users = User.objects.all()
        count = users.count()
        message = 'Fixing inbox counts for the users'
        for user in ProgressBar(users.iterator(), count, message):
            counter = UnreadInboxCounter.get_for_user(user)
            counter.recalculate()
            counter.save()
            transaction.commit()
