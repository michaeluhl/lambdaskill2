from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestBodyMissingObjectTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/integration/data/request-launch.json', 'rt') as jsonfile:
            cls.json = json.load(jsonfile)

    def setUp(self):
        self.request_json = deepcopy(type(self).json)

    def test_missing_session(self):
        del self.request_json['session']
        request = RequestBody(self.request_json)
        self.assertIsInstance(request, RequestBody)

    def test_missing_audio_player(self):
        del self.request_json['context']['System']['device']['supportedInterfaces']['AudioPlayer']
        del self.request_json['context']['AudioPlayer']
        request = RequestBody(self.request_json)
        self.assertIsInstance(request, RequestBody)

