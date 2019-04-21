import json
import unittest

from lambdaskill2.enums import CardType, OutputTextType
from lambdaskill2.responses.base import *


class ResponseTestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/integration/data/response-standard.json', 'rt') as json_file:
            self.datum = json.load(json_file)
        self.card_content = 'Today will provide you a new learning opportunity.  Stick with it and the possibilities will be endless.'
        self.output_text = 'Today will provide you a new learning opportunity.  Stick with it and the possibilities will be endless. Can I help you with anything else?'
        self.reprompt_text = 'Can I help you with anything else?'
        self.session_attributes = {'supportedHoroscopePeriods': {'daily': True, 'weekly': False, 'monthly': False}}

    def test_card(self):
        card_json = self.datum['response']['card']
        card = Card(type_=CardType.SIMPLE).with_title('Horoscope')
        card.with_content(self.card_content)
        self.assertEqual(json.dumps(card_json, sort_keys=True),
                         json.dumps(card.prepare(), sort_keys=True))

    def test_outputspeech(self):
        output_json = self.datum['response']['outputSpeech']
        output = OutputText(self.output_text)
        self.assertEqual(json.dumps(output_json, sort_keys=True),
                         json.dumps(output.prepare(), sort_keys=True))

    def test_reprompt(self):
        reprompt_json = self.datum['response']['reprompt']['outputSpeech']
        reprompt = OutputText(self.reprompt_text)
        self.assertEqual(json.dumps(reprompt_json, sort_keys=True),
                         json.dumps(reprompt.prepare(), sort_keys=True))

    def test_response_body(self):
        response_body_json = self.datum
        print(self.datum)
        response = Response(should_end_session=False)
        response.with_card(Card(type_=CardType.SIMPLE,
                                title='Horoscope',
                                content=self.card_content))
        response.with_output(self.output_text)
        response.with_reprompt(self.reprompt_text)
        response_body = ResponseBody()
        response_body.with_response(response)
        print(response_body.prepare(session_attributes=self.session_attributes))
        self.assertEqual(json.dumps(response_body_json, sort_keys=True),
                         json.dumps(response_body.prepare(session_attributes=self.session_attributes), sort_keys=True))

