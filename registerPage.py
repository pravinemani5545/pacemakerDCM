from tkinter import *

# file address storing user login information
user_data_file = "user_data.txt"

class registerPage:

    def __init__(self, parent, *args, **kwargs):
        self.register = parent
        self.register.title("Register New User")
        self.register.geometry("500x500")

        user = StringVar()
        password = StringVar()

        Label(self.register, text="Create New Account", font=("Bahnschrift", 24)).grid(row=0, column=0, padx=120, pady=10,
                                                                            columnspan=2)

        Label(self.register, text="Username:").grid(row=1, column=0, pady=10)
        enter_user = Entry(self.register, textvariable=user)
        enter_user.grid(row=1, column=1)

        Label(self.register, text="Password:").grid(row=2, column=0, pady=10)
        enter_pass = Entry(self.register, textvariable=password)
        enter_pass.grid(row=2, column=1)

        Button(self.register, text="Register", padx=20, pady=10, command= lambda: self.register_new_user(user, password)).grid(row=3, column=0, pady=20,
                                                                                            columnspan=2)
        Button(self.register, text="Return to Menu", padx=20, pady=10, command=self.register.destroy).grid(row=5, column=0, pady=20,
                                                                                                columnspan=2)

    def register_new_user(self, username, password):
        verifyUsers, user_count = self.check_user_limit()
        veryifyNewAccount = self.check_new_account(username, password)

        # write data to file  
        if verifyUsers and veryifyNewAccount == 6:
            # update user_count and restore previous data to file
            file = open(user_data_file, "r")
            data = file.readlines()
            data[0] = str(user_count) + "\n"
            file.close()

            file = open(user_data_file, "w")
            file.writelines(data)
            file.close()

            # append new data to file
            file = open(user_data_file, "a")
            file.write(username.get() + "," + password.get() + "\n")
            file.close()

            Label(self.register, text="                 Registration Success                 ", font=("Calibri", 24), fg="green").grid(row=4, column=0,
                                                                                                columnspan=2)
        elif verifyUsers == False:
            Label(self.register, text="Registration Failed: Number of Users Exceeded Limit", font=("Calibri", 16),
                fg="red").grid(row=4, column=0, columnspan=2)

        elif veryifyNewAccount == 1:
            Label(self.register, text="Registration Failed: User Already Registered", font=("Calibri", 18),
                fg="red").grid(row=4, column=0, columnspan=2)

        elif veryifyNewAccount == 2:
            Label(self.register, text="Registration Failed: Username cannot be empty", font=("Calibri", 18),
                fg="red").grid(row=4, column=0, columnspan=2)

        elif veryifyNewAccount == 3:
            Label(self.register, text="Registration Failed: Username cannot contain commas", font=("Calibri", 18),
                fg="red").grid(row=4, column=0, columnspan=2)

        elif veryifyNewAccount == 4:
            Label(self.register, text="Registration Failed: Password cannot be empty", font=("Calibri", 18),
                fg="red").grid(row=4, column=0, columnspan=2)

        elif veryifyNewAccount == 5:
            Label(self.register, text="Registration Failed: Password cannot contain commas", font=("Calibri", 18),
                fg="red").grid(row=4, column=0, columnspan=2)

    def check_user_limit(self):
            user_count = 0

            # get latest user_count from first line in file
            file = open(user_data_file, "r")
            user_count = int(file.readline())
            file.close()

            if user_count == 10:
                return False, user_count
            else:
                user_count = user_count + 1
                return True, user_count
            
    def check_new_account(self, username, password):

        file = open(user_data_file, "r")
        data = file.readlines()
        file.close()

        for users in data[1:]:
            if(users.split(',')[0] == username.get()):
                return 1
            if(username.get() == ""):
                return 2
            if (username.get() == ","):
                return 3
            if(password.get() == ""):
                return 4
            if (password.get() == ","):
                return 5

        # if user registration info is valid
        return 6
