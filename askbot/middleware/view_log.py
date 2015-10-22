"""
This module records the site visits by the authenticated users

Included here is the ViewLogMiddleware
"""
from django.utils import timezone
from askbot import signals


class ViewLogMiddleware(object):
    """
    ViewLogMiddleware sends the site_visited signal

    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        # send the site_visited signal for the authenticated users
        if request.user.is_authenticated():
            # this signal has no sender
            signals.site_visited.send(None, user=request.user, timestamp=timezone.now())

