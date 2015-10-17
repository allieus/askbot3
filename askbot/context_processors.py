from django.conf import settings


def extra(request):
    return {
        'settings': settings,
    }

