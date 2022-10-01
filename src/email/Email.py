import abc
import email
from typing import List, Dict, TypedDict
from .Base import Email, Singleton


class EmailWarehouse(Singleton):

    def __init__(self, email_reading_strategy: "EmailReadingStrategy"):
        self.emails: List[Email] = []
        self._email_reading_strategy = email_reading_strategy


    @property
    def email_reading_strategy(self) -> "EmailReadingStrategy":
        return self._email_reading_strategy


    @email_reading_strategy.setter
    def email_reading_strategy(self, email_reading_strategy: "EmailReadingStrategy") -> None:
        self._email_reading_strategy = email_reading_strategy

    def add_email(self, payload):
        self.emails.append(self.email_reading_strategy.read_email(payload))


class EmailReadingStrategy(abc.ABC, type(Singleton)):
    @abc.abstractmethod
    def read_email(self, payload: str) -> dict:
        raise NotImplementedError


class PlainTextStrategy(EmailReadingStrategy):
    def read_email(self, paylaod:str) -> dict:
        pass
