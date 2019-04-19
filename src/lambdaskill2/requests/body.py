from lambdaskill2.enums import PlayerActivity, SessionEndedReason, SessionEndedErrorType


class Application(object):

    def __init__(self, json):
        self.__application_id = json['applicationId']

    @property
    def application_id(self):
        return self.__application_id

    def __repr__(self):
        return "Application({}={})".format("application_id", self.__application_id)


class Permissions(object):

    def __init__(self, json):
        self.__consent_token = json['consentToken']

    @property
    def consent_token(self):
        return self.__consent_token

    def __repr__(self):
        return "Permissions({}={})".format("consent_token", self.__consent_token)


class User(object):

    def __init__(self, json):
        self.__user_id = json['userId']
        self.__access_token = json.get('accessToken', None)
        self.__permissions = Permissions(json['permissions']) if 'permissions' in json else None

    @property
    def user_id(self):
        return self.__user_id

    @property
    def access_token(self):
        return self.__access_token

    @property
    def permissions(self):
        return self.__permissions

    def __repr__(self):
        return "User({})".format(
            ",\n     ".join(
                ["{}={}".format(n, v) for n, v in (("user_id", self.__user_id),
                                                   ("access_token", self.__access_token),
                                                   ("permissions", self.__permissions))]
            )
        )


class Session(object):

    def __init__(self, json):
        self.__new = json['new']
        self.__session_id = json['sessionId']
        self.__attributes = json.get('attributes', {})
        self.__application = Application(json['application'])
        self.__user = User(json['user'])

    @property
    def new(self):
        return self.__new

    @property
    def session_id(self):
        return self.__session_id

    @property
    def attributes(self):
        return self.__attributes

    @property
    def application(self):
        return self.__application

    @property
    def user(self):
        return self.__user

    def __repr__(self):
        return "Session({})".format(
            ",\n        ".join(
                ["{}={}".format(n, v) for n, v in (("new", self.__new),
                                                   ("session_id", self.__session_id),
                                                   ("attributes", self.__attributes),
                                                   ("application", self.__application),
                                                   ("user", self.__user))]
            )
        )


class AudioPlayer(object):

    def __init__(self, json):
        self.__token = json.get('token', None)
        if 'offsetInMilliseconds' in json and json['offsetInMilliseconds'] is not None:
            self.__offset_in_milliseconds = int(json['offsetInMilliseconds'])
        else:
            self.__offset_in_milliseconds = None
        self.__player_activity = PlayerActivity(json['playerActivity'])

    @property
    def token(self):
        return self.__token

    @property
    def offset_in_milliseconds(self):
        return self.__offset_in_milliseconds

    @property
    def player_activity(self):
        return self.__player_activity

    def __repr__(self):
        return "AudioPlayer({})".format(
            ', '.join(['{}={}'.format(n, v) for n, v in (('token', self.__token),
                                                         ('offset_in_milliseconds', self.__offset_in_milliseconds),
                                                         ('player_activity', self.__player_activity))])
        )


class Device(object):

    def __init__(self, json):
        self.__device_id = json.get('deviceId', None)
        self.__supported_interfaces = json.get('supportedInterfaces', {})

    @property
    def device_id(self):
        return self.__device_id

    @property
    def supported_interfaces(self):
        return self.__supported_interfaces

    def __repr__(self):
        return "Device({})".format(
            ', '.join(['{}={}'.format(n, v) for n, v in (("device_id", self.__device_id),
                                                         ('supported_interfaces', self.__supported_interfaces))])
        )


class System(object):

    def __init__(self, json):
        self.__api_access_token = json.get('apiAccessToken', None)
        self.__api_endpoint = json.get('apiEndpoint', None)
        self.__application = Application(json['application'])
        self.__device = Device(json['device'])
        self.__user = User(json['user'])

    @property
    def api_access_token(self):
        return self.__api_access_token

    @property
    def api_endpoint(self):
        return self.__api_endpoint

    @property
    def application(self):
        return self.__application

    @property
    def device(self):
        return self.__device

    @property
    def user(self):
        return self.__user

    def __repr__(self):
        return "System({})".format(
            ",\n       ".join(["{}={}".format(n, v) for n, v in (("api_access_token", self.__api_access_token),
                                                                 ("api_endpoint", self.__api_endpoint),
                                                                 ("application", self.__application),
                                                                 ("device", self.__device),
                                                                 ("user", self.__user))])
        )


class Context(object):

    def __init__(self, json):
        self.__system = System(json['System'])
        self.__audio_player = None
        if 'AudioPlayer' in json:
            self.__audio_player = AudioPlayer(json['AudioPlayer'])

    @property
    def system(self):
        return self.__system

    @property
    def audio_player(self):
        return self.__audio_player

    def __repr__(self):
        return "Context({})".format(
            ",\n        ".join(["{}={}".format(n, v) for n, v in (("system", self.__system),
                                                                  ("audio_player", self.__audio_player))])
        )


class Request(object):

    def __init__(self, json):
        self.__type = json['type']
        self.__timestamp = json['timestamp']
        self.__request_id = json['requestId']
        self.__locale = json['locale']
        self.__json = json

    @property
    def type(self):
        return self.__type

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def request_id(self):
        return self.__request_id

    @property
    def locale(self):
        return self.__locale

    @property
    def json(self):
        return self.__json

    @classmethod
    def for_request(cls, json):
        tgt = cls._find_subclass(json.get('type', None))
        if not tgt:
            tgt = cls
        return tgt(json)

    @classmethod
    def _find_subclass(cls, name):
        if cls.__name__ == name:
            return cls
        for subclass in cls.__subclasses__():
            result = subclass._find_subclass(name)
            if result:
                return result
        return None


class LaunchRequest(Request):
    pass


class SessionEndedError(object):

    def __init__(self, json):
        self.__type = SessionEndedErrorType(json['type'])
        self.__message = json['message']

    @property
    def type(self):
        return self.__type

    @property
    def message(self):
        return self.__message


class SessionEndedRequest(Request):

    def __init__(self, json):
        super(SessionEndedRequest, self).__init__(json)
        self.__reason = SessionEndedReason(json['reason'])
        self.__error = None
        if 'error' in json:
            self.__error = SessionEndedError(json['error'])

    @property
    def reason(self):
        return self.__reason

    @property
    def error(self):
        return self.__error


class RequestBody(object):

    def __init__(self, json):
        self.__version = json["version"]
        self.__session = Session(json["session"]) if "session" in json else None
        self.__context = Context(json["context"])
        self.__request = Request.for_request(json["request"])

    @property
    def version(self):
        return self.__version

    @property
    def session(self):
        return self.__session

    @property
    def context(self):
        return self.__context

    @property
    def request(self):
        return self.__request

    def __repr__(self):
        return "Request({})".format(
            ",\n        ".join(["{}={}".format(n, v) for n, v in (("version", self.__version),
                                                                  ("session", self.__session),
                                                                  ("context", self.__context),
                                                                  ("request", self.__request))])
        )
