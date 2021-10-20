from tkinter import *
import tkinter.font as tkFont
from Pacemaker_Modes import *
import os

# IMPORTANT VARIABLES
user_data_file = "user_data.txt"
user_count = 0

# pacemaker programmable parameters
lrl_value, url_value, aa_value, apw_value, va_value, vpw_value, vrp_value, arp_value = 0, 0, 0, 0, 0, 0, 0, 0

# ONLY FOR INITIALIZING DCM, USED FOR TESTING
def erase_user_data():
    file = open(user_data_file, "w")
    file.write("0\n")
    file.close()

# REGISTRATION PAGE ====================================================================================================
def register_page():
    global register
    register = Toplevel(welcome)
    register.title("Register New User")
    register.geometry("500x500")

    global user
    global password

    user = StringVar()
    password = StringVar()

    Label(register, text="Create New Account", font=header).grid(row=0, column=0, padx=120, pady=10,
                                                                          columnspan=2)

    Label(register, text="Username:").grid(row=1, column=0, pady=10)
    enter_user = Entry(register, textvariable=user)
    enter_user.grid(row=1, column=1)

    Label(register, text="Password:").grid(row=2, column=0, pady=10)
    enter_pass = Entry(register, textvariable=password)
    enter_pass.grid(row=2, column=1)

    Button(register, text="Register", padx=20, pady=10, command=register_new_user).grid(row=3, column=0, pady=20,
                                                                                        columnspan=2)
    Button(register, text="Return to Menu", padx=20, pady=10, command=register.destroy).grid(row=5, column=0, pady=20,
                                                                                             columnspan=2)

# ADD REGISTRATION INFO TO DATA FILE
def register_new_user():
    verify = check_user_limit()

    # write data to file
    if verify:
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
        file.write(user.get() + "," + password.get() + "\n")
        file.close()

        Label(register, text="Registration Success", font=("Calibri", 24), fg="green").grid(row=4, column=0,
                                                                                            columnspan=2)
    else:
        Label(register, text="Registration Failed: Number of Users Exceeded Limit", font=("Calibri", 24),
              fg="red").grid(row=4, column=0, columnspan=2)


# CHECK TO SEE IF CURRENT USERS > USER LIMIT (10)
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

# LOGIN PAGE ===========================================================================================================
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
    Button(login, text="Return to Menu", padx=20, pady=10, command=login.destroy).grid(row=5, column=0, pady=20,
                                                                                       columnspan=2)

# CHECK TO SEE IF LOGIN DETAILS CORRECT
def login_check():
    # import data from user_data_file
    file = open(user_data_file, "r")
    data = file.readlines()
    file.close()

    flag = 1  # to track if user was found or not
    verify = check_user_limit()  # get latest user_count

    message = Label(login, text="", font=("Calibri", 24), fg="green")
    message.grid(row=4, column=0, columnspan=2)  # initialize label

    for i in range(1, user_count):
        user_data = data[i].split(",")
        if (user.get() == user_data[0]):  # check to see if user is in list
            if (password.get() == user_data[1].strip("\n")):  # check to see if password is correct
                message.config(text="                        Login Success                        ")
                flag = 0
                DCM_login()  # go to main DCM page
            else:
                message.config(text="Login Failed: Password Not Recognized", fg="red")
                flag = 0
                break;

    if (flag):
        message.config(text="Login Failed: Username Not Recognized", fg="red")

# WELCOME PAGE ============================================================================================================
def welcome_page():
    global welcome
    welcome = Tk()
    welcome.geometry("500x500")
    welcome.title("Login to DCM")

    # fonts
    header = tkFont.Font(welcome, family="Roman", size=24, weight="bold")
    print(tkFont.families())

    Label(text="Pacemaker DCM", font=header, justify=CENTER).grid(row=0, column=0, padx=140)
    Label(text="").grid(row=1, column=0)
    Button(text="Login", padx=20, pady=10, command=login_page).grid(row=2, column=0)
    Label(text="").grid(row=3, column=0)
    Label(text="Not a registered user?").grid(row=4, column=0)
    Button(text="Register", padx=20, pady=10, command=register_page).grid(row=5, column=0)
    Label(text="", pady=100).grid(row=6, column=0)
    Button(text="Quit", padx=20, pady=10, command=welcome.destroy).grid(row=6, column=0)

    welcome.mainloop()

