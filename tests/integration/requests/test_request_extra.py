from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestExtraTestCase(unittest.TestCase):

    json_path = None

    @classmethod
    def setUpClass(cls):
        if cls.json_path:
            with open(cls.json_path, 'rt') as jsonfile:
                cls.json = json.load(jsonfile)

    def setUp(self):
        self.request = RequestBody(deepcopy(type(self).json))


class TestSessionEndedRequestExtra(RequestExtraTestCase):

    json_path = 'tests/integration/data/extra-request-session_ended.json'

    def test_session_ended_request(self):
        request_body = RequestBody(deepcopy(type(self).json))
        request = request_body.request
        self.assertIsInstance(request, SessionEndedRequest)


class TestIntentRequestExtra(RequestExtraTestCase):

    json_path = 'tests/integration/data/extra-request-intent.json'

    def test_intent_request(self):
        request_body = RequestBody(deepcopy(type(self).json))
        request = request_body.request
        self.assertIsInstance(request, IntentRequest)


class TestLaunchRequestExtra(RequestExtraTestCase):

    json_path = 'tests/integration/data/extra-request-launch.json'

    def test_launch_request(self):
        request_body = RequestBody(deepcopy(type(self).json))
        request = request_body.request
        self.assertIsInstance(request, LaunchRequest)

