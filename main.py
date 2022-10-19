import sys
import time
import systemControl
import FileSystem as fS
import AppWindow as App
import serialComm as sCom
import comm
from systemControl import TransactionState as TS, PumpState as PS, AdMode_1, setAdMode_1, ads
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QWidget)
window = 15
pumpState_ = 0
adMode = AdMode_1.msg_1
adMode_ = 0

tSnap = time.time()
adChng = 0

sxd = "{\"at\":0,\"di\":\"864120050746347\",\"tk\":1656976707,\"atgs\":[88888,54563,21539,12666,21548,12683],\"bt\":4329472,\"}"
# comm.sock0.connect(comm.host, 9095)
# comm.checkAd(5)

sCom.setup()
systemControl.sysSetup()
comm.sendMs0()

app = App.App(sys.argv)
# app2 = QApplication(sys.argv)




# def serComm():
#     while 1:
#         comm.sock0.mysend('lp')
#         time.sleep(25)

# t3 = threading.Thread(target=serComm(), daemon=True)
windows = []

for i in range(fS.config['adBox']['screen']):
    windows.append(App.Window())
    windows[i].show()
# window_2 = App.Window()
# window_ = App.Window()
# window_.show()
# window_2.show()
sys.exit(app.exec())
sys.exit(app2.exec())


# comm.msgQueue.put((1, 'typ'))
# if (1, 'typ') in comm.msgQueue:
#     print("found it")
# comm.sockSelect()
# print(comm.readyToW)
# comm.sock0.mysend(sxd.encode())
# tSnap_2 = time.time()
# window = QWidget()
# window.setWindowTitle("QHBoxLayout")
#
# layout = QHBoxLayout()
# layout.addWidget(QPushButton("Left"))
# layout.addWidget(QPushButton("Center"))
# layout.addWidget(QPushButton("Right"))
# window.setLayout(layout)
# print(time.time())
# window.show()
# sys.exit(app.exec())

# configP1 = 'P1'
# configP2 = 'P2'
# def serComm():
#     # while 1:
#     comm.sock0.mysend('lp')
#     time.sleep(25)
# serComm()
# serverCom = multiprocessing.Process(target=serComm)
# serComm()
# t1 = threading.main_thread()
# t2 = threading.Thread(target=window_2.dykSM())
# t3 = threading.Thread(target=serComm(), daemon=True)
# window_.show()
# window_2.show()
# t1.start()
# t2.start()
# t3.start()
# if __name__ == '__main__':
#     # freeze_support()
#     print("called")
#     serverCom.start()
#     serverCom.join
# sCom.readLoop()



# adIndx = 0
# adChng_= -1
# factIndx = 10
#
#
# transState = TS.inactive
# pumpState = PS.transEnd
#
# #  main stateMachine
# def lopp():
#     window_.show()
#     sys.exit(app.exec())
#     global transState
#     global pumpState
#     global adMode
#     global tSnap
#     global adMode_
#     global factIndx
#     if transState == TS.inactive:
#         adMode, tSnap = setAdMode_1(adMode, tSnap)
#         if adMode != adMode_:
#             adMode_ = adMode
#         # inactive state machine
#             if adMode == AdMode_1.msg_1:
#                 print("This is Message 1")
#             elif adMode == AdMode_1.msg_2:
#                 print("This is Message 2")
#                 if factIndx == 10:
#                     FileSystem.loadFacts()
#                     factIndx = 0
#                     print(FileSystem.factList[factIndx])
#                     factIndx += 1
#                 else:
#                     print(FileSystem.factList[factIndx])
#                     factIndx += 1
#     elif transState == TS.active:
#         # if pumpState != pumpState_:
#         #     pumpState_ =pumpState
#             if pumpState == PS.nozzleUp:
#                 print("Nozzle up")
#             elif pumpState == PS.authorized:
#                 print("Authorized")
#             elif pumpState == PS.transBegin:
#                 print("Transaction About to Start")
#             elif pumpState == PS.transInProgress:
#                 tSnap, adChng= systemControl.setAdmode_2(tSnap, adChng)
#                 if adChng_ != adChng:
#                     if adChng == 0:
#                         print("chnging Ad")
#                         adIndx = systemControl.setNxtAd(adIndx)
#                     if adChng == 1:
#                         print("showing pl")
#                 adChng_ = adChng
#             elif pumpState == PS.transEnd:
#                 print("Transaction has Ended")
#                 transState = TS.inactive
#     time.sleep(1)

# t1.start()
# import sys
# from PySide6.QtGui import QPixmap, QIcon
# from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
#
# class MainWindow(QMainWindow):
#
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.title = "Image Viewer"
#         self.setWindowTitle(self.title)
#         self.setGeometry(0, 0, 1024, 600)
#         icon = QIcon("C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\Include\\Frame 102.png")
#         self.setWindowIcon(icon)
#
#         label = QLabel(self)
#         pixmap = QPixmap('..\\include\\Frame 102.png')
#         label.setPixmap(pixmap)
#         self.setCentralWidget(label)
#         # self.resize(pixmap.width(), pixmap.height())
#
#
# app = QApplication(sys.argv)
# w = MainWindow()
# w.show()
# sys.exit(app.exec())                    