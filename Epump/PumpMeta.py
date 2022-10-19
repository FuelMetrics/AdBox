# class Pump:
#     def __int__(self, indx):
#         self.pumpNum = indx
#         self.transState = 0
#         self.pumpState = 0
#         self.amount = 0
#
    # def load(self, tState, pState, pAmt):
    #     self.transState = tState
    #     self.pumpState = pState
    #     self.amount = pAmt

class Pump:
    def __init__(self, i):
        print("Init")
        self.pumpNum = i
        self.transState = 0
        self.pumpState = 0
        self.amount = 0

    # def load(self, tState, pState, pAmt):
    #     self.transState = tState
    #     self.pumpState = pState
    #     self.amount = pAmt