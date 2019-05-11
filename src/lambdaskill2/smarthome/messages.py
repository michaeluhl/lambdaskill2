from uuid import uuid4

from lambdaskill2.enums import StrEnum


class ScopeType(StrEnum):
    BEARER_TOKEN = "BearerToken"
    BEARER_TOKEN_WITH_PARTITION = "BearerTokenWithPartition"


class Scope(object):

    def __init__(self, type_, token, partition=None, user_id=None):
        self.__type = ScopeType(type_)
        self.__token = token
        if self.__type is ScopeType.BEARER_TOKEN_WITH_PARTITION:
            if partition is None or user_id is None:
                raise ValueError('partition and user_id are required for BEARER_TOKEN_WITH_PARTITION')
        self.__partition = partition
        self.__user_id = user_id

    @property
    def type(self):
        return self.__type

    @property
    def token(self):
        return self.__token

    @property
    def partition(self):
        if self.__type is ScopeType.BEARER_TOKEN:
            raise TypeError('BEARER_TOKEN-type scopes do not support the "partition" attribute.')
        return self.__partition

    @property
    def user_id(self):
        if self.__type is ScopeType.BEARER_TOKEN:
            raise TypeError('BEARER_TOKEN-type scopes do not support the "user_id" attribute.')
        return self.__user_id

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(type_=json['type'],
                   token=json['token'],
                   partition=json.get('partition', None),
                   user_id=json.get('userId', None))

    def prepare(self):
        container = {
            'type': self.__type,
            'token': self.__token
            }
        if self.__type is ScopeType.BEARER_TOKEN_WITH_PARTITION:
            container['partition'] = self.__partition
            container['userId'] = self.__user_id
        return container


class EndPoint(object):

    def __init__(self, scope, endpoint_id, cookie=None):
        self.__scope = scope
        self.__endpoint_id = endpoint_id
        self.__cookie = cookie if cookie is not None else {}

    @property
    def scope(self):
        return self.__scope

    @property
    def endpoint_id(self):
        return self.__endpoint_id

    @property
    def cookie(self):
        return self.__cookie

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(scope=Scope.from_json(json['scope']),
                   endpoint_id=json['endpointId'],
                   cookie=json['cookie'])

    def prepare(self):
        return {
            'scope': self.__scope.prepare(),
            'endpointId': self.__endpoint_id,
            'cookie': self.__cookie
            }


class Header(object):

    def __init__(self, namespace, name, payload_version, message_id=None, correlation_token=None):
        self.__namespace = namespace
        self.__name = name
        self.__payload_version = payload_version
        self.__message_id = message_id
        if not self.__message_id:
            self.__message_id = str(uuid4())
        self.__correlation_token = correlation_token

    @property
    def namespace(self):
        return self.__namespace

    @property
    def name(self):
        return self.__name

    @property
    def payload_version(self):
        return self.__payload_version

    @property
    def message_id(self):
        return self.__message_id

    @property
    def correlation_token(self):
        return self.__correlation_token

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(namespace=json['namespace'],
                   name=json['name'],
                   message_id=json['messageId'],
                   correlation_token=json.get('correlationToken', None),
                   payload_version=json['payloadVersion'])

    def prepare(self):
        container = {
            'namespace': self.__namespace,
            'name': self.__name,
            'payloadVersion': self.__payload_version,
            'messageId': self.__message_id
            }
        if self.__correlation_token is not None:
            container['correlationToken'] = self.__correlation_token
        return container


class Message(object):

    def __init__(self, header, endpoint, payload):
        self.__header = header
        self.__endpoint = endpoint
        self.__payload = payload if payload else {}

    @property
    def header(self):
        return self.__header

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def payload(self):
        return self.__payload

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(header=Header.from_json(json.get('header', None)),
                   endpoint=EndPoint.from_json(json.get('endpoint', None)),
                   payload=None)

    def prepare(self):
        container = {}
        if self.__header is not None:
            container['header'] = self.__header.prepare()
        if self.__endpoint is not None:
            container['endpoint'] = self.__endpoint.prepare()
        if self.__payload is not None:
            container['payload'] = self.__payload
        return container


class Directive(Message):

    pass


class Event(Message):

    def __init__(self, header, endpoint, payload=None, context=None):
        if payload is None:
            payload = {}
        super(Event, self).__init__(header=header,
                                    endpoint=endpoint,
                                    payload=payload)

    def with_payload(self, payload):
        self.__payload = payload
        return self


class SmartHomeRequest(object):

    def __init__(self, directive):
        self.__directive = directive

    @property
    def directive(self):
        return self.__directive

    @classmethod
    def from_json(cls, json):
        return cls(directive=Directive.from_json(json['directive']))


class SmartHomeResponse(object):

    def __init__(self, event, context=None):
        self.__event = event
        self.__context = context

    @property
    def event(self):
        return self.__event

    @property
    def context(self):
        return self.__context

    def with_context(self, context):
        self.__context = context
        return self

    def prepare(self):
        container = {'event': self.__event.prepare()}
        if self.__context is not None:
            container['context'] = self.__context.prepare()
        return container
