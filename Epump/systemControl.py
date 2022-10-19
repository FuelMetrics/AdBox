import enum
import time
import random
from AdMeta import AdMeta
from PumpMeta import Pump
import FileSystem as fS
import comm


# AdMeta[8]
#making list of adverts


# MAX_NO_AD = 5
MAX_NO_PUMP = 2
TOTAL_NO_ADS = 7
SERIALNUM = 'NOSERIAL'
ads = []
pumps = []
cnt  = 0


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

def sysSetup():
    global SERIALNUM
    global ads,TOTAL_NO_ADS
    print("We are in setup")
    SERIALNUM = getserial()
    print(SERIALNUM)
    fS.load()
    for i in range(fS.config['adBox']['pump']):
        pumps.append(Pump(i))
    i = 0
    # setAttributes(self, adId, fileName, maxDisp, numWindow)
    for ad in fS.config['adBox']['ads']:
        ads.append(AdMeta(i))
        ads[i].setAttributes(ad['id'], fS.path+ad['file'], ad['maxDisplay'], ad['windowNum'])
        print(ads[i].file)
        i += 1
    comm.sock0.connect(fS.config['adBox']['port1'])
    comm.sock1.connect(fS.config['adBox']['port2'])
    TOTAL_NO_ADS =  len(ads)
    # for i in range(MAX_NO_PUMP):
    #     pumps.append(Pump(i))
    # for i in range(MAX_NO_AD + 2):
    #     ads.append(AdMeta(i))
    # setAttributes(self, AdId, fileName, maxDisp, numWindow):
    # ads[MAX_NO_AD].setAttributes('0001', fS.DEFAD0, 99, 1)
    # ads[MAX_NO_AD+1].setAttributes('0002', fS.DEFAD1, 99, 2)


window = 15
# @unique
class TransactionState(enum.Enum):
    inactive = 1
    active = 2

# @unique
class PumpState(enum.IntEnum):
    nozzleDown = 1
    nozzleUp = 2
    authorized = 3
    transBegin = 4
    transInProgress = 5
    transEnd = 6

class AdMode_1(enum.IntEnum):
    msg_1 = 1
    msg_2 = 2

class AdMode_2(enum.IntEnum):
    msg_1 = 1
    msg_2 = 2
    msg_3 = 3


def setAdMode_1(mode, tm):
    if(mode == AdMode_1.msg_1):
        if((time.time() - tm) > 5):
            mode = AdMode_1.msg_2
            tm = time.time()
    elif(mode == AdMode_1.msg_2):
        if((time.time() - tm) >window):
            mode = AdMode_1.msg_1
            tm = time.time()
    # print(mode)
    return mode, tm

def setAdmode_2(tm1, adChg):
    if adChg == 0 :
        if((time.time() - tm1)>15):
            adChg = 1
            tm1 = time.time()
    if adChg == 1:
        if((time.time() - tm1)>5):
            adChg = 0;
            tm1 = time.time()
    return tm1, adChg

def setNxtAd(prev):
    global cnt
    #checking or adds thathave no displa
    nxt = prev
    start = prev
    for ad in ads:
        if ad.maxDisplay == 0:
            comm.sendMs2(ad.indx)
        # print(f'file name {ad.file}')
        if (ad.file == fS.path or ad.file == fS.path+'None') and ad.maxDisplay != 0 and not ad.lock:
            comm.checkAd(ad.indx)
            # print("no display for ad")
    if (cnt % 20) == 0:
        n = fS.config['adBox']['adSlots'] - len(ads)
        if n > 0:
            comm.sendMs3(n)
            # print('Alomost there')
    #put function to send message to server about prev add
    # cnt = 0
    # past = prev
    # ads[prev].windowCnt += 1
    # if (ads[prev].window != ads[prev].windowCnt and ads[prev].maxDisplay > 0):
    #     print('*******************window not elapsed***************************')
    #     return prev
    # ads[prev].windowCnt = 0
    # while 1:
    #     cnt += 1
    #     nxt = 0 if nxt > (MAX_NO_AD - 1) else nxt +1
    #     if cnt > MAX_NO_AD:
    #         nxt = MAX_NO_AD
    #         if prev == nxt or ads[nxt].lock:
    #             nxt = MAX_NO_AD + 1
    #         ads[nxt].maxDisplay = 999
    #         break
    #  #   print("cnt is ",cnt)
    #    # print ("nxt is ", nxt)
    #     #print(f"maxDis ->{ads[nxt].maxDisplay} lock ->{ads[nxt].lock} prev ->{prev}  next ->{nxt}")
    #     if (ads[nxt].maxDisplay != 0 and (not ads[nxt].lock) and nxt != prev ):
    #         break
    if prev == TOTAL_NO_ADS-1:
        start = 0
    for i in range(start, TOTAL_NO_ADS):
        # print(prev,TOTAL_NO_ADS)
        # print(f'88888888-->{i}')
        if ads[i].maxDisplay>0 and i != prev and not ads[i].lock:
            nxt = i
            break
    if(ads[nxt].id[0]=='D'):
        ads[nxt].maxDisplay = 99

    # print("out of loop nxt is ", nxt)
    cnt += 1
    return nxt #MAX_NO_AD

def getPumpInfo(screen):
    t_St  = 0
    p_St = 0
    p_amt = 0
    for i in range(MAX_NO_PUMP):
     #   print("pUmp idid ", pumps[i].pumpState)
        if(pumps[i].pumpNum == screen):
            t_St = pumps[i].transState
            p_St = pumps[i].pumpState
            p_amt = pumps[i].amount
           # print("found")
            break
    return t_St, p_St, p_amt

# def resetAds():
#     print('resetting ads display count')
#     for ad in ads:
#         ad.displayCount = 0

def test():
    print("we entered")
    print(pumps[0].transState)
    if (pumps[0].transState == 0):
        pumps[0].transState = 1
    if (pumps[1].transState == 0):
        pumps[1].transState = 1

    if (pumps[0].transState==1):
        pumps[0].pumpState += 1
    if  (pumps[0].transState==1):
        pumps[0].pumpState += 1

    if pumps[0].pumpState > 3:
        pumps[0].transState = 0
        pumps[0].pumpState = 0
        pumps[0].amount += 1000

    if pumps[1].pumpState > 3:
        pumps[1].transState = 0
        pumps[1].pumpState = 0
        pumps[1].amount += 1000





    # print("KOjbxhjs")
    # # global pump0.transState = 1
    # # print(pump0.pumpState)
    # if screen == 0:
    #     return  pumps[0
    # else:
    #     return pump1
    # ret = PumpInfo()
    # print(ret)
    # try:
    #     if screen == 0:
    #         print(pump0.pumpState)
    #         return pump0.pumpState, p
    #     # if screen== 1:
    #     else:
    #         print (2)
    #         return pump1
    # except:
    #     print("FAILURE")
    # return ret

# def getPumpState(screen):
#     print("here")
#     try:
#         ret = pumpState[screen]
#         print("\ngetting pumpState Success state-> ", ret)
#     except:
#         ret = pumpState[0]
#         print("\ngetting pumpState Failed state-> ", ret)
#     return ret
#
# def getTransState(screen):
#     print("There")
#     print(screen)
#     try:
#         ret = transState[screen]
#         print("\ngetting transState Success state-> ", ret)
#     except:
#         ret = transState[0]
#         print("\ngetting transState Failed state-> ", ret)
#     return ret