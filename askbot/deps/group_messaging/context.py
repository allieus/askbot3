from group_messaging.models import UnreadInboxCounter


def group_messaging_context(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        instance = UnreadInboxCounter.get_for_user(request.user)
        return {'group_messaging_unread_inbox_count': instance.count}
    return {}

