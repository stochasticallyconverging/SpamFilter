import abc
from email.message import Message

from bs4 import BeautifulSoup

from .Base import Email


class EmailParser:
    def __init__(self, email_parsing_strategy=None):
        self._email_parsing_strategy = email_parsing_strategy
    
    @property
    def email_parsing_strategy(self) -> "EmailParsingStrategy":
        return self._email_parsing_strategy

    @email_parsing_strategy.setter
    def email_parsing_strategy(self, email_parsing_strategy: "EmailParsingStrategy") -> None:
        self._email_parsing_strategy = email_parsing_strategy
    
    def transform(self, msg: Message) -> Email:
        if self.email_parsing_strategy is None:
            raise Exception("email_parsing_strategy must be set")
        return self.email_parsing_strategy.parse_email(msg)


class EmailParsingStrategy(abc.ABC):
    @abc.abstractmethod
    def parse_email(self, email_msg: Message) -> Email:
        raise NotImplementedError


class TextHtmlStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        return Email(
            con_type=email_msg.get_content_type(), 
            body=BeautifulSoup(
                email_msg.get_payload(),
                "html.parser").get_text(strip=True)
        )


class TextPlainStrategy(EmailParsingStrategy):

    def parse_email(self, email_msg: Message) -> Email:
        return Email(
            con_type = email_msg.get_content_type(),
            body = email_msg.get_payload()
        )

class TextOtherStrategy(EmailParsingStrategy):
    def parse_email(self, email_msg: Message) -> Email:
        return Email(
            con_type = email_msg.get_content_type(),
            body = BeautifulSoup(
                email_msg.get_payload(),
                "html.parser"
            ).get_text(strip=True).replace("\n", " ").replace("\t", " ")
        )