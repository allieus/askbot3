from django.contrib import messages as django_messages
from django.shortcuts import redirect
from askbot.utils.forms import get_next_url


class CancelActionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'cancel' in request.GET or 'cancel' in request.POST:
            # TODO: use session messages for the anonymous users
            try:
                msg = getattr(view_func, 'CANCEL_MESSAGE')
            except AttributeError:
                msg = 'action canceled'
            # request.user.message_set.create(message=msg)
            django_messages.info(request, msg)
            return redirect(get_next_url(request))
        else:
            return None

