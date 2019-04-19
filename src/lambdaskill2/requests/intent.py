import enum

from lambdaskill2.requests.body import Request


class DialogState(enum.Enum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    STARTED = "STARTED"


class ConfirmationStatus(enum.Enum):
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    NONE = "NONE"


class ResolutionStatus(enum.Enum):
    ER_ERROR_EXCEPTION = "ER_ERROR_EXCEPTION"
    ER_ERROR_TIMEOUT = "ER_ERROR_TIMEOUT"
    ER_SUCCESS_MATCH = "ER_SUCCESS_MATCH"
    ER_SUCCESS_NO_MATCH = "ER_SUCCESS_NO_MATCH"


class ResolutionValue(object):

    def __init__(self, json):
        self.__name = json['name']
        self.__id = json['id']

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id


class Resolution(object):

    def __init__(self, json):
        self.__authority = json['authority']
        self.__status_code = ResolutionStatus(json['status']['code'])
        self.__values = [ResolutionValue(value['value']) for value in json['values']]

    @property
    def authority(self):
        return self.__authority

    @property
    def status_code(self):
        return self.__status_code

    @property
    def values(self):
        return self.__values


class Slot(object):

    def __init__(self, json):
        self.__name = json['name']
        self.__value = json.get('value', None)
        self.__confirmation_status = ConfirmationStatus(json['confirmationStatus'])
        self.__resolutions = None
        if 'resolutions' in json:
            self.__resolutions = [Resolution(res) for res in json['resolutions']['resolutionsPerAuthority']]

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def confirmation_status(self):
        return self.__confirmation_status

    @property
    def resolutions(self):
        return self.__resolutions

    def __repr__(self):
        return "Slot(name='{}', value='{}')".format(self.name, self.value)


class Slots(dict):

    def __init__(self, json):
        super(Slots, self).__init__()
        for name, value in json.items():
            self[name] = Slot(value)


class Intent(object):

    def __init__(self, json):
        self.__name = json['name']
        self.__confirmation_status = ConfirmationStatus(json['confirmationStatus'])
        self.__slots = Slots(json['slots'])

    @property
    def name(self):
        return self.__name

    @property
    def confirmation_status(self):
        return self.__confirmation_status

    @property
    def slots(self):
        return self.__slots


class IntentRequest(Request):

    def __init__(self, json):
        super(IntentRequest, self).__init__(json=json)
        self.__dialog_state = None
        if 'dialogState' in json:
            self.__dialog_state = DialogState(json['dialogState'])
        self.__intent = Intent(json['intent'])

    @property
    def dialog_state(self):
        return self.__dialog_state

    @property
    def intent(self):
        return self.__intent


class CanFulfillIntentRequest(IntentRequest):
    pass
