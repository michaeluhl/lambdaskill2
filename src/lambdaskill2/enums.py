import enum


class StrEnum(enum.Enum):

    def __str__(self):
        return str(self.value)


class CardType(StrEnum):
    ASK_FOR_PERMISSIONS_CONSENT = "AskForPermissionsConsent"
    LINK_ACCOUNT = "LinkAccount"
    SIMPLE = "Simple"
    STANDARD = "Standard"


class ConfirmationStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"
    NONE = "NONE"


class DialogState(StrEnum):
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    STARTED = "STARTED"


class OutputTextType(StrEnum):
    PLAIN_TEXT = "PlainText"
    SSML = "SSML"


class PlayerActivity(StrEnum):
    IDLE = "IDLE"
    PAUSED = "PAUSED"
    PLAYING = "PLAYING"
    BUFFER_UNDERRUN = "BUFFER_UNDERRUN"
    FINISHED = "FINISHED"
    STOPPED = "STOPPED"


class PlayBehavior(StrEnum):
    ENQUEUE = "ENQUEUE"
    REPLACE_ALL = "REPLACE_ALL"
    REPLACE_ENQUEUED = "REPLACE_ENQUEUED"


class ResolutionStatus(StrEnum):
    ER_ERROR_EXCEPTION = "ER_ERROR_EXCEPTION"
    ER_ERROR_TIMEOUT = "ER_ERROR_TIMEOUT"
    ER_SUCCESS_MATCH = "ER_SUCCESS_MATCH"
    ER_SUCCESS_NO_MATCH = "ER_SUCCESS_NO_MATCH"


class SessionEndedReason(StrEnum):
    USER_INITIATED = "USER_INITIATED"
    ERROR = "ERROR"
    EXCEEDED_MAX_REPROMPTS = "EXCEEDED_MAX_REPROMPTS"


class SessionEndedErrorType(StrEnum):
    INVALID_RESPONSE = "INVALID_RESPONSE"
    DEVICE_COMMUNICATION_ERROR = "DEVICE_COMMUNICATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"

