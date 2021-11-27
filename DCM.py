from tkinter import *
from pmParams import *
from nav import *
import serial
from serialcom import *

class DCM():
    def __init__(self, parent, *args, **kwargs):
        self.DCM = parent
        self.DCM.geometry("980x720")
        self.DCM.title("DCM")
        self.ser = serialcom()

        self.navFrm = Frame(self.DCM)
        self.nav = nav(self.navFrm, self.DCM, args[0], self.ser)

        self.pmParamsFrm = Frame(self.DCM)
        self.pmParams = pmParams(self.pmParamsFrm, args[0], self.ser)

def main(): 
    root = Tk()
    app = DCM(root)
    root.mainloop()

if __name__ == "__main__":
    main()