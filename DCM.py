from pmParams import *
from nav import *

class DCM():
    def __init__(self, parent, *args, **kwargs):
        DCM = parent
        DCM.geometry("980x720")
        DCM.title("DCM")

        navFrm = Frame(DCM)
        navWnd = nav(navFrm, DCM, args[0])

        pmParamsFrm = Frame(DCM)
        pmParamsWnd = pmParams(pmParamsFrm, args[0])