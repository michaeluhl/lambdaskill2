from lambdaskill2.enums import ConfirmationStatus, DialogState, ResolutionStatus
from lambdaskill2.requests.body import Request


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

    def prepare(self):
        return {'value': {'name': self.__name, 'id': self.__id}}


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

    def prepare(self):
        return {'authority': self.__authority,
                'status': {'code': str(self.__status_code)},
                'values': [v.prepare() for v in self.__values]}


class Slot(object):

    def __init__(self, json):
        self.__name = json['name']
        self.__value = json.get('value', None)
        self.__confirmation_status = ConfirmationStatus(json['confirmationStatus'])
        self.__resolutions = None
        if 'resolutions' in json and json['resolutions']:
            self.__resolutions = [Resolution(res) for res in json['resolutions']['resolutionsPerAuthority']]

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    @property
    def confirmation_status(self):
        return self.__confirmation_status

    @confirmation_status.setter
    def confirmation_status(self, cs):
        self.__confirmation_status = ConfirmationStatus(cs)

    @property
    def resolutions(self):
        return self.__resolutions

    def __repr__(self):
        return "Slot(name='{}', value='{}')".format(self.name, self.value)

    def prepare(self):
        container = {'name': self.__name,
                     'value': self.__value,
                     'confirmationStatus': str(self.__confirmation_status)}
        if self.__resolutions is not None:
            resolutions = {'resolutionsPerAuthority': [r.prepare() for r in self.__resolutions]}
            container['resolutions'] = resolutions
        return container


class Slots(dict):

    def __init__(self, json):
        super(Slots, self).__init__()
        for name, value in json.items():
            self[name] = Slot(value)

    def prepare(self):
        return {k: v.prepare() for k, v in self.items()}


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

    @confirmation_status.setter
    def confirmation_status(self, cs):
        self.__confirmation_status = ConfirmationStatus(cs)

    @property
    def slots(self):
        return self.__slots

    def prepare(self):
        return {'name': self.__name,
                'confirmationStatus': str(self.__confirmation_status),
                'slots': self.__slots.prepare()}


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
