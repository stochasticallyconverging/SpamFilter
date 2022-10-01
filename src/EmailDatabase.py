import abc
import email
from email.message import Message
from dataclasses import dataclass, asdict
from typing import List, Dict, TypedDict

import pandas as pd


from .Base import Email, Singleton

'''
{
 'multipart/alternative',
 'multipart/mixed',
 'multipart/related',
 'multipart/report',
 'multipart/signed',
 
 'text/html',
 'text/plain',
 'text/plain charset=us-ascii'}
'''

@dataclass
class EmailDatabase:
    emails: List[Email]

    def append(self, processed_email):
        self.emails.append(processed_email)

    def to_pandas(self):
        return pd.DataFrame(asdict(self))
    
    def __str__(self):
        pass

    
    



    


