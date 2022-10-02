from dataclasses import dataclass, asdict
from typing import List

import pandas as pd


from .Base import Email
from .Vocab import Vocab

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

    def append(self, processed_email: Email) -> None:
        self.emails.append(processed_email)
    
    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(asdict(self))
    
    def to_vocab(self) -> Vocab:
        return Vocab(conn=self)



    
    


    
    



    


