import os
import threading
import multiprocessing
from typing import List, Dict
from itertools import islice
from email.message import Message

from .EmailDatabase import EmailDatabase

class EmailPipeline:
    def __init__(self, steps: tuple) -> None:
        self.steps = steps

    def _iter(self):
        stop = len(self.steps)
        for idx, (name, trans) in enumerate(islice(self.steps, 0, stop)):
            yield idx, name, trans
    
    def __len__(self):
        return len(self.steps)

    def extract_transform_store(self, src: List[Dict], dest: EmailDatabase) -> None:
        self.steps = list(self.steps)
        for step_idx, name, transformer in self._iter():
            if transformer is None:
                continue
            processed = transformer.transform(src)
        dest.append(processed)
        