# ACTUAL DCM ===========================================================================================================
# NAVIGATION BAR AT TOP OF WINDOW
def nav_bar():
    global nav
    nav = Frame(DCM)

    Label(nav, text="Welcome to DCM, " + user.get()).grid(row=0, column=0)
    Label(nav, text="ICON1", padx=50 ).grid(row=0, column=1)
    Label(nav, text="ICON2", padx=50).grid(row=0, column=2)
    Label(nav, text="", padx=400).grid(row=0, column=3)
    Button(nav, text="Log Out", padx=10, pady=5, command=back_to_welcome).grid(row=0, column=4)

def back_to_welcome():
    DCM.destroy()
    welcome_page()

# AOO MODE PARAMETERS
def set_mode_AOO():
    # set up AOO frame inside of pm_params frame
    mode_name.config(text="AOO")
    global AOO_mode
    AOO_mode = Frame(pm_params)

    # forget previous mode frame and set this as new one
    global mode_frame
    mode_frame.grid_forget()
    mode_frame = AOO_mode
    mode_frame.grid(row=1, column=0, columnspan=2)

    # parameters for this mode to be modified
    global lrl_value, url_value, aa_value, apw_value
    lrl_value = StringVar()
    url_value = StringVar()
    aa_value = StringVar()
    apw_value = StringVar()

    Label(AOO_mode, text="Lower Rate Limit: ").grid(row=1, column=0, padx=100)
    enter_lrl = Entry(AOO_mode, textvariable = lrl_value).grid(row=1, column=1)

    Label(AOO_mode, text="Upper Rate Limit: ").grid(row=2, column=0)
    enter_url = Entry(AOO_mode, textvariable=url_value).grid(row=2, column=1)

    Label(AOO_mode, text="Atrial Amplitude: ").grid(row=3, column=0)
    enter_aa = Entry(AOO_mode, textvariable=aa_value).grid(row=3, column=1)

    Label(AOO_mode, text="Atrial Pulse Width: ").grid(row=4, column=0)
    enter_apw = Entry(AOO_mode, textvariable=apw_value).grid(row=4, column=1)

    Button(AOO_mode, text="Update", padx=20, pady=10, command=send_AOO).grid(row=5, columnspan=2)

def send_AOO():
    mode = AOO()

    message = Label(AOO_mode, text="                                                         ", font=("Calibri", 24), fg="green")
    message.grid(row=6, column=0, columnspan=2)

    # make sure values entered are valid
    try:
        int(lrl_value.get())
        int(url_value.get())
        int(aa_value.get())
        int(apw_value.get())

        mode.set_LRL(int(lrl_value.get()))
        mode.set_URL(int(url_value.get()))
        mode.set_AA(int(aa_value.get()))
        mode.set_APW(int(apw_value.get()))
        message.config(text="                     Update Success!                     ", fg="green")

    except:
        message.config(text="Update Failed: please use integers", fg="red")

    # for testing values are correct
    print(mode.get_LRL())
    print(mode.get_URL())
    print(mode.get_AA())
    print(mode.get_APW())

def set_mode_VOO():
    mode_name.config(text="VOO")
    global VOO_mode
    VOO_mode = Frame(pm_params)

    # forget previous mode frame and set this as new one
    global mode_frame
    mode_frame.grid_forget()
    mode_frame = VOO_mode
    mode_frame.grid(row=1, column=0, columnspan=2)

    # parameters for this mode to be modified
    global lrl_value, url_value, va_value, vpw_value
    lrl_value = StringVar()
    url_value = StringVar()
    va_value = StringVar()
    vpw_value = StringVar()

    Label(VOO_mode, text="Lower Rate Limit: ").grid(row=1, column=0, padx=100)
    enter_lrl = Entry(VOO_mode, textvariable=lrl_value).grid(row=1, column=1)

    Label(VOO_mode, text="Upper Rate Limit: ").grid(row=2, column=0)
    enter_url = Entry(VOO_mode, textvariable=url_value).grid(row=2, column=1)

    Label(VOO_mode, text="Atrial Amplitude: ").grid(row=3, column=0)
    enter_va = Entry(VOO_mode, textvariable=va_value).grid(row=3, column=1)

    Label(VOO_mode, text="Atrial Pulse Width: ").grid(row=4, column=0)
    enter_vpw = Entry(VOO_mode, textvariable=vpw_value).grid(row=4, column=1)

    Button(VOO_mode, text="Update", padx=20, pady=10, command=send_VOO).grid(row=5, columnspan=2)

