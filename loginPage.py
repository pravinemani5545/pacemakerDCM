from tkinter import *
from DCM import *
import os

user_data_file = "user_data.txt"

class loginPage:

    def __init__(self, parent, *args, **kwargs):
        self.login = parent
        self.login.title("Login")
        self.login.geometry("500x500")
        self.user_count = 0
        self.user = StringVar()
        self.password = StringVar()
        
        Label(self.login, text="Login", font=("Calibri", 24)).grid(row=0, column=0, padx=220, pady=10, columnspan=2)
        Label(self.login, text="Username:").grid(row=1, column=0, pady=10)
        enter_user = Entry(self.login, textvariable=self.user)
        enter_user.grid(row=1, column=1)

        Label(self.login, text="Password:").grid(row=2, column=0, pady=10)
        enter_pass = Entry(self.login, textvariable=self.password)
        enter_pass.grid(row=2, column=1)

        Button(self.login, text="Login", padx=20, pady=10, command= self.login_check).grid(row=3, column=0, pady=20, columnspan=2)
        Button(self.login, text="Return to Menu", padx=20, pady=10, command=self.login.destroy).grid(row=5, column=0, pady=20,
                                                                                        columnspan=2)
                                                                        
    def login_check(self):

        # import data from user_data_file
        file = open(user_data_file, "r")
        data = file.readlines()
        file.close()

        flag = 1  # to track if user was found or not
        verify = self.check_user_limit()  # get latest user_count

        message = Label(self.login, text="", font=("Calibri", 18), fg="green")
        message.grid(row=4, column=0, columnspan=2)  # initialize label

        print(self.user_count)
        for i in range(1, self.user_count):
            user_data = data[i].split(",")
            if (self.user.get() == user_data[0]):  # check to see if user is in list
                if (self.password.get() == user_data[1].strip("\n")):  # check to see if password is correct
                    message.config(text="                        Login Success                        ")
                    flag = 0
                    self.DCM_login(self.user.get())  # go to main DCM page
                else:
                    message.config(text="Login Failed: Password Not Recognized", fg="red")
                    flag = 0
                    break;

        if (flag):
            message.config(text="Login Failed: Username Not Recognized", fg="red")


    def check_user_limit(self):

        # get latest user_count from first line in file
        file = open(user_data_file, "r")
        self.user_count = int(file.readline())
        file.close()

        if self.user_count == 10:
            return False
        else:
            self.user_count = self.user_count + 1
            return True
    
    def DCM_login(self, userName):
        
        self.DCMScreen = Tk()
        self.DCMWindow = DCM(self.DCMScreen, userName)
