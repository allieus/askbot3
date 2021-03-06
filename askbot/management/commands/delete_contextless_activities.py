from __future__ import print_function
from django.core.management.base import NoArgsCommand
from askbot.utils.console import ProgressBar
from askbot.models import Activity

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        acts = Activity.objects.all()
        deleted_count = 0
        message = "Searching for context-less activity objects:"
        for act in ProgressBar(acts.iterator(), acts.count(), message):
            try:
                if act.object_id is not None and act.content_object is None:
                    act.delete()
                    deleted_count += 1
            except:
                # this can happen if we have a stale content type
                act.delete()

        if deleted_count:
            print("%d activity objects deleted" % deleted_count)
        else:
            print("None found")
