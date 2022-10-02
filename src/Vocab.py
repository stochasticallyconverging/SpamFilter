from collections import Counter

import numpy as np

from .Base import bidict
from .EmailDatabase import EmailDatabase


class Vocab(bidict):

    def __init__(self, conn: EmailDatabase, *args, **kwargs):
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
        with self._conn.to_pandas() as df:
            for i in range(df.shape[0]):
                yield df.iloc[i,0].lower().split(" ")

    def _populate(self) -> None:
        for text in self._iter():
            for token in text:
                self._word_counts[token] += 1
        for idx, i in enumerate(self._word_counts):
            self[i[0]] = idx

    def encode(self, string: str, return_numpy: bool = False):
        return [self[token] if token in self.keys() else 1 for token in string.lower().split(" ")]
    
    def decode(self, integer: int, return_numpy: bool = False):
        return [self.inverse[integer] if integer in self.inverse.keys() else self.inverse[1]]
    
    def encode_to_numpy(self, string: str):
        return np.ndarray(self.encode(string))
    
    def decode_to_numpy(self, integer: int):
        return np.ndarray(self.decode(integer))
