import enum

from lambdaskill2.enums import CardType, OutputTextType, PlayBehavior
from lambdaskill2.ssml import SSML


class CardImage(object):

    def __init__(self, small_image_url=None, large_image_url=None):
        self.__small_image_url = small_image_url
        self.__large_image_url = large_image_url

    def with_small_image(self, url):
        self.__small_image_url = url
        return self

    def with_large_image(self, url):
        self.__large_image_url = url
        return self

    def prepare(self):
        container = {}
        if self.__small_image_url is not None:
            container['smallImageUrl'] = self.__small_image_url
        if self.__large_image_url is not None:
            container['largeImageUrl'] = self.__large_image_url
        return container


class Card(object):

    def __init__(self, type_, title=None, content=None, text=None, image=None):
        self.__type = CardType(type_)
        self.__title = title
        self.__content = content
        self.__text = text
        self.__image = image

    def with_title(self, title):
        self.__title = title
        return self

    def with_content(self, content):
        self.__content = content
        return self

    def with_text(self, text):
        self.__text = text
        return self

    def with_image(self, image):
        self.__image = image
        return self

    def prepare(self):
        container = {'type': str(self.__type)}
        if self.__title is not None:
            container['title'] = self.__title
        if self.__content is not None and self.__type is CardType.SIMPLE:
            container['content'] = self.__content
        if self.__type is CardType.STANDARD:
            if self.__text is not None:
                container['text'] = self.__text
            if self.__image is not None:
                container['image'] = self.__image.prepare()
        return container


class OutputText(object):

    def __init__(self, content, output_type=None, play_behavior=None):
        self.__content = content
        self.__output_type = OutputTextType(output_type) if output_type else None
        if isinstance(content, SSML) and not output_type:
            self.__output_type = OutputTextType.SSML
        if not self.__output_type:
            self.__output_type = OutputTextType.PLAIN_TEXT
        self.__play_behavior = play_behavior

    def prepare(self):
        container = {'type': str(self.__output_type)}
        if self.__output_type is OutputTextType.SSML:
            container['ssml'] = str(self.__content)
        else:
            container['text'] = str(self.__content)
        if self.__play_behavior:
            container['playBehavior'] = str(self.__play_behavior)
        return container


class Response(object):

    def __init__(self, output=None, reprompt_text=None,
                 card=None, directives=None, should_end_session=None):
        if isinstance(output, OutputText) or output is None:
            self.__output = output
        else:
            self.__output = OutputText(output)
        if isinstance(reprompt_text, OutputText) or reprompt_text is None:
            self.__reprompt_text = reprompt_text
        else:
            self.__reprompt_text = OutputText(reprompt_text)
        self.__card = card
        self.__directives = []
        self.__should_end_session = should_end_session

    def add_directive(self, directive):
        self.__directives.append(directive)
        return self

    def with_output(self, output_text):
        if not isinstance(output_text, OutputText):
            output_text = OutputText(output_text)
        self.__output = output_text
        return self

    def with_reprompt(self, reprompt_text):
        if not isinstance(reprompt_text, OutputText):
            reprompt_text = OutputText(reprompt_text)
        self.__reprompt_text = reprompt_text
        return self

    def with_card(self, card):
        self.__card = card
        return self

    def prepare(self):
        container = {}
        if self.__output is not None:
            container['outputSpeech'] = self.__output.prepare()
        if self.__reprompt_text is not None:
            container['reprompt'] = {'outputSpeech': self.__reprompt_text.prepare()}
        if self.__card is not None:
            container['card'] = self.__card.prepare()
        if self.__should_end_session is not None:
            container['shouldEndSession'] = self.__should_end_session
        if self.__directives:
            container['directives'] = [d.prepare() for d in self.__directives]
        return container


class ResponseBody(object):

    def __init__(self, request=None):
        self.__version = "1.0"
        try:
            self.__session_attributes = dict(request.session.attributes)
        except AttributeError:
            self.__session_attributes = None
        self.__response = None

    def with_response(self, response):
        self.__response = response
        return self

    def prepare(self, session_attributes=None):
        container = {}
        container['version'] = self.__version
        if self.__session_attributes:
            container['sessionAttributes'] = self.__session_attributes
        if session_attributes:
            container['sessionAttributes'] = session_attributes
        if not self.__response:
            raise RuntimeError('A response object is required')
        container['response'] = self.__response.prepare()
        return container
