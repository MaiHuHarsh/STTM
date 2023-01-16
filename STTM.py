import socket, base64, os, json, datetime

config = {'LOG':'.\\LOG\\'}

class ErrorManagment():
    def __init__(self):
        pass

    @staticmethod
    def LogError(error):
        with open(config['LOG']+str(datetime.datetime.now().strftime("%w%d%m%Y%H%M%S%f")+'.logfile'),'a+')as LogFile:LogFile.write(str(error))
        input("There was a error making the request, file has been logged, please said to our support email")    
        exit()

class Recv():
    socketServer = socket.socket()

    def __init__(self,port):
        if type(port) != int: 
            try:port = int(port)
            except ValueError: print("Invalid Input");input();exit()
        try: self.socketServer.bind((socket.gethostbyname(socket.gethostname()),port))
        except Exception as SocketBingingError: ErrorManagment.LogError(SocketBingingError)
        print(">>> Server is ready to recive <<<")
        print("::> Connetion Information >>> \nIP: {}\nPort: {}".format(socket.gethostbyname(socket.gethostname()), port))
        self.socketServer.listen()
        self.conn, self.addr = self.socketServer.accept()
        print('got a connetion from : {}'.format(self.addr))
        print('Starting File Recv [+]')
        self.Recv()
        print('>> File Saved')
    
    def Recv(self):
        rawFile = b''
        while True:
            rawFile+= self.conn.recv(2048)
            try: json.loads(rawFile.decode());break
            except json.JSONDecodeError: continue
        file= json.loads(rawFile.decode())
        with open(file["NAME"],'wb')as fileRecv:
            fileRecv.write(base64.b64decode(file["DATA"].encode()))




class send():
    sock = socket.socket()

    def __init__(self,ip,port):
        file = self.loadFine()
        if type(port)!=int:port=int(port)
        try:self.sock.connect((ip,port))
        except Exception as e: print('Unable to find the reciver\n{}'.format(e));input();exit()
        print('>>SendingFile<<<')
        self.sock.sendall(file)

    def loadFine(self):
        fileToTransfer =  input('>>Select File to tranfer : ').replace('"','')
        if os.path.isfile(fileToTransfer)!=True :print("The File selected was invalid");input();exit
        file = {"NAME":fileToTransfer.split('\\')[::-1][0]}
        with open(fileToTransfer,'rb')as rawFile:file['DATA'] = base64.b64encode(rawFile.read()).decode()
        return json.dumps(file).encode()



class UI():
    def __init__(self):
        print("[+][+][+] Wecome To File Share [+][+][+]")
        print('[1] Send A File\n[2] Recv A File')
        client = input('>> Please Input the numer beside to chose the opration : ')
        if client == '1':
            send(input("Please Inter the Credentials \nIP:"),input("Port:"))
        elif client == '2':
            Recv(input("Enter the port ( any number between 2000-3000 ) you want to start a server at : "))

UI()