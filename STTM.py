import socket, base64, os, json


class Recv():
    socketServer = socket.socket()


    def __init__(self,port):
        if type(port) != int: port = int(port)
        try: self.socketServer.bind((socket.gethostbyname(socket.gethostname()),port))
        except Exception: print('>>> There was some error in building server please try again with a different port or try again later');input();exit()
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
        self.sock.send(file)


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
            send()
        elif client == '2':
            Recv()