def send_VOO():
    mode = VOO()

    message = Label(VOO_mode, text="                                                         ", font=("Calibri", 24), fg="green")
    message.grid(row=6, column=0, columnspan=2)

    # make sure values entered are valid
    try:
        int(lrl_value.get())
        int(url_value.get())
        int(va_value.get())
        int(vpw_value.get())

        mode.set_LRL(int(lrl_value.get()))
        mode.set_URL(int(url_value.get()))
        mode.set_VA(int(va_value.get()))
        mode.set_VPW(int(vpw_value.get()))
        message.config(text="                     Update Success!                     ", fg="green")

    except:
        message.config(text="Update Failed: please use integers", fg="red")

    # for testing values are correct
    print(mode.get_LRL())
    print(mode.get_URL())
    print(mode.get_VA())
    print(mode.get_VPW())

def set_mode_AAI():
    mode_name.config(text="AAI")
    global AAI_mode
    AAI_mode = Frame(pm_params)

    # forget previous mode frame and set this as new one
    global mode_frame
    mode_frame.grid_forget()
    mode_frame = AAI_mode
    mode_frame.grid(row=1, column=0, columnspan=2)

    # parameters for this mode to be modified
    global lrl_value, url_value, aa_value, apw_value, arp_value
    lrl_value = StringVar()
    url_value = StringVar()
    aa_value = StringVar()
    apw_value = StringVar()
    arp_value = StringVar()

    Label(AAI_mode, text="Lower Rate Limit: ").grid(row=1, column=0, padx=100)
    enter_lrl = Entry(AAI_mode, textvariable=lrl_value).grid(row=1, column=1)

    Label(AAI_mode, text="Upper Rate Limit: ").grid(row=2, column=0)
    enter_url = Entry(AAI_mode, textvariable=url_value).grid(row=2, column=1)

    Label(AAI_mode, text="Atrial Amplitude: ").grid(row=3, column=0)
    enter_aa = Entry(AAI_mode, textvariable=aa_value).grid(row=3, column=1)

    Label(AAI_mode, text="Atrial Pulse Width: ").grid(row=4, column=0)
    enter_apw = Entry(AAI_mode, textvariable=apw_value).grid(row=4, column=1)

    Label(AAI_mode, text="ARP: ").grid(row=5, column=0)
    enter_arp = Entry(AAI_mode, textvariable=arp_value).grid(row=5, column=1)

    Button(AAI_mode, text="Update", padx=20, pady=10, command=send_AAI).grid(row=6, columnspan=2)

def send_AAI():
    mode = AAI()

    message = Label(AAI_mode, text="                                                         ", font=("Calibri", 24), fg="green")
    message.grid(row=7, column=0, columnspan=2)

    # make sure values entered are valid
    try:
        int(lrl_value.get())
        int(url_value.get())
        int(aa_value.get())
        int(apw_value.get())
        int(arp_value.get())

        mode.set_LRL(int(lrl_value.get()))
        mode.set_URL(int(url_value.get()))
        mode.set_AA(int(aa_value.get()))
        mode.set_APW(int(apw_value.get()))
        mode.set_ARP(int(arp_value.get()))
        message.config(text="                     Update Success!                     ", fg="green")

    except:
        message.config(text="Update Failed: please use integers", fg="red")

    # for testing values are correct
    print(mode.get_LRL())
    print(mode.get_URL())
    print(mode.get_AA())
    print(mode.get_APW())
    print(mode.get_ARP())

