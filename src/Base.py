import abc
from typing import List, TypedDict
from dataclasses import dataclass

class Singleton(abc.ABC):
    __instance = None

    @classmethod
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance


# From: https://stackoverflow.com/questions/3318625/how-to-implement-an-efficient-bidirectional-hash-table/21894086#21894086
class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)
    
    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)
    
    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)



@dataclass
class Email:
    con_type: str
    subj: str
    src: str
    body: str





