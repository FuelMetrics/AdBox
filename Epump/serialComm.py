import time
import systemControl as sC
import serial

conSer = serial.Serial()


def setup(baudrate=None, port=None, timeout = None):
    if baudrate==None:
        conSer.baudrate=9600
    else:
        conSer.baudrate = baudrate
    if port == None:
        conSer.port = '/dev/ttyUSB0'
        # conSer.port='/dev/ttyS0'
    else:
        conSer.port = port
    if timeout == None:
        conSer.timeout=0.1
    else:
        conSer.timeout = timeout
    try:
        conSer.open()
        print("serial port open success")
    except:
        print("serial port open failed")

def decodeState():
    pass

def getPumpState(st ):
    #print("st is ", st)
  #  print(type(st))
    r_st = 0
    st = int(st)
    if st == 3:
        r_st =1
    elif st == 5:
        r_st = 2
    elif st == 6:
        r_st = 3
    elif st == 8:
        r_st = 4 # chane later
    else:
        r_st = 0
    #print("r_st is ", r_st)
    return r_st

# tstStr = 'P3:255:123:1234567:345678|P4:1:123.45:12345678.45:999.45'
tstStr = b'[86412005073881501A2:2:1:1648.18:0|A1:3:1:113.82:018]'
sxd = b''
failcnt = 0
def read():
    # global failcnt
    # while 1:
    #     print("REading")
    try:
        conSer.write(sxd)
        p = conSer.read(254)
        # p = tstStr
        print('Read syccess')
        print("p is ", p)
        if b']'  in p and b']' in p :
            p = p[p.find(b'['):p.find(b']')]
        print(p)
        #time.sleep(1)
        # print("reading from Serial")
        # t = tstStr.split('|',2)
        t = [chr(i) for i in list(p)]
        print(t)
        #t[:0] = tstStr
        if (len(t) > 5):
            t = t[18:]
            t = (''.join(t))#.split('|')
            t = t.split('|')
            print('final t is ',t)
            p0 = t[0].split(':')
            p1 = t[1].split(':')

            sC.pumps[0].pumpState = getPumpState(p0[1])
            sC.pumps[0].transState = 0 if sC.pumps[0].pumpState == 0 else  1
            sC.pumps[0].amount = float(p0[4])

            sC.pumps[1].pumpState = getPumpState(p1[1])
            sC.pumps[1].transState = 0 if sC.pumps[1].pumpState == 0 else  1
            sC.pumps[1].amount = float(p1[4])
        else:
            print("**No message")
    except:
        # print('***********************bad message*****************')
        pass
        # print('.')# += 1
        # print('#################Fail count ->  ', failcnt)
        # time.sleep(5)
   # print(f"pstate ->{sC.pumps[0].pumpState} tstate->{sC.pumps[0].transState} sAmount ->{sC.pumps[0].amount}")
 #   print(f"pstate ->{sC.pumps[1].pumpState} tstate->{sC.pumps[1].transState} sAmount ->{sC.pumps[1].amount}")
    # print(p1, p2, sep='---')
    # for i in range (3):
    #     time.sleep(5)
    #     print("reading from Serial")
#