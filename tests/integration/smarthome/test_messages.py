import json
import unittest

from lambdaskill2.smarthome.messages import *


class MessageDirectiveTestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/integration/data/message-directive-turn_on-with_partition.json', 'rt') as jsonfile:
            self.json = json.load(jsonfile)

    def test_header(self):
        header = Header.from_json(self.json['directive']['header'])
        self.assertEqual(header.namespace, "Alexa.PowerController")
        self.assertEqual(header.name, "TurnOn")
        self.assertEqual(header.message_id, "message-id")
        self.assertEqual(header.correlation_token, "correlation-token")
        self.assertEqual(header.payload_version, "3")

    def test_scope_with_partition(self):
        scope = Scope.from_json(self.json['directive']['endpoint']['scope'])
        self.assertIs(scope.type, ScopeType.BEARER_TOKEN_WITH_PARTITION)
        self.assertEqual(scope.token, "access-token")
        self.assertEqual(scope.partition, "partition-id")
        self.assertEqual(scope.user_id, "user-id")

    def test_endpoint(self):
        endpoint = EndPoint.from_json(self.json['directive']['endpoint'])
        self.assertIsInstance(endpoint.scope, Scope)
        self.assertEqual(endpoint.endpoint_id, "endpoint-id")
        self.assertDictEqual(endpoint.cookie, {"key-1": "value-1",
                                               "key-0": "value-0"})

    def test_directive(self):
        directive = Directive.from_json(self.json['directive'])
        self.assertIsInstance(directive.header, Header)
        self.assertIsInstance(directive.endpoint, EndPoint)
        self.assertDictEqual(directive.payload, {})


class BearerTokenScopeTestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/integration/data/message-directive-turn_on.json', 'rt') as jsonfile:
            self.json = json.load(jsonfile)

    def test_scope(self):
        scope = Scope.from_json(self.json['directive']['endpoint']['scope'])
        self.assertIs(scope.type, ScopeType.BEARER_TOKEN)
        self.assertEqual(scope.token, "access-token")
        self.assertRaises(TypeError, getattr, scope, "partition")
        self.assertRaises(TypeError, getattr, scope, "user_id")


class SmartHomeRequestTestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/integration/data/message-directive-turn_on-with_partition.json', 'rt') as jsonfile:
            self.json = json.load(jsonfile)

    def test_smart_home_request(self):
        request = SmartHomeRequest.from_json(self.json)
        self.assertIsInstance(request.directive, Directive)
