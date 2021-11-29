
from loginPage import *
from registerPage import *
from tkinter import *

user_data_file = "user_data.txt"
user_count = 0

class welcomePage:
    def __init__(self, parent, *args, **kwargs):
        
        self.welcome = parent
        #tk.Frame(self.parent)

        self.welcome.geometry("500x500")
        self.welcome.title("Login to DCM")

        Label(self.welcome,text="Pacemaker DCM", font= "Calibri" , justify=CENTER).grid(row=0, column=0, padx=140)
        Label(self.welcome,text="").grid(row=1, column=0)
        Button(self.welcome,text="Login", padx=20, pady=10, command= self.topLevelLogin).grid(row=2, column=0)
        Label(self.welcome,text="").grid(row=3, column=0)
        Label(self.welcome,text="Not a registered user?").grid(row=4, column=0, pady = 10)
        Button(self.welcome,text="Register", padx=20, pady=10, command = self.topLevelRegister).grid(row=5, column=0)
        Label(self.welcome,text="", pady=100).grid(row=6, column=0)
        Button(self.welcome,text="Quit", padx=20, pady=10, command= self.welcome.destroy).grid(row=6, column=0)

        self.welcome.mainloop()

    def topLevelRegister(self):
        self.registerPg = Toplevel(self.welcome)
        self.registerWindow = registerPage(self.registerPg, self.welcome)

    def topLevelLogin(self):
        self.loginPg = Toplevel(self.welcome)
        self.LoginWindow = loginPage(self.loginPg, self.welcome)
        

def main(): 
    root = Tk()
    app = welcomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()