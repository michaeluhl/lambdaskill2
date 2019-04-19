from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestBodyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/integration/data/extra-request-intent.json', 'rt') as jsonfile:
            cls.json = json.load(jsonfile)

    def setUp(self):
        self.request = RequestBody(deepcopy(type(self).json))


class TestIntentSerialize(RequestBodyTestCase):

    def test_intent_serialize(self):
        intent_json = type(self).json['request']['intent']
        intent = self.request.request.intent
        self.assertEqual(json.dumps(intent_json, sort_keys=True),
                         json.dumps(intent.prepare(), sort_keys=True))

