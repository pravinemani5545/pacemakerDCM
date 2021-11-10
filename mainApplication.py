# Use Tkinter for python 2, tkinter for python 3
#import tkinter as tk


#IGNORE FOR NOWWWW
from tkinter import *
from welcome_page import *

class mainApplication:

    def __init__(self, parent,  *args, **kwargs):
        self.root = parent
        self.welcome = welcomePage(self.root);


def main(): 
    root = Tk()
    app = mainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()