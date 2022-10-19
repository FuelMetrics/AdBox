import time

import select
import  socket
import random
import queue
import systemControl as sC
MSGLEN = 1024
host = "52.232.103.77"
port = 9096
readyToW = []
readyToR = []
error = []


msgResendQueue = dict()



class Socket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.msgQueue = queue.Queue(50)
        self.recvQueue = queue.Queue(50)
        self.sock.settimeout(0.1)

    def connect(self,port, host=host):
        return
        try:
            self.sock.connect((host, port))
        except:
            print(f'{__name__} socket is not active')


    def sockSend(self):
        msg = ''
        try:
            if not self.msgQueue.empty():
                msg = self.msgQueue.get(block=False)
                print(f'****sending message {msg}****')
                print(f'msg send ->{self.sock.send(msg.encode())}')
        except:
            # self.addToQueue(msg)
            print(f'{__name__} socket is not active')
        # while totalsent < MSGLEN:
        #     sent = self.sock.send(msg[totalsent:])
        #     totalsent = totalsent + sent
        # except :
        # print("retrying soc send")
        #     # self.sock.connect((host, port))
        #     self.mysend(msg)

    def receive(self):
        # print('we are in recieve')
        chunks = []
        bytes_recd = 0
        return
        try:
            while bytes_recd < MSGLEN:
                # print('we are in while')
                chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
                if chunk == b'':
                     #print("socket connection broken")
                     break
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
                # print('we are in recieve')
                print(chunk)
        except TimeoutError:
            pass
        return (b''.join(chunks)).decode()

    def addToQueue(self,msg):
        try:
            self.msgQueue.put(msg, block=False)
        except queue.Full:
            print(f'****{__name__} msg queue full****')


sock0 = Socket()
sock1 = Socket()

def sockSelect():
    readyToR_, readyToW_, error_ = select.select([sock0.sock, sock1.sock], [sock0.sock, sock1.sock], [], 60000)
    print("in sock check",readyToR_)
    readyToR = readyToR_.copy()
    readyToW = readyToW_.copy()
    error = error_.copy()



def getToken():
    random.seed(time.time())
    return random.randint(100000, 999999)

def sendMs0():
    tk = getToken()
    msg = f'm0,{sC.SERIALNUM},{round(time.time())},{tk},'
    for ad in sC.ads:
        msg += f'[{ad.id}, {ad.maxDisplay}],'
    msg = msg[:-1]
    sock0.addToQueue(msg)



def sendMs1(scrNum, transId, displayCount, transAmt):
    print('******************************Added msg 1***************************\n')
    # print(displayCount)
    tk = getToken()
    for a in displayCount.keys():
        if displayCount[a][0] == 0:
            continue
        # print(a)
        msg = f'm1,{sC.SERIALNUM},{round(time.time())},{tk},{a},{displayCount[a][1]}'  \
          f',{displayCount[a][0]},{transId},{transAmt},{scrNum}'
        print(msg)
        sock0.addToQueue(msg)

def sendMs2(adIndx):
    tk = getToken()
    msg = f'm2,{sC.SERIALNUM},{round(time.time())},{tk},{sC.ads[adIndx].id}'
    sock0.addToQueue(msg)

def sendMs3(n):
    tk = getToken()
    msg = f'm3,{sC.SERIALNUM},{round(time.time())},{tk},{n}'
    # print(msg)
    sock0.addToQueue(msg)

def checkAd(indx):
    tk = getToken()
    msg =  {"type":"checkAdvert","id":sC.SERIALNUM,"version":21005,"tk":tk,"details":sC.ads[indx].id,"ty":"AdvertBox"}
    print(msg)
    # msg = dict({'type':'checkAdvert'},{"id":sC.SERIALNUM},{"version":3000},{"tk":tk})
    sock1.addToQueue(msg)

def serverComm():
    sock0.sockSend()
    sock0.receive()
    sock1.sockSend()
    sock1.receive()

def recvHandler(msg):
    pass
