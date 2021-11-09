from tkinter import *
from pmParams import *
from nav import *

class DCM:
    def __init__(self, parent, *args, **kwargs):
        self.DCM = parent
        self.DCM.geometry("980x720")
        self.DCM.title("DCM")

    def frameNav(self):
        self.navFrm = Frame(self.DCM)
        self.nav = nav(self.DCM)

    def framePmParams(self):
        self.pmParamsFrm = Frame(self.welcome)
        self.pmParams = pmParams(self.pmParamsFrm)