import re
from unittest import TestCase

from django.conf import settings

settings.configure()

from fakebotdetector.middleware import FakeBotDetectorMiddleware


class Mock:
    pass


def get_response(request):
    response = Mock()
    response.status_code = 200
    return response


class MiddlewareTests(TestCase):

    def setUp(self):
        self.request = Mock()
        self.request.META = {'REMOTE_ADDR': '0.0.0.0', 'HTTP_USER_AGENT': 'GoogleBot'}
        self.middleware = FakeBotDetectorMiddleware(get_response=get_response)
        self.middleware.reverse_lookup = lambda x: 'real.google.com'
        self.middleware.ipaddress_is_private = lambda x: False
        self.middleware.BOTS = (('googlebot', re.compile(r'.*google\.com$')),)
        self.middleware.FAKE_BOT_RESPONSE_CODE = 403

    def test_real_bot(self):
        response = self.middleware.__call__(self.request)
        self.assertEqual(200, response.status_code)

    def test_fake_bot(self):
        self.middleware.reverse_lookup = lambda x: 'fake.bot.domain.com'
        response = self.middleware.__call__(self.request)
        self.assertEqual(403, response.status_code)

    def test_raise_if_remote_addr_missing(self):
        self.request.META.pop('REMOTE_ADDR')
        with self.assertRaises(RuntimeError):
            response = self.middleware.__call__(self.request)

    def test_setting_enabled(self):
        self.middleware.reverse_lookup = lambda x: 'fake.bot.domain.com'
        self.middleware.FAKE_BOT_DETECTOR_ENABLED = True
        response = self.middleware.__call__(self.request)
        self.assertEqual(403, response.status_code)
        self.middleware.FAKE_BOT_DETECTOR_ENABLED = False
        response = self.middleware.__call__(self.request)
        self.assertEqual(200, response.status_code)

    def test_setting_fake_bot_response_code(self):
        self.middleware.FAKE_BOT_RESPONSE_CODE = 444
        self.middleware.reverse_lookup = lambda x: 'fake.bot.domain.com'
        response = self.middleware.__call__(self.request)
        self.assertEqual(444, response.status_code)
