import datetime
import socket, os, base64, json

config ={
        'LOG':'.\\LOG\\'
    }


class Send():
    
    def __init__(self,port):
        if type(port)!=int:
            try:port=int(port)
            except ValueError: ErrorManager.ReportError('Invalid Port input', 'The Port number is suppoed to be an Integer');return
        self.ThisPC = socket.socket()
        self.Configration = (socket.gethostbyaddr(socket.gethostname()),port)
        self.ThisPC.bind(self.Configration)
    
    def StartAcceptingRequests(self):
        self.ThisPC.listen()
        self.Receiver, self.ReceiverAddr = self.ThisPC.accept()
    
    def BuildPacakgeToSend(self,file):
        if not os.path.isfile(file): ErrorManager.ReportError('Invalid File','The File Selected is invalid')
        FILE ={}
        with open(file,'rb')as TragetFileData:FILE['DATA'] = base64.b64encode(TragetFileData.read()).decode()
        FILE['FILENAME']=str(file).split('\\')[::-1][0]
        Package = json.dumps(FILE).encode()
        CONFIG = {'SIZE':len(Package)}
        return Package, CONFIG
    
    def SendFile(self,Package,CONFIG):
        try:
            self.Receiver.sendall(CONFIG)
            self.Receiver.sendAll(Package)
        except Exception as Error:
            ErrorManager.ReportLog(Error,"Shareing the CONFIG and Package")



class Recv():
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
    
    @staticmethod
    def ReportError(ErrorHeader,ErrorMsg):
        print('[-] ERROR [-] --> {}\n>>{}'.format(ErrorHeader, ErrorMsg))