def set_mode_VVI():
    mode_name.config(text="VVI")

    global VVI_mode
    VVI_mode = Frame(pm_params)

    # forget previous mode frame and set this as new one
    global mode_frame
    mode_frame.grid_forget()
    mode_frame = VVI_mode
    mode_frame.grid(row=1, column=0, columnspan=2)

    # parameters for this mode to be modified
    global lrl_value, url_value, va_value, vpw_value, vrp_value
    lrl_value = StringVar()
    url_value = StringVar()
    va_value = StringVar()
    vpw_value = StringVar()
    vrp_value = StringVar()

    Label(VVI_mode, text="Lower Rate Limit: ").grid(row=1, column=0, padx=50)
    enter_lrl = Entry(VVI_mode, textvariable=lrl_value).grid(row=1, column=1, padx=100)

    Label(VVI_mode, text="Upper Rate Limit: ").grid(row=2, column=0)
    enter_url = Entry(VVI_mode, textvariable=url_value).grid(row=2, column=1)

    Label(VVI_mode, text="Atrial Amplitude: ").grid(row=3, column=0)
    enter_va = Entry(VVI_mode, textvariable=va_value).grid(row=3, column=1)

    Label(VVI_mode, text="Atrial Pulse Width: ").grid(row=4, column=0)
    enter_vpw = Entry(VVI_mode, textvariable=vpw_value).grid(row=4, column=1)

    Label(VVI_mode, text="VRP: ").grid(row=5, column=0)
    enter_vrp = Entry(VVI_mode, textvariable=vrp_value).grid(row=5, column=1)

    Button(VVI_mode, text="Update", padx=20, pady=10, command=send_VVI).grid(row=6, columnspan=2)

def send_VVI():
    mode = VVI()

    message = Label(VVI_mode, text="                                                         ", font=("Calibri", 24), fg="green")
    message.grid(row=7, column=0, columnspan=2)

    # make sure values entered are valid
    try:
        int(lrl_value.get())
        int(url_value.get())
        int(va_value.get())
        int(vpw_value.get())
        int(vrp_value.get())

        mode.set_LRL(int(lrl_value.get()))
        mode.set_URL(int(url_value.get()))
        mode.set_VA(int(va_value.get()))
        mode.set_VPW(int(vpw_value.get()))
        mode.set_VRP(int(vrp_value.get()))
        message.config(text="                     Update Success!                     ", fg="green")

    except:
        message.config(text="Update Failed: please use integers", fg="red")

    # for testing values are correct
    print(mode.get_LRL())
    print(mode.get_URL())
    print(mode.get_VA())
    print(mode.get_VPW())
    print(mode.get_VRP())

# PACEMAKER PARAMETERS WINDOW
def pacemaker_parameters():
    global pm_params
    pm_params = Frame(DCM)

    # displays current mode
    global mode_name
    mode_name = Label(pm_params, text="")
    mode_name.grid(row=0, column=1)

    # initialize pacemaker mode windows
    global mode_frame
    mode_frame = Frame(pm_params)
    mode_frame.grid(row=1, column=0, columnspan=2)

    set_mode_AOO()
    set_mode_VOO()
    set_mode_AAI()
    set_mode_VVI()

    # set up menu to choose different pacemaker modes
    pm_modes = Menubutton(pm_params, text="Choose Pacing Mode", relief = GROOVE)
    pm_modes.menu = Menu(pm_modes, tearoff=0)
    pm_modes["menu"] = pm_modes.menu

    pm_modes.menu.add_command(label="AOO", command=set_mode_AOO)
    pm_modes.menu.add_command(label="VOO", command=set_mode_VOO)
    pm_modes.menu.add_command(label="AAI", command=set_mode_AAI)
    pm_modes.menu.add_command(label="VVI", command=set_mode_VVI)

    pm_modes.grid(row=0, column=0)

def DCM_login():
    global DCM
    welcome.destroy()
    DCM = Tk()
    DCM.geometry("1280x720")
    DCM.title("Welcome to DCM")

    nav_bar()
    nav.grid(row=0)

    pacemaker_parameters()
    pm_params.grid(row=1, column=0, sticky = W)

welcome_page()