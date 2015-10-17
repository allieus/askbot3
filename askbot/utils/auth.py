import re
from askbot.conf import settings as askbot_settings


def email_is_blacklisted(email):
    patterns = askbot_settings.BLACKLISTED_EMAIL_PATTERNS
    patterns = patterns.strip().split()
    for pattern in patterns:
        try:
            regex = re.compile(r'{}'.format(pattern))
        except:
            pass
        else:
            if regex.search(email):
                return True
    return False

