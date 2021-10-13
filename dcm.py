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

    screen2 = Toplevel(screen)
    screen2.title("Login")
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
            login_success()
        else:
            print("Password not Recognized")
            password_not_recognized()
    else:
        print("User not found!")
        user_not_found()

def login_success():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("DCM")
    screen3.geometry("1000x1000")

def password_not_recognized():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Error")
    screen4.geometry("200x100")
    Label(screen4, text = "Password not recognized").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "OK",  width = "20", height = "2", command = delete4).pack()


def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Error")
    screen5.geometry("200x100")
    Label(screen5, text = "User not found").pack()
    Label(screen5, text = "").pack()
    Button(screen5, text = "OK",  width = "20", height = "2", command = delete5).pack()

def delete4():
    screen4.destroy()

def delete5():
    screen5.destroy()



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


