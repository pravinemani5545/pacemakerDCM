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
    register.geometry("500x250")

    global user
    global password

    user = StringVar()
    password = StringVar()

    Label(register, text = "Create New Account", font=("Calibri", 24)).grid(row = 0, column = 0, padx = 140, pady = 10, columnspan = 2)

    Label(register, text = "Username:").grid(row = 1, column = 0, pady = 10)
    enter_user = Entry(register, textvariable = user)
    enter_user.grid(row = 1, column = 1)

    Label(register, text = "Password:").grid(row = 2, column = 0, pady = 10)
    enter_pass = Entry(register, textvariable = password)
    enter_pass.grid(row = 2, column = 1)

    Button(register, text = "Register", padx = 20, pady = 10,command = register_new_user).grid(row = 3, column = 0, pady = 20, columnspan = 2)

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

def welcome_page():
    global welcome
    welcome =  Tk()
    welcome.geometry("500x500")
    welcome.title("Welcome to DCM")

    Label(text="Pacemaker DCM", font=("Calibri", 24), justify = CENTER).grid(row = 0, column = 0, padx = 140)
    Label(text="").grid(row = 1, column = 0)
    Button(text="Login", padx = 20, pady = 10).grid(row = 2, column = 0)
    Label(text="").grid(row = 3, column = 0)
    Label(text = "Not a registered user?").grid(row = 4, column = 0)
    Button(text = "Register", padx = 20, pady = 10, command = register_page).grid(row = 5, column = 0)

    welcome.mainloop()

welcome_page()