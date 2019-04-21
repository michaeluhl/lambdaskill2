import json
import unittest

from lambdaskill2.requests import *
from lambdaskill2.responses.base import *
from lambdaskill2.responses.dialog import *


class DialogTestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/integration/data/dialog-intent-base.json', 'rt') as json_file:
            self.intent = Intent(json.load(json_file))
        with open('tests/integration/data/dialog-intent-base2.json', 'rt') as json_file:
            self.intent2 = Intent(json.load(json_file))
        with open('tests/integration/data/response-dialog-delegate.json', 'rt') as json_file:
            self.delegate = json.load(json_file)
        with open('tests/integration/data/response-dialog-elicitslot.json', 'rt') as json_file:
            self.elicitslot = json.load(json_file)
        with open('tests/integration/data/response-dialog-confirmslot.json', 'rt') as json_file:
            self.confirmslot = json.load(json_file)
        with open('tests/integration/data/response-dialog-confirmintent.json', 'rt') as json_file:
            self.confirmintent = json.load(json_file)


    def test_dialog_delegate(self):
        directive = DelegateDialogDirective(updated_intent=self.intent)
        self.assertEqual(json.dumps(self.delegate, sort_keys=True),
                         json.dumps(directive.prepare(), sort_keys=True))

    def test_dialog_elicitslot(self):
        directive = ElicitSlotDialogDirective(updated_intent=self.intent2,
                                              slot_to_elicit='string')
        self.assertEqual(json.dumps(self.elicitslot, sort_keys=True),
                         json.dumps(directive.prepare(), sort_keys=True))

    def test_dialog_confirmslot(self):
        directive = ConfirmSlotDialogDirective(updated_intent=self.intent2,
                                               slot_to_confirm='string')
        self.assertEqual(json.dumps(self.confirmslot, sort_keys=True),
                         json.dumps(directive.prepare(), sort_keys=True))

    def test_dialog_confirmintent(self):
        directive = ConfirmIntentDialogDirective(updated_intent=self.intent2)
        self.assertEqual(json.dumps(self.confirmintent, sort_keys=True),
                         json.dumps(directive.prepare(), sort_keys=True))

