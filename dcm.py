from tkinter import *
import os

def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("500x500")

    global username
    global password
    global user_Entry
    global pass_Entry
    
    username = StringVar()
    password = StringVar()
    
    Label(screen1, text = "Please enter details below").pack()
    Label(screen1,text = "").pack()
    Label(screen1, text = "Username").pack()
    user_Entry = Entry(screen1, textvariable = username)
    user_Entry.pack()
    Label(screen1, text = "Password").pack()
    pass_Entry = Entry(screen1, textvariable = password)
    pass_Entry.pack()
    Label(screen1,text = "").pack()
    Button(screen1, text = "Register",  width = "20", height = "2", command = register_user).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info+"\n")
    file.write(password_info)
    file.close

    user_Entry.delete(0, END)
    pass_Entry.delete(0, END)

    Label(screen1, text = "Registration Success", width = "200", height = "3", font = ("Calibri", 24), fg = "green").pack()


def login():
    global screen2
    global user_Entry2
    global pass_Entry2
    global userCheck
    global passCheck

    screen2 = Toplevel((screen))
    screen2.title = "Login"
    screen2.geometry("500x500")

    userCheck = StringVar()
    passCheck = StringVar()

    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Username").pack()
    user_Entry2 = Entry(screen2, textvariable = userCheck)
    user_Entry2.pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Password").pack()
    pass_Entry2 = Entry(screen2, textvariable = passCheck)
    pass_Entry2.pack()
    Label(screen2, text = "").pack()

    Button(screen2, text = "Login",  width = "20", height = "2", command = login_user).pack()

def login_user():

    username_info = userCheck.get()
    password_info = passCheck.get()

    user_Entry2.delete(0, END)
    pass_Entry2.delete(0, END)

    list_of_files = os.listdir()
    if username_info in list_of_files:
        file1 = open(username_info, "r")
        verify = file1.read().splitlines()
        if password_info in verify:
            print("Login Success")
        else:
            print("Password not Recognized")
    else:
        print("User not found!")


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("500x500")
    screen.title("Pacemaker DCM Login/Register")
    Label(text = "Pacemaker DCM", width = "200", height = "3", font = ("Calibri", 24)).pack()
    Label(text = "").pack()
    Button(text = "Login",  width = "30", height = "2", command = login).pack()
    Label(text = "").pack()
    Button(text = "Register",  width = "30", height = "2", command = register).pack()

    screen.mainloop()


main_screen()


