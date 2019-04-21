from lambdaskill2.enums import DialogState, StrEnum


class DialogDirectiveType(StrEnum):
    CONFIRM_INTENT = 'Dialog.ConfirmIntent'
    CONFIRM_SLOT = 'Dialog.ConfirmSlot'
    DELEGATE = 'Dialog.Delegate'
    ELICIT_SLOT = 'Dialog.ElicitSlot'


class DialogDirective(object):

    def __init__(self, type_, updated_intent):
        self.__type = DialogDirectiveType(type_)
        self.__updated_intent = updated_intent

    def prepare(self):
        return {'type': str(self.__type),
                'updatedIntent': self.__updated_intent.prepare()}


class DelegateDialogDirective(DialogDirective):

    def __init__(self, updated_intent):
        super(DelegateDialogDirective, self).__init__(type_=DialogDirectiveType.DELEGATE,
                                                      updated_intent=updated_intent)


class ElicitSlotDialogDirective(DialogDirective):

    def __init__(self, updated_intent, slot_to_elicit):
        super(ElicitSlotDialogDirective, self).__init__(type_=DialogDirectiveType.ELICIT_SLOT,
                                                        updated_intent=updated_intent)
        self.__slot_to_elicit = slot_to_elicit

    def prepare(self):
        container = super(ElicitSlotDialogDirective, self).prepare()
        container['slotToElicit'] = self.__slot_to_elicit
        return container


class ConfirmSlotDialogDirective(DialogDirective):

    def __init__(self, updated_intent, slot_to_confirm):
        super(ConfirmSlotDialogDirective, self).__init__(type_=DialogDirectiveType.CONFIRM_SLOT,
                                                         updated_intent=updated_intent)
        self.__slot_to_confirm = slot_to_confirm

    def prepare(self):
        container = super(ConfirmSlotDialogDirective, self).prepare()
        container['slotToConfirm'] = self.__slot_to_confirm
        return container


class ConfirmIntentDialogDirective(DialogDirective):

    def __init__(self, updated_intent):
        super(ConfirmIntentDialogDirective, self).__init__(type_=DialogDirectiveType.CONFIRM_INTENT,
                                                           updated_intent=updated_intent)

