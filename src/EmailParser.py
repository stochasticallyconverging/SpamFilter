import abc
from email.message import Message
from html.parser import HTMLParser

from .Base import Singleton, Email

EMAIL_REGEX = {"emails":"(?<name>[\\w.-]+)\\@(?<domain>[-\\w+\\.\\w+]+)(\\.\\w+)?",
               "urls_prot":"/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/",
               "url_no_prot":"/^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/"}

class EmailParser:
    def __init__(self):
        self._email_parsing_strategy = None
    
    @property
    def email_parsing_strategy(self) -> "EmailParsingStrategy":
        return self._email_parsing_strategy

    @email_parsing_strategy.setter
    def email_parsing_strategy(self, email_reading_strategy: "EmailParsingStrategy") -> None:
        self._email_reading_strategy = email_reading_strategy
    
    def transform(self, msg: Message) -> Email:
        if self.email_parsing_strategy is None:
            raise Exception("email_parsing_strategy must be set")
        return self._parse_email(msg)
    
    def _parse_email(self, msg: Message) -> Email:
        return self.email_parsing_strategy.parse_email(msg)


class EmailParsingStrategy(abc.ABC, type(Singleton)):
    @abc.abstractmethod
    def parse_email(self, email_msg: Message) -> Email:
        raise NotImplementedError


class PlainTextStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        return Email(con_type=email_msg.get_content_type(), src=None, body=email_msg.get_payload())


class TextHtmlStrategy(str):
    def parse_email(self, email_msg: Message) -> Email:
        pass

class MultipartAlternativeStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        pass

class MultipartMixedStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        pass

class MultipartRelatedStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        pass

class MultipartReportStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        pass

class MultipartSignedStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        pass
