import abc
from typing import List, TypedDict

class Singleton(abc.ABC):
    __instance = None

    @classmethod
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance


class Email(TypedDict):
    con_type: str
    subj: str
    src: str
    dests: List[str]
    body: str
    sig: str
