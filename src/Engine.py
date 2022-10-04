import os
import glob
import email
from .EmailParser import EmailParser, TextHtmlStrategy, TextOtherStrategy, TextPlainStrategy
from .EmailDatabase import EmailDatabase, Vocab

class Engine:
    def __init__(self):
        self.strategy_pool = {"text/html": TextHtmlStrategy(), 
                              "text/plain": TextPlainStrategy(),
                              "text/other": TextOtherStrategy()}
        self.parser = EmailParser()
        self.email_db = EmailDatabase()
        self._vocab = None
    
    def run(self, data_dir, dir_names=["easy", "hard", "spam"]):
        self._read_emails(datapath=data_dir, dir_names=dir_names)
        return self.email_db.to_pandas(), Vocab(conn=self.email_db)
    
    
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
                            self.parser.email_parsing_strategy = self.strategy_pool[x.get_content_type()]
                        except KeyError:
                            self.parser.email_parsing_strategy = self.strategy_pool["text/other"]
                        spam = True if dirclass == "spam" else False
                        self.email_db.append(self.parser.transform(x),spam)


    