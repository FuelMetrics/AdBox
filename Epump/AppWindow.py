import time
from random import seed, randint
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
import FileSystem as fS
import systemControl as sC
import serialComm
import comm as serverComm
from copy import deepcopy

TXTCL0 = "color: rgba(152, 110, 1, 1)"
TXTCL1 = "color: rgba(168, 71, 0, 1)"
TXTCL2 = "color: rgba(4, 98, 14, 1)"
TXTCL3 = "color: rgba(98, 4, 55, 1)"
TXTCLD = "color: rgb(64, 37, 91)"

def dykTxtSize(txt):
    cs = 78
    cl = 60
    rt = 0
    ln = len(txt)
    if ln > cl and ln < 100:
        rt = 60
    elif ln > 100 and ln < 180:
        rt = 48
    elif ln > 180:
        rt = 28
    else:
        rt = cs
    if rt < 30:
        rt = 30
    return int(rt)


class communication(QObject):
    def __init__(self):
        super().__init__()
        self.tS = 0
        self.pS = 0
        self.amt = 0

    def  commLoop(self):
        while 1:
            # print('comm loop')
            self.serialCom()
            self.serverCom()
    def serverCom(self):
        # print('we are in server comm')
        serverComm.serverComm()

    def serialCom(self):
        serialComm.read()

class App(QApplication):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comm()

    def comm(self):
        self.thread = QThread()
        self.comm = communication()
        self.comm.moveToThread(self.thread)
        self.thread.started.connect(self.comm.commLoop)
        # self.thread.started.connect(self.setSM.run)
        self.thread.started.connect(lambda: print("started Thread"))
        # self.setSM.timeout.connect(self.dykLoop)
        # self.setSM.timeout.connect(lambda: print("timeoutHappened", self.setSM.timeout.signal ) )
        self.thread.start()

class SDykSM(QObject):
    t = 5
    t_c = time.time()
    isRun = False
    timeout = pyqtSignal(int)
    t_k = 0
    out = 1
    
    def __init__(self, scrNum):
        super().__init__()
        self.scrNum = scrNum
        self.tS = 0
        self.pS = 0
        self.amt = 0
        self.out = 0

    def setTimeOut(self, tm):
        self.t = tm

    def start(self):
        # self.t_c = time.time()
        self.isRun =True

    def run(self):
        while 1:
            tS_, pS_, amt_ = sC.getPumpInfo(self.scrNum)
            if self.tS != tS_ or pS_ != self.pS :# or amt_ != self.amt:
                self.tS = tS_
                self.pS = pS_
                self.amt = amt_
                self.timeout.emit(2)

            if amt_ != self.amt:
                self.amt = amt_
                self.timeout.emit(self.out)
            
            if(time.time() - self.t_c ) > self.t and self.isRun:
                print("\ntime -> ", self.t)
                if self.t == 5:
                    self.out = 1
                    self.timeout.emit(self.out)
                    self.t = 15
                    self.t_k = 0
                elif self.t == 15:
                    self.out = 2
                    self.timeout.emit(self.out)
                    self.t = 5
                    self.t_k = 0
                    # sC.test()
                self.t_c = time.time()
            # elif (time.time() - self.t_c > self.t_k):# and self.t !=
            #         # if self.scrNum == 0:
            #         #     serComm.readLoop()
            #     self.timeout.emit(0)
            #     self.t_k += 1
            # sC.test()

    def stop(self):
        self.isRun = False



