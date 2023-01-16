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
        self.Configration = (socket.gethostbyname(socket.gethostname()),port)
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

        CONFIG = json.dumps({'SIZE':len(Package)}).encode()
        if len(CONFIG) >2048:  ErrorManager.ReportWarning("To Large File","The File is To large to be send, our app is not cappable yet")
        
        return Package, CONFIG
    
    def SendFile(self,Package,CONFIG):
        try:
            self.Receiver.sendall(CONFIG)
            self.Receiver.sendall(Package)
        except Exception as Error:
            ErrorManager.ReportLog(Error,"Shareing the CONFIG and Package")



class Recv():
    def __init__(self,ip,port):
        self.ThisPC = socket.socket()
        if type(port) != int: ErrorManager.ReportError('Invalid Port','The port is invalid')
        try:self.ThisPC.connect((ip,port))
        except ConnectionRefusedError: ErrorManager.ReportError('Unable to make the connection','Either the info entred was wrong or the reciver is not yet ready please resolve accordingly');return
        except Exception as e: ErrorManager.ReportLog(e,'Connecting to recevier')
    
    def RecvFile(self):
        CONFIG = json.loads(self.ThisPC.recv(2048).decode())
        print('config aagay')
        rawFile = b''
        percentageReceved = 0
        while True:
            rawFile+= self.ThisPC.recv(2048)
            try: json.loads(rawFile.decode());break
            except json.JSONDecodeError: 
                percentageBuffer = round((len(rawFile)/CONFIG['SIZE'])*100,0)
                if percentageReceved != percentageBuffer:percentageReceved=percentageBuffer;print(percentageReceved)
                
        file= json.loads(rawFile.decode())
        with open(file["FILENAME"],'wb')as fileRecv:
            fileRecv.write(base64.b64decode(file["DATA"].encode()))
        
class ErrorManager():
    
    def __init__(self):pass

    @staticmethod
    def ReportLog(ErrorMsg,comment):
        NameOfLogFile = datetime.datetime.now().strftime("%w%d%m%Y%H%M%S%f")+'.logfile'
        
        with open((config['LOG']+NameOfLogFile),'a+')as LogFile: LogFile.write(str(ErrorMsg)+'\n'+comment)
        input('There was an error during the {}, the error has been logged... error id is {}\nHit Entere to continue'.format(comment,ErrorMsg))    
        exit()
    
    @staticmethod
    def ReportError(ErrorHeader,ErrorMsg):
        print('[-] ERROR [-] --> {}\n>>{}'.format(ErrorHeader, ErrorMsg))
    
    @staticmethod
    def ReportWarning(WarningHeadder,WarningMsg):
        print('[!] ERROR [!] --> {}\n>>{}'.format(WarningHeadder, WarningHeadder))