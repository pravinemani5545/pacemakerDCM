# Use Tkinter for python 2, tkinter for python 3
#import tkinter as tk


#IGNORE FOR NOWWWW
from tkinter import *
from welcome_page import *

class mainApplication(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.welcome = welcomePage(self.root);


if __name__ == "__main__":
    root = Tk()
    mainApplication(root)
    root.mainloop()