import datetime


config ={
        'LOG':'.\\LOG\\'
    }


class Send():
    def __init__(self):
        pass

class Recv():
    pass

class FileShare():
    pass

class ErrorManager():
    
    def __init__(self):pass

    @staticmethod
    def ReportLog(ErrorMsg,comment):
        NameOfLogFile = ''.join(list({
            'NAME':datetime.datetime.now().strftime("%w%d%m%Y%H%M%S%f"),
            'EXT':'.logfile'}))
        
        with open(config['LOG']+NameOfLogFile,'a+')as LogFile:LogFile.write(str(ErrorMsg),comment)
        input('There was an error during the {}, the error has been logged... error id is {}\nHit Entere to continue'.format(comment,ErrorMsg))    
        exit()