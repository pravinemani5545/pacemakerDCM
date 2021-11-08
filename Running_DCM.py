from tkinter import *
import tkinter.font as tkFont
from Pacemaker_Modes import *
import os


#NOTES DEFINE THE SEND FUNCTIONS TRY CATCH BLOCK IN A SEPERATE FUNCTION THAT RETURNS IF CONDITIONS ARE NOT MET WITH A ERROR MSG

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

    Label(register, text="Create New Account", font=("Calibri", 24)).grid(row=0, column=0, padx=120, pady=10,
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
    verifyUsers = check_user_limit()
    veryifyNewAccount = check_new_account()

    print(veryifyNewAccount)

    # write data to file
    if verifyUsers and veryifyNewAccount:
        # update user_count and restore previous data to file
        file = open(user_data_file, "r")
        data = file.readlines()
        data[0] = str(user_count) + "\n"
        file.close()

        print(data)


        file = open(user_data_file, "w")
        file.writelines(data)
        file.close()

        # append new data to file
        file = open(user_data_file, "a")
        file.write(user.get() + "," + password.get() + "\n")
        file.close()

        Label(register, text="                 Registration Success                 ", font=("Calibri", 24), fg="green").grid(row=4, column=0,
                                                                                            columnspan=2)
    elif verifyUsers == False:
        Label(register, text="Registration Failed: Number of Users Exceeded Limit", font=("Calibri", 16),
              fg="red").grid(row=4, column=0, columnspan=2)

    elif veryifyNewAccount == False:
        Label(register, text="Registration Failed: User Already Registered", font=("Calibri", 18),
              fg="red").grid(row=4, column=0, columnspan=2)

def check_new_account():

    file = open(user_data_file, "r")
    data = file.readlines()
    file.close()

    print(data)

    for username in data[1:]:
        if(username.split(',')[0] == user.get()):
            return False

    return True

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

    message = Label(login, text="", font=("Calibri", 18), fg="green")
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
    global header
    header = tkFont.Font(welcome, family="Roman", size=24, weight="bold")
    print(tkFont.families())

    Label(text="Pacemaker DCM", font=header, justify=CENTER).grid(row=0, column=0, padx=140)
    Label(text="").grid(row=1, column=0)
    Button(text="Login", padx=20, pady=10, command=login_page).grid(row=2, column=0)
    Label(text="").grid(row=3, column=0)
    Label(text="Not a registered user?").grid(row=4, column=0, pady = 10)
    Button(text="Register", padx=20, pady=10, command=register_page).grid(row=5, column=0)
    Label(text="", pady=100).grid(row=6, column=0)
    Button(text="Quit", padx=20, pady=10, command=welcome.destroy).grid(row=6, column=0)

    welcome.mainloop()


















# ACTUAL DCM ===========================================================================================================

# NAVIGATION BAR AT TOP OF WINDOW
def nav_bar():
    global nav
    global pmStatus
    global connectStatus

    nav = Frame(DCM)

    Label(nav, text="     Welcome to the DCM, " + user.get() + ": ", font=("Calibri", 14)).grid(row=0, column=0)
    pmStatus = Label(nav, text="Pacemaker Device Status: Pacemaker Device Change Detected", font=("Calibri", 13), padx = 35)
    pmStatus.grid(row=0, column=1, sticky = W, columnspan= 2)
    Button(nav, text="Dismiss", font=("Calibri", 12), command=changePmStatus).grid(row=0, column=3, pady=3, ipadx= 50)
    Button(nav, text="About", font=("Calibri", 12), command = about).grid(row=1, column=0, pady=3, ipadx= 50)
    connectStatus = Label(nav, text="Connection Status:  Connecting ", font=("Calibri", 13), padx= 35 )
    connectStatus.grid(row=1, column=1, sticky = W)
    Label(nav, text="[PORTS PLACEHOLDER]", font=("Calibri", 13), padx= 10 ).grid(row=1, column=2, sticky = W)
    Button(nav, text="Change Device", font=("Calibri", 12), command=changeConnectStatus).grid(row=1, column=3, pady=3, ipadx= 27)
    Label(nav, text= "-------------------------------------------------------", font=("Calibri", 13), padx = 10).grid(row=2, column=0, sticky = W)
    Label(nav, text= "     ---------------------------------------------------------------------------------------------", font=("Calibri", 13), padx = 10).grid(row=2, column=1, sticky = W, columnspan= 2)
    Button(nav, text="Log Out", font=("Calibri", 12), command=back_to_welcome).grid(row=2, column=3, pady=3, ipadx= 50)

def changePmStatus():
    pmStatus.config(text ="Pacemaker Device Status: No Issues")

def changeConnectStatus():
    connectStatus.config(text ="Connection Status: Disconnected")

def back_to_welcome():
    DCM.destroy()
    welcome_page()

def about():
    aboutScr = Toplevel(DCM)
    aboutScr.title("About")
    aboutScr.geometry("500x300")
    Label(aboutScr, text=" About ", font=("Calibri", 18)).grid(row=0, column=0, pady= 7, padx = 10)
    Label(aboutScr, text=" Application model number: PLACEHOLDER", font=("Calibri", 14)).grid(row=1, column=0, pady= 4, padx = 10)
    Label(aboutScr, text=" Application software revision number in use: PLACEHOLDER", font=("Calibri", 14)).grid(row=2, column=0, pady= 4, padx = 10)
    Label(aboutScr, text=" DCM serial number: PLACEHOLDER", font=("Calibri", 14)).grid(row=3, column=0, pady= 4, padx = 10)
    Label(aboutScr, text=" Institution name: McMaster University ", font=("Calibri", 14)).grid(row=4, column=0, pady= 4, padx = 10)
    Button(aboutScr, text="Close", font=("Calibri", 14), command= aboutScr.destroy).grid(row=5, column=0, pady = 7, ipadx= 30, ipady= 5, padx = 10)





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

    Label(AOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx= 85, pady=2)
    enter_lrl = Entry(AOO_mode, textvariable = lrl_value).grid(row=1, column=1)

    Label(AOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
    enter_url = Entry(AOO_mode, textvariable =url_value).grid(row=2, column=1)

    Label(AOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
    enter_aa = Entry(AOO_mode, textvariable=aa_value).grid(row=3, column=1)

    Label(AOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
    enter_apw = Entry(AOO_mode, textvariable=apw_value).grid(row=4, column=1)

    Button(AOO_mode, text="Update", padx=20, pady=10, command=send_AOO).grid(row=5, columnspan=2)

def send_AOO():
    mode = AOO()
    errormsg = ""
    error = False

    message = Label(AOO_mode, text=" ", font=("Calibri", 30), fg="green")
    message.grid(row=6, column=0, columnspan=2,pady= 15)

    # make sure values entered are valid
    try:
        lrlval = int(lrl_value.get())
        urlval = int(url_value.get())
        aaval = float(aa_value.get())
        apwval = float(apw_value.get())

        if(lrlval>175 or lrlval<30):
            error = True
            errormsg = "        Please make sure your lrl value         \n         is between 30-175 ppm.        "

        elif(lrlval>=30 and lrlval<=50 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl        \n         by 5 ppm for vals of 30-50 ppm.        "

        elif(lrlval>=90 and lrlval<=175 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl         \n         by 5 ppm for vals of 90-175 ppm.        "

        if (urlval>175 or urlval<50):
            error = True
            errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

        elif(urlval>=50 and urlval<=175):
            if(urlval%5 != 0):
                error = True
                errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "

        if (aaval <0  or aaval>5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif(aaval>=0 and aaval<=5):
            if((aaval*100)%5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "
        
        if(apwval != 0.05 and not(0.1 <= apwval <=1.9 and (apwval*100)%10 == 0)):
            error = True
            errormsg = "        Please make sure your apw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

        if error == False:
            mode.set_LRL(int(lrl_value.get()))
            mode.set_URL(int(url_value.get()))
            mode.set_AA(float(aa_value.get()))
            mode.set_APW(float(apw_value.get()))
            message.config(text="                         Update Success!                         ", fg="green")
        else:
            message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

    except:
        message.config(text="      Update Failed:       \n       Please use integers for lrl and url       \n       Please use floats for aa and apw      ", fg="red", font=("Calibri", 12))

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

    Label(VOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx= 85, pady=2)
    enter_lrl = Entry(VOO_mode, textvariable=lrl_value).grid(row=1, column=1)

    Label(VOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
    enter_url = Entry(VOO_mode, textvariable=url_value).grid(row=2, column=1)

    Label(VOO_mode, text="Ventrical Amplitude (V): ").grid(row=3, column=0, pady=2)
    enter_va = Entry(VOO_mode, textvariable=va_value).grid(row=3, column=1)

    Label(VOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=4, column=0, pady=2)
    enter_vpw = Entry(VOO_mode, textvariable=vpw_value).grid(row=4, column=1)

    Button(VOO_mode, text="Update", padx=20, pady=10, command=send_VOO).grid(row=5, columnspan=2, pady=2)

def send_VOO():
    mode = VOO()
    errormsg = ""
    error = False

    message = Label(VOO_mode, text="", font=("Calibri", 30), fg="green")
    message.grid(row=6, column=0, columnspan=2, pady= 15)

    # make sure values entered are valid
    try:
        lrlval = int(lrl_value.get())
        urlval = int(url_value.get())
        vaval = float(va_value.get())
        vpwval = float(vpw_value.get())

        if(lrlval>175 or lrlval<30):
            error = True
            errormsg = "        Please make sure your lrl value         \n         is between 30-175 ppm.        "

        elif(lrlval>=30 and lrlval<=50 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl        \n         by 5 ppm for vals of 30-50 ppm.        "

        elif(lrlval>=90 and lrlval<=175 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl         \n         by 5 ppm for vals of 90-175 ppm.        "

        if (urlval>175 or urlval<50):
            error = True
            errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

        elif(urlval>=50 and urlval<=175):
            if(urlval%5 != 0):
                error = True
                errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "
                
        if (vaval <0  or vaval>5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif(vaval>=0 and vaval<=5):
            if((vaval*100)%5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "
        
        if(vpwval != 0.05 and not(0.1 <= vpwval <=1.9 and (vpwval*100)%10 == 0)):
            error = True
            errormsg = "        Please make sure your vpw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

        if error == False:
            mode.set_LRL(int(lrl_value.get()))
            mode.set_URL(int(url_value.get()))
            mode.set_VA(float(va_value.get()))
            mode.set_VPW(float(vpw_value.get()))
            message.config(text="                         Update Success!                         ", fg="green")
        else:
            message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

    except:
        message.config(text="      Update Failed:       \n       Please use integers for lrl and url       \n       Please use floats for va and vpw      ", fg="red", font=("Calibri", 12))

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

    Label(AAI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85 , pady=2)
    enter_lrl = Entry(AAI_mode, textvariable=lrl_value).grid(row=1, column=1)

    Label(AAI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
    enter_url = Entry(AAI_mode, textvariable=url_value).grid(row=2, column=1)

    Label(AAI_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
    enter_aa = Entry(AAI_mode, textvariable=aa_value).grid(row=3, column=1)

    Label(AAI_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
    enter_apw = Entry(AAI_mode, textvariable=apw_value).grid(row=4, column=1)

    Label(AAI_mode, text="ARP (ms): ").grid(row=5, column=0, pady=2)
    enter_arp = Entry(AAI_mode, textvariable=arp_value).grid(row=5, column=1)

    Button(AAI_mode, text="Update", padx=20, pady=10, command=send_AAI).grid(row=6, columnspan=2 , pady=2)

def send_AAI():
    mode = AAI()
    errormsg = ""
    error = False

    message = Label(AAI_mode, text="", font=("Calibri", 30), fg="green")
    message.grid(row=7, column=0, columnspan=2, pady= 15)

    # make sure values entered are valid
    try:
        lrlval = int(lrl_value.get())
        urlval = int(url_value.get())
        aaval = float(aa_value.get())
        apwval = float(apw_value.get())
        arpval = int(arp_value.get())

        if(lrlval>175 or lrlval<30):
            error = True
            errormsg = "        Please make sure your lrl value         \n         is between 30-175 ppm.        "

        elif(lrlval>=30 and lrlval<=50 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl        \n         by 5 ppm for vals of 30-50 ppm.        "

        elif(lrlval>=90 and lrlval<=175 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl         \n         by 5 ppm for vals of 90-175 ppm.        "

        if (urlval>175 or urlval<50):
            error = True
            errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

        elif(urlval>=50 and urlval<=175):
            if(urlval%5 != 0):
                error = True
                errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "

        if (aaval <0  or aaval>5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif(aaval>=0 and aaval<=5):
            if((aaval*100)%5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "
        
        if(apwval != 0.05 and not(0.1 <= apwval <=1.9 and (apwval*100)%10 == 0)):
            error = True
            errormsg = "        Please make sure your apw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms!.        "

        if(not(arpval>=150 and arpval<=500 and (arpval%10 == 0))):
            error = True
            errormsg = "        Please make sure your arp value is between          \n         150ms and 500ms in increments of 10ms.        "
        

        if error == False:
            mode.set_LRL(int(lrl_value.get()))
            mode.set_URL(int(url_value.get()))
            mode.set_AA(float(aa_value.get()))
            mode.set_APW(float(apw_value.get()))
            mode.set_ARP(int(arp_value.get()))
            message.config(text="                         Update Success!                         ", fg="green")
        else:
            message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

    except:
        message.config(text="      Update Failed:       \n       Please use integers for lrl, url, and arp       \n       Please use floats for aa and apw      ", fg="red", font=("Calibri", 12))

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


    Label(VVI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady = 2)
    enter_lrl = Entry(VVI_mode, textvariable=lrl_value).grid(row=1, column=1)

    Label(VVI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
    enter_url = Entry(VVI_mode, textvariable=url_value).grid(row=2, column=1)

    Label(VVI_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
    enter_va = Entry(VVI_mode, textvariable=va_value).grid(row=3, column=1)

    Label(VVI_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
    enter_vpw = Entry(VVI_mode, textvariable=vpw_value).grid(row=4, column=1)

    Label(VVI_mode, text="VRP (ms): ").grid(row=5, column=0, pady=2)
    enter_vrp = Entry(VVI_mode, textvariable=vrp_value).grid(row=5, column=1)

    Button(VVI_mode, text="Update", padx=20, pady=10, command=send_VVI).grid(row=6, columnspan=2, pady= 2)

def send_VVI():
    mode = VVI()
    errormsg = ""
    error = False

    message = Label(VVI_mode, text="", font=("Calibri",30), fg="green")
    message.grid(row=7, column=0, columnspan=2, pady = 15)

    # make sure values entered are valid
    try:
        lrlval = int(lrl_value.get())
        urlval = int(url_value.get())
        vaval = float(va_value.get())
        vpwval = float(vpw_value.get())
        vrpval = int(vrp_value.get())

        if(lrlval>175 or lrlval<30):
            error = True
            errormsg = "        Please make sure your lrl value         \n         is between 30-175 ppm.        "

        elif(lrlval>=30 and lrlval<=50 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl        \n         by 5 ppm for vals of 30-50 ppm.        "

        elif(lrlval>=90 and lrlval<=175 and (lrlval%5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl         \n         by 5 ppm for vals of 90-175 ppm.        "

        if (urlval>175 or urlval<50):
            error = True
            errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

        elif(urlval>=50 and urlval<=175):
            if(urlval%5 != 0):
                error = True
                errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "

        if (vaval <0  or vaval>5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif(vaval>=0 and vaval<=5):
            if((vaval*100)%5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "

        if(vpwval != 0.05 and not(0.1 <= vpwval <=1.9 and (vpwval*100)%10 == 0)):
            error = True
            errormsg = "        Please make sure your vpw value is either          \n        0.05ms or 0.1ms - 1.9ms in increments of 0.1 ms.        "

        if(not(vrpval>=150 and vrpval<=500 and (vrpval%10 == 0))):
            error = True
            errormsg = "        Please make sure your vrp value is between          \n         150ms and 500ms in increments of 10 ms.        "

        if(error == False):
            mode.set_LRL(int(lrl_value.get()))
            mode.set_URL(int(url_value.get()))
            mode.set_VA(float(va_value.get()))
            mode.set_VPW(float(vpw_value.get()))
            mode.set_VRP(int(vrp_value.get()))
            message.config(text="              Update Success!              ", fg="green")
        else:
            message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

    except:
        message.config(text= "      Update Failed:       \n       Please use integers for lrl, url, and vrp       \n       Please use floats for va and vpw      ", fg="red", font=("Calibri", 12))

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

    pm_modes.grid(row=0, column=0, pady= 2)

def DCM_login():
    global DCM
    welcome.destroy()
    DCM = Tk()
    DCM.geometry("980x720")
    DCM.title("DCM")

    nav_bar()
    nav.grid(row=0)

    pacemaker_parameters()
    pm_params.grid(row=1, column=0, sticky = W, pady = 5)

erase_user_data()
welcome_page()

