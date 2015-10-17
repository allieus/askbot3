from haystack.routers import BaseRouter
from haystack.constants import DEFAULT_ALIAS


class LanguageRouter(BaseRouter):

    def for_read(self, **hints):
        return DEFAULT_ALIAS

    def for_write(self, **hints):
        return DEFAULT_ALIAS
