from copy import deepcopy
import json
import unittest

from lambdaskill2.requests import *


class RequestBodyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/integration/data/request-intent.json', 'rt') as jsonfile:
            cls.json = json.load(jsonfile)

    def setUp(self):
        self.request = RequestBody(deepcopy(type(self).json))


class TestIntentRequest(RequestBodyTestCase):

    def test_intent_request(self):
        request = self.request.request
        self.assertIsInstance(request, IntentRequest)
        self.assertEqual(request.request_id, 'string-reqid')
        self.assertEqual(request.timestamp, 'string-timestamp')
        self.assertIs(request.dialog_state, DialogState.COMPLETED)

    def test_intent(self):
        request = self.request.request
        intent = request.intent
        self.assertEqual(intent.name, 'string-intentname')
        self.assertIs(intent.confirmation_status, ConfirmationStatus.CONFIRMED)

    def test_slots(self):
        intent = self.request.request.intent
        self.assertIsInstance(intent.slots, Slots)
        self.assertIn('SlotName', intent.slots)
        slot = intent.slots['SlotName']
        self.assertEqual(slot.name, 'SlotName')
        self.assertEqual(slot.value, 'string-slotvalue')
        self.assertIs(slot.confirmation_status, ConfirmationStatus.CONFIRMED)
        self.assertEqual(len(slot.resolutions), 1)
        resolution = slot.resolutions[0]
        self.assertEqual(resolution.authority, 'string-authority')
        self.assertIs(resolution.status_code, ResolutionStatus.ER_SUCCESS_MATCH)
        self.assertEqual(len(resolution.values), 1)
        value = resolution.values[0]
        self.assertIsInstance(value, ResolutionValue)
        self.assertEqual(value.name, 'string-resolutionvaluename')
        self.assertEqual(value.id, 'string-resolutionid')

