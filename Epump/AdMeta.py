class AdMeta:
    def __init__(self, i, maxDis = None):
        self.file=""
        self.indx = i
        self.id='Nill'
        self.window=0
        # self.windowCnt = 0
        if maxDis == None:
            self.maxDisplay=0
        else:
            self.maxDisplay = maxDis
        # self.displayCount=0
        self.lock = False

    def setFileName(self, fileName):
        self.file = fileName

    def setAdId(self, adId):
        self.id = adId

    def setMaxDisplay(self, maxDisp):
        self.maxDisplay = maxDisp

    def setWindow(self, numWindow):
        self.window = numWindow

    def setAttributes(self, adId, fileName, maxDisp, numWindow):
        self.file = fileName
        self.id = adId
        self.maxDisplay = maxDisp
        self.window = numWindow