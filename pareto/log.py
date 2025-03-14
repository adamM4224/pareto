

def getLogger(fname):
    logger = MyLogger(fname)
    return logger

class MyLogger:
    def __init__(
            self, 
            fname,
            open_with="w"
        ):
        self.fname = fname 
        with open(self.fname, open_with):
            pass
    
    def info(self, message):
        with open(self.fname, 'a') as f:
            f.write(f"{message}\n")
