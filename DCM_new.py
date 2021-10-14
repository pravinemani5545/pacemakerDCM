from tkinter import *
import os

# GONNA COPY THIS OVER ONCE LOGIN PART IS DONE AS WELL
user_data_file = "user_data.txt"
user_count = 0

# ONLY FOR INITIALIZING DCM, USED FOR TESTING
def erase_user_data():
    file = open(user_data_file, "w")
    file.write("0\n")
    file.close()

# SET UP REGISTRATION PAGE
def register_page():
    global register
    register = Toplevel(welcome)
    register.title("Register New User")
    register.geometry("500x500")

    global user
    global password

    user = StringVar()
    password = StringVar()

    Label(register, text = "Create New Account", font=("Calibri", 24)).grid(row = 0, column = 0, padx = 120, pady = 10, columnspan = 2)

    Label(register, text = "Username:").grid(row = 1, column = 0, pady = 10)
    enter_user = Entry(register, textvariable = user)
    enter_user.grid(row = 1, column = 1)

    Label(register, text = "Password:").grid(row = 2, column = 0, pady = 10)
    enter_pass = Entry(register, textvariable = password)
    enter_pass.grid(row = 2, column = 1)

    Button(register, text = "Register", padx = 20, pady = 10, command = register_new_user).grid(row = 3, column = 0, pady = 20, columnspan = 2)
    Button(register, text = "Return to Menu", padx = 20, pady = 10, command = register.destroy).grid(row = 5, column = 0, pady = 20, columnspan = 2)

# add new info to login data file
def register_new_user():
    verify = check_user_limit()

    # write data to file
    if verify:
        # update user_count and restore rest of data to file
        file = open(user_data_file, "r")
        data = file.readlines()
        data[0] = str(user_count) + "\n"
        file.close()

        file = open(user_data_file, "w")
        file.writelines(data)
        file.close()

        # append new data to file
        file = open(user_data_file, "a")
        file.write(user.get() + "," + password.get() + "\n")
        file.close()
		
        Label(register, text="Registration Success", font=("Calibri", 24), fg="green").grid(row=4, column=0, columnspan=2)

    else:
        Label(register, text="Registration Failed: Number of Users Exceeded Limit", font=("Calibri", 24), fg="red").grid(row=4, column=0, columnspan=2)

# checks to see if amount of users logged !> maximum
def check_user_limit():
    global user_count

    # get latest user_count from first line in file
    file = open(user_data_file, "r")
    user_count = int(file.readline())
    file.close()

    if user_count == 10:
        return False
    else:
        user_count = user_count + 1
        return True

# SET UP LOGIN PAGE ====================================================================================================
def login_page():
    global login
    login = Toplevel(welcome)
    login.title("Login")
    login.geometry("500x500")

    global user
    global password

    user = StringVar()
    password = StringVar()

    Label(login, text="Login", font=("Calibri", 24)).grid(row=0, column=0, padx=220, pady=10, columnspan=2)
    Label(login, text="Username:").grid(row=1, column=0, pady=10)
    enter_user = Entry(login, textvariable=user)
    enter_user.grid(row=1, column=1)

    Label(login, text="Password:").grid(row=2, column=0, pady=10)
    enter_pass = Entry(login, textvariable=password)
    enter_pass.grid(row=2, column=1)

    Button(login, text="Login", padx=20, pady=10, command=login_check).grid(row=3, column=0, pady=20, columnspan=2)
    Button(login, text="Return to Menu", padx=20, pady=10, command = login.destroy).grid(row=5, column=0, pady=20, columnspan=2)

# check to see if login details are correct
def login_check():
    # import data from user_data_file
    file = open(user_data_file, "r")
    data = file.readlines()
    file.close()

    flag = 1 # to track if user was found or not
    verify = check_user_limit() # get latest user_count

    message = Label(login, text="", font=("Calibri", 24), fg="green")
    message.grid(row=4, column=0, columnspan=2) # initialize label

    for i in range(1, user_count):
        user_data = data[i].split(",")
        if (user.get() == user_data[0]):    # check to see if user is in list
            if(password.get() == user_data[1].strip("\n")): # check to see if password is correct
                message.config(text="                        Login Success                        ")
                flag = 0
                login_success() # WELCOME PAGE
            else:
                message.config(text="Login Failed: Password Not Recognized", fg="red")
                flag = 0
                break;

    if (flag):
        message.config(text="Login Failed: Username Not Recognized", fg="red")

# TRANSFER FROM LOGIN PAGE TO ACTUAL DCM PAGE (in progress...)
def login_success():
    global screen3
    welcome.destroy()
    screen3 = Tk()
    screen3.geometry("1000x1000")
    screen3.title("DCM")

# MAIN PAGE ============================================================================================================
def welcome_page():
    global welcome
    welcome =  Tk()
    welcome.geometry("500x500")
    welcome.title("Welcome to DCM")

    Label(text="Pacemaker DCM", font=("Calibri", 24), justify = CENTER).grid(row = 0, column = 0, padx = 140)
    Label(text="").grid(row = 1, column = 0)
    Button(text="Login", padx = 20, pady = 10, command = login_page).grid(row = 2, column = 0)
    Label(text="").grid(row = 3, column = 0)
    Label(text = "Not a registered user?").grid(row = 4, column = 0)
    Button(text = "Register", padx = 20, pady = 10, command = register_page).grid(row = 5, column = 0)

    welcome.mainloop()

erase_user_data()
welcome_page()