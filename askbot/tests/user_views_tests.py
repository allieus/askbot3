from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.six.moves.urllib.parse import urlparse, parse_qsl, unquote
from askbot.tests.utils import AskbotTestCase
from askbot.views.users import owner_or_moderator_required
from mock import Mock


class UserViewsTests(AskbotTestCase):

    def test_owner_or_mod_required_passes_url_parameters(self):
        @owner_or_moderator_required
        def mock_view(request, user, context):
            return None

        request = Mock(spec=('path', 'REQUEST', 'user'))
        request.user = AnonymousUser()
        request.REQUEST = {'abra': 'cadabra', 'foo': 'bar'}
        request.path = '/some/path/'
        user = self.create_user('user')
        response = mock_view(request, user, {})
        self.assertEqual(isinstance(response, HttpResponseRedirect), True)

        url = response['location']
        parsed_url = urlparse(url)

        self.assertEqual(parsed_url.path, reverse('user_signin'))

        next = dict(parse_qsl(parsed_url.query))['next']
        next_url = unquote(next)
        parsed_url = urlparse(next_url)

        self.assertEqual(parsed_url.path, request.path)

        query = dict(parse_qsl(parsed_url.query))
        self.assertEqual(set(query.keys()), set(['foo', 'abra']))
        self.assertEqual(set(query.values()), set(['bar', 'cadabra']))
        self.assertEqual(query['abra'], 'cadabra')
