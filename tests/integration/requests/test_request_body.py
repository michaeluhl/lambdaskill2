from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestBodyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/integration/data/request-launch.json', 'rt') as jsonfile:
            cls.json = json.load(jsonfile)

    def setUp(self):
        self.request = RequestBody(deepcopy(type(self).json))


class TestRequestBody(RequestBodyTestCase):

    def test_version(self):
        self.assertEqual(self.request.version, '1.0')


class TestSession(RequestBodyTestCase):

    def test_session_class(self):
        self.assertIsInstance(self.request.session, Session)

    def test_new(self):
        self.assertEqual(self.request.session.new, True)

    def test_session_id(self):
        self.assertEqual(self.request.session.session_id,
                         'amzn1.echo-api.session.[unique-value-here]')

    def test_session_application(self):
        application = self.request.session.application
        self.assertIsInstance(application, Application)
        self.assertEqual(application.application_id,
                         'amzn1.ask.skill.[unique-value-here]')

    def test_session_attributes(self):
        attributes = self.request.session.attributes
        self.assertIsInstance(attributes, dict)
        self.assertEqual(attributes['key'], 'string value')

    def test_session_user(self):
        user = self.request.session.user
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id,
                         'amzn1.ask.account.[unique-value-here]')
        self.assertEqual(user.access_token,
                         'Atza|AAAAAAAA...')
        self.assertIsInstance(user.permissions, Permissions)
        self.assertEqual(user.permissions.consent_token,
                         'ZZZZZZZ...')


class TestContext(RequestBodyTestCase):

    def test_context_class(self):
        self.assertIsInstance(self.request.context, Context)

    def test_context_system(self):
        system = self.request.context.system
        self.assertIsInstance(system, System)
        self.assertEqual(system.api_endpoint,
                         'https://api.amazonalexa.com')
        self.assertEqual(system.api_access_token,
                         'AxThk...')

    def test_context_system_device(self):
        system = self.request.context.system
        device = system.device
        self.assertIsInstance(device, Device)
        self.assertEqual(device.device_id, 'string')
        supported_interfaces = device.supported_interfaces
        self.assertIsInstance(supported_interfaces, dict)
        self.assertIn('AudioPlayer', supported_interfaces)
        self.assertIsInstance(supported_interfaces['AudioPlayer'], dict)

    def test_context_system_application(self):
        system = self.request.context.system
        application = system.application
        self.assertIsInstance(application, Application)
        self.assertEqual(application.application_id,
                         'amzn1.ask.skill.[unique-value-here]')

    def test_context_system_user(self):
        system = self.request.context.system
        user = system.user
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id,
                         'amzn1.ask.account.[unique-value-here]')
        self.assertEqual(user.access_token,
                         'Atza|AAAAAAAA...')
        self.assertIsInstance(user.permissions, Permissions)
        self.assertEqual(user.permissions.consent_token,
                         'ZZZZZZZ...')

    def test_context_audio_player(self):
        audio_player = self.request.context.audio_player
        self.assertIsInstance(audio_player, AudioPlayer)
        self.assertIs(audio_player.player_activity, PlayerActivity.PLAYING)
        self.assertEqual(audio_player.token,
                         'audioplayer-token')
        self.assertEqual(audio_player.offset_in_milliseconds, 0)


class TestLaunchRequest(RequestBodyTestCase):

    def test_launch_request(self):
        request = self.request.request
        self.assertIsInstance(request, LaunchRequest)
        self.assertEqual(request.request_id, 'string-reqid')
        self.assertEqual(request.timestamp, 'string-timestamp')
        self.assertEqual(request.locale, 'string')

