import pytz
from datetime import date, datetime, timedelta
from django.conf import settings as django_settings


def get_current_tz():
    return pytz.timezone(django_settings.TIME_ZONE)


def get_today_range():
    today = date.today()
    today_tz = datetime(today.year, today.month, today.day, 0, 0, 0, 0, get_current_tz())
    return (today_tz, today_tz + timedelta(days=1))

