from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestBodyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/integration/data/request-session_ended.json', 'rt') as jsonfile:
            cls.json = json.load(jsonfile)

    def setUp(self):
        self.request = RequestBody(deepcopy(type(self).json))


class TestSessionEndedRequest(RequestBodyTestCase):

    def test_session_ended_request(self):
        request = self.request.request
        self.assertIsInstance(request, SessionEndedRequest)
        self.assertEqual(request.request_id, 'string-reqid')
        self.assertEqual(request.timestamp, 'string-timestamp')
        self.assertIs(request.reason, SessionEndedReason.ERROR)
        self.assertIsInstance(request.error, SessionEndedError)
        self.assertIs(request.error.type, SessionEndedErrorType.INVALID_RESPONSE)
        self.assertEqual(request.error.message, 'string-message')

