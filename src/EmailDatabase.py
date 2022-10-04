from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import pdb


import pandas as pd


from .Base import Email, bidict


class Vocab(bidict):

    def __init__(self, conn, *args, **kwargs):
        super(Vocab, self).__init__(*args, **kwargs)
        self._word_counts = Counter({"<pad>":10000001,"<unk>":1000000})
        self._conn = conn
        self._populate()

    @property
    def word_counts(self):
        return self._word_counts

    def most_common(self, *args, **kwargs):
        return self._word_counts.most_common(*args, **kwargs)

    def _iter(self):
        df = self._conn.to_pandas()
        for i in range(df.shape[0]):
            yield df.iloc[i,1].lower().split(" ")

    def _populate(self) -> None:
        for text in self._iter():
            for token in text:
                self._word_counts[token] += 1
        for idx, i in enumerate(self._word_counts):
            self.update({i:idx})

    def encode(self, string: str):
        return [self[token] if token in self.keys() else 1 for token in string.lower().split(" ")]
    
    def decode(self, integer: int):
        return [self.inverse[integer] if integer in self.inverse.keys() else self.inverse[1]]


class EmailDatabase:
    def __init__(self):
        self.emails = []
        self.spam = []

    def append(self, processed_email: Email, spam: bool) -> None:
        self.emails.append(processed_email)
        self.spam.append(spam)
    
    def to_pandas(self) -> pd.DataFrame:
        res = {"spam": self.spam, "message": []}
        for sub in self.emails:
            res["message"].append(sub.body)
        return pd.DataFrame(res)

    
    def to_vocab(self) -> Vocab:
        return Vocab(conn=self)
    


    
    



    