class Window(QMainWindow):
    W_X = 0
    screenCnt  = 0
    serCommFlag = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Epump"
        self.setWindowTitle(self.title)
        print("\nclass var = ", self.W_X)
        self.setGeometry(Window.W_X,0,fS.config['adBox']['windowWidth'],fS.config['adBox']['windowHeight'])
        #self.setGeometry(0,0,1960,1080)
        self.background = QLabel(self)
        self.text = QLabel(self)
        self.backPic = QPixmap()
        self.backAnim = QLabel(self)
        self.backGif0 = QMovie(fS.BACKANIM0)
        self.backGif1 = QMovie(fS.BACKANIM1)
        self.backGif2 = QMovie(fS.BACKANIM2)
        self.backGif3 = QMovie(fS.BACKANIM3)
        self.thankGif = QMovie(fS.THANKYOU)
        self.cntDwnGif = QMovie(fS.CNTDOWN)
        self.facts = []
        self.backStateDyk = 0
        self.textStateDyk = 0
        self.transState = 0
        self.adNum = 0
        Window.W_X += fS.config['adBox']['windowWidth']
        self.screenNum = Window.screenCnt
        Window.screenCnt += 1
        self.tS = 0
        self.pS = 0
        self.amt = 0
        self.p_tS = 0
        self.p_pS = 0
        self.p_amt = 0
        self.transId = ''
        self.adsDisplayCount = {a['id'] : [0, 0] for a in fS.config['adBox']['ads']}
        print(f'new dict \n{self.adsDisplayCount}')
        self.adWindowCnt = 0
        self.setupUi()

    def setupUi(self):
        # self.backAnim.setGeometry(1390,534,350,350)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignCenter)
        # self.backAnim.setMovie(self.backGif0)
        # self.backGif0.start()
        self.backPic.load(fS.BACKND)
        font = QFont('Quiet Sans', 68, QFont.Normal)
        self.text.setFont(font)
        self.text.setStyleSheet(TXTCLD)
        self.text.setText("Nozzle is down\nand ready for next\ntransaction")
        self.text.setGeometry(800, 280, 1000, 480)
        # self.text.
        # backPic2 = QPixmap('C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\Include\\back2.png')
        # backPic3 = QPixmap('C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\Include\\back3.png')
        # backPic4 = QPixmap('C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\Include\\back1.png')
        self.background.setPixmap(self.backPic.scaled(self.width(), self.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.background.setGeometry(0,0,self.width(),1080)
        self.setCentralWidget(self.background)
        self.dykSM()
        #self.resize(pixmap.width(), pixmap.height())

    def changeText(self, txt):
        self.text.setText(txt)

    def changeBackground(self, path):
        self.backPic.load(path)

    def dykLoop(self, t):
        #print("her************")
       # print("dyk state = ", t)
        #update add count dict if the length of ad dict has changed
        if len(self.adsDisplayCount) != len(fS.config['adBox']['ads']):
            print("diff in ad len reseting")
            for a in fS.config['adBox']['ads']:
                if a['id'] not in self.adsDisplayCount:
                    k = a['id']
                    self.adsDisplayCount.update({a['id']:[0,0]})
                    print(f'After updating new dict \n{self.adsDisplayCount}')
            # self.adsDisplayCount = {a['id'] : 0 for a in fS.config['adBox']['ads']}
        self.tS, self.pS, self.amt = sC.getPumpInfo(self.screenNum)
        print( "PS, TS, AMT", self.pS,self.tS, self.amt)
        print(f'p_ts->{self.p_tS} p_ps->{self.p_pS} p_amt->{self.p_amt}')
        if self.p_tS == 0:
            if self.tS == 1:
                seed(time.time())
                self.transId = '%04d'%(randint(0,9999))
                print (f'new trans id -> {self.transId}')
                # self.adsDisplayCount.
                # self.adsDisplayCount = [0 for i in self.adsDisplayCount]
        elif self.p_tS == 1:
            if self.tS == 0:
                # serverComm.sendMs3(self.screenNum, self.transId, self.p_amt)
                serverComm.sendMs1(self.screenNum, self.transId, self.adsDisplayCount, self.p_amt)
                self.pS = 4
        # if self.p_pS != 3:
        #     if self.pS == 3:
        #
        self.p_tS, self.p_pS, self.p_amt = self.tS, self.pS, self.amt
        if self.tS ==0:
            if self.pS == 4:#t == 1 and self.pS == 4:
                self.backAnim.setHidden(False)
                self.backAnim.setGeometry(914, 240, 600, 454)
                self.backAnim.setMovie(self.thankGif)
                self.thankGif.start()
                self.backPic.load(fS.BACKNT)
                font = QFont('Quiet Sans', 58, QFont.Normal)
                self.text.setFont(font)
                self.text.setText("For the patronage.")
                self.text.setGeometry(823, 660, 736, 120)
            elif t == 2:
                self.backAnim.setHidden(True)
                self.text.setHidden(False)
                self.backPic.load(fS.BACKND)
                font = QFont('Quiet Sans', 68, QFont.Normal)
                self.text.setFont(font)
                self.text.setStyleSheet(TXTCLD)
                self.text.setAlignment(Qt.AlignCenter)
                self.text.setText("Nozzle is down\nand ready for next\ntransaction.")
                self.text.setGeometry(800, 280, 1000, 480)
            elif t == 1:
                # if self.textStateDyk % 3 == 0 and self.textStateDyk != 0:
                #     self.showAd()
                # else:
                if self.backStateDyk == 3:
                    self.showAd()
                    self.backStateDyk = 0

                else :
                    self.showDYK()

        # elif ts==1:
        elif self.tS == 1:
            self.backAnim.setHidden(True)
            self.text.setHidden(False)
            self.text.setStyleSheet(TXTCLD)
            self.text.setAlignment(Qt.AlignCenter)
            # if ps == 1: #Nozzle up
            if self.pS == 1:
                self.cntDwnGif.start()
                self.cntDwnGif.setPaused(True)
                self.backPic.load(fS.BACKNU)
                font = QFont('Quiet Sans', 55, QFont.Normal)
                self.text.setFont(font)
                self.text.setText("Nozzle is lifted \npump is reseting.")
                self.text.setGeometry(860, 300, 1000, 319)
            # if ps == 2: #Transaction authotized
            elif self.pS == 2:
                self.backAnim.setHidden(False)
                self.backAnim.setGeometry(1168,505,350,350)
                self.backAnim.setMovie(self.cntDwnGif)
                if self.cntDwnGif.currentFrameNumber() == self.cntDwnGif.frameCount() - 1 :
                    self.cntDwnGif.stop()
                else:
                    self.cntDwnGif.start()
                self.backPic.load(fS.BACKNA)
                font = QFont('Quiet Sans', 48, QFont.Normal)
                self.text.setFont(font)
                self.text.setText("Pump is about to dispense.\nPlease switch of car \nengine.")
                self.text.setGeometry(760, 140, 1000, 319)
            # if ps == 3:
            elif self.pS == 3:
                if t == 2:
                    self.backPic.load(fS.BACKNP)
                    font = QFont('Digital-7', 78, QFont.Normal)
                    self.text.setFont(font)
                    self.text.setText(str(round(self.amt,2)) +' L')
                    self.text.setGeometry(1114, 480, 619, 80)
                elif t == 1:
                    if sC.ads[self.adNum].maxDisplay == 0:
                        self.showAd(nxt=True)
                        self.adWindowCnt = 0
                    elif self.adWindowCnt >= sC.ads[self.adNum].window:
                        self.adsDisplayCount[sC.ads[self.adNum].id][0] += 1
                        self.adsDisplayCount[sC.ads[self.adNum].id][1] = sC.ads[self.adNum].maxDisplay
                        sC.ads[self.adNum].maxDisplay -= 1
                        # serverComm.sendMs1(self.screenNum, self.adNum, self.transId, self.adsDisplayCount)
                        self.showAd(nxt=True)
                        self.adWindowCnt = 0
                    else:
                        self.showAd(nxt=False)
                        print('*******************window not elapsed***************************')
                    self.adWindowCnt += 1
        self.background.setPixmap(
            self.backPic.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


        # self.readSerial()



    def dykSM(self):
        self.thread = QThread()
        self.setSM = SDykSM(self.screenNum)
        self.setSM.moveToThread(self.thread)
        self.thread.started.connect(self.setSM.start)
        self.thread.started.connect(self.setSM.run)
        self.thread.started.connect(lambda: print("started Thread"))
        self.setSM.timeout.connect(self.dykLoop)
        # self.setSM.timeout.connect(lambda: print("timeoutHappened", self.setSM.timeout.signal ) )
        self.thread.start()

    def showAd(self, nxt=True):
        self.backAnim.setHidden(True)
        self.text.setHidden(True)
        if nxt :
            self.adNum = sC.setNxtAd(self.adNum)
        print ("**************ad Num is *****************************", self.adNum)
        print(sC.ads[self.adNum].file)
        self.backPic.load(sC.ads[self.adNum].file)
        self.background.setPixmap(
                self.backPic.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # if(self.transState == 1):
        #     sC.ads[self.adNum].maxDisplay -= 1

    def showDYK(self):
        self.backAnim.setHidden(False)
        self.text.setHidden(False)
        self.text.setGeometry(218, 116, 1400, 550)
        self.backAnim.setGeometry(1340, 634, 350, 350)
        self.text.setAlignment(Qt.AlignLeft)
        # font = QFont('Quiet Sans', 78, QFont.Bold)
        # self.text.setFont(font)
        # print("\nbackStateDyk = ", self.backStateDyk)
        if (self.backStateDyk == 0):
            self.text.setStyleSheet(TXTCL0)
            self.backPic.load(fS.BACKPIC0)
            self.backAnim.setMovie(self.backGif0)
            self.backGif0.start()
        elif (self.backStateDyk == 1):
            self.text.setStyleSheet(TXTCL1)
            self.backPic.load(fS.BACKPIC1)
            self.backAnim.setMovie(self.backGif1)
            self.backGif1.start()
        elif (self.backStateDyk == 2):
            self.text.setStyleSheet(TXTCL2)
            self.backPic.load(fS.BACKPIC2)
            self.backAnim.setMovie(self.backGif2)
            self.backGif2.start()
        elif (self.backStateDyk == 3):
            self.text.setStyleSheet(TXTCL3)
            self.backPic.load(fS.BACKPIC3)
            self.backAnim.setMovie(self.backGif3)
            self.backGif3.start()
        self.backStateDyk += 1
        if (self.textStateDyk == 0):
            self.facts = fS.loadFacts().copy()
        self.textStateDyk = 0 if self.textStateDyk == 9 else self.textStateDyk + 1
        # print("\ntextStateDyk =", self.textStateDyk)

        txt = self.facts[self.textStateDyk]
        # print(txt)
        sz = dykTxtSize(txt)
        font = QFont('Quiet Sans', sz, QFont.Bold)
        self.text.setFont(font)
        self.text.setText(self.facts[self.textStateDyk])








