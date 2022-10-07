import os
import glob
import email

import pandas as pd

from .EmailParser import EmailParser, TextHtmlStrategy, TextOtherStrategy, TextPlainStrategy
from .EmailDatabase import EmailDatabase, Vocab

class Engine:
    def __init__(self):
        self._strategy_pool = {"text/html": TextHtmlStrategy(), 
                              "text/plain": TextPlainStrategy(),
                              "text/other": TextOtherStrategy()}
        self._parser = EmailParser()
        self._email_db = EmailDatabase()
    
    def run(self, data_dir, dir_names=["easy", "hard", "spam"]):
        self._read_emails(datapath=data_dir, dir_names=dir_names)
        df = self._db_to_pandas()

        return df, self._db_to_vocab(df)
    
    
    def _read_emails(self, datapath, dir_names=["easy","hard","spam"]):
        dirclasses = dict.fromkeys(dir_names, None)
        for key in dirclasses.keys():
            dirclasses[key] = glob.glob(os.path.join(datapath,key+"*/*"), recursive=True)
        
        for dirclass in dirclasses.keys():
            for file in dirclasses[dirclass]:
                with open(file, "r", encoding="latin1") as f:
                    x = email.message_from_file(f)
                    if x.get_content_maintype() == "text":
                        try:
                            self._parser.email_parsing_strategy = self._strategy_pool[x.get_content_type()]
                        except KeyError:
                            self._parser.email_parsing_strategy = self._strategy_pool["text/other"]
                        spam = True if dirclass == "spam" else False
                        self._email_db.append(self._parser.transform(x),spam)

    def _db_to_pandas(self):
        res = {"spam": self._email_db.spam, "message": []}
        for sub in self._email_db.emails:
            res["message"].append(sub.body)
        return pd.DataFrame(res)
    
    def _db_to_vocab(self, df: pd.DataFrame):
        return Vocab(df=df)


    