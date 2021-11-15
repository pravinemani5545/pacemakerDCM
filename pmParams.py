from tkinter import *
from loginPage import *
from pacemakerModes import *

class pmParams:
    def __init__(self, parent, *args, **kwargs):
        self.pmParams = parent
        self.userName = args[0]

        # displays current mode
        self.mode_name = Label(self.pmParams, text="")
        self.mode_name.grid(row=0, column=1)

        # initialize pacemaker mode windows
        self.mode_frame = Frame(self.pmParams)
        self.mode_frame.grid(row=1, column=0, columnspan=2)

        self.set_mode_AOO()
        self.set_mode_VOO()
        self.set_mode_AAI()
        self.set_mode_VVI()

        # set up menu to choose different pacemaker modes
        pm_modes = Menubutton(self.pmParams, text="Choose Pacing Mode", relief = GROOVE)
        pm_modes.menu = Menu(pm_modes, tearoff=0)
        pm_modes["menu"] = pm_modes.menu

        pm_modes.menu.add_command(label="AOO", command=self.set_mode_AOO)
        pm_modes.menu.add_command(label="VOO", command=self.set_mode_VOO)
        pm_modes.menu.add_command(label="AAI", command=self.set_mode_AAI)
        pm_modes.menu.add_command(label="VVI", command=self.set_mode_VVI)

        pm_modes.grid(row=0, column=0, pady= 2)

        self.pmParams.grid(row=1, column=0, sticky = W, pady = 5)

        # AOO MODE PARAMETERS
    def set_mode_AOO(self):
        # set up AOO frame inside of pm_params frame
        self.mode_name.config(text="AOO")
        self.AOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        
        self.mode_frame.grid_forget()
        mode_frame = self.AOO_mode
        mode_frame.grid(row=1, column=0, columnspan=2)

        # parameters for this mode to be modified
        
        self.lrl_value = StringVar(self.AOO_mode)
        self.url_value = StringVar(self.AOO_mode)
        self.aa_value = StringVar(self.AOO_mode)
        self.apw_value = StringVar(self.AOO_mode)

        Label(self.AOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx= 85, pady=2)
        enter_url = Entry(self.AOO_mode, textvariable=self.lrl_value).grid(row=1, column=1)

        Label(self.AOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AOO_mode, textvariable = self.url_value).grid(row=2, column=1)

        Label(self.AOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AOO_mode, textvariable= self.aa_value).grid(row=3, column=1)

        Label(self.AOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AOO_mode, textvariable= self.apw_value).grid(row=4, column=1)

        Button(self.AOO_mode, text="Update", padx=20, pady=10, command= self.send_AOO).grid(row=5, columnspan=2)

    def send_AOO(self):
        mode = AOO(self.userName)
        errormsg = ""
        error = False

        message = Label(self.AOO_mode, text=" ", font=("Calibri", 30), fg="green")
        message.grid(row=6, column=0, columnspan=2, pady=15)

        # make sure values entered are valid
        try:
            error, errormsg = self.check_LRL(int(self.lrl_value.get()))
            if error == False:
                error, errormsg = self.check_URL(int(self.url_value.get()))
                if error == False:
                     error, errormsg = self.check_AA(float(self.aa_value.get()))
                     if error == False:
                        error, errormsg = self.check_APW(float(self.apw_value.get()))

            if error == False:
                mode.set_LRL(int(self.lrl_value.get()))
                mode.set_URL(int(self.url_value.get()))
                mode.set_AA(float(self.aa_value.get()))
                mode.set_APW(float(self.apw_value.get()))
                mode.write_params()
                message.config(text="                         Update Success!                         ", fg="green")
            else:
                message.config(text=f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

        except Exception as e:
            print(f"EXCEPTION: {e}")
            message.config(
                text="      Update Failed:       \n       Please use integers for lrl and url       \n       Please use floats for aa and apw      ",
                fg="red", font=("Calibri", 12))

        # VOO MODE PARAMETERS
    def set_mode_VOO(self):
        self.mode_name.config(text="VOO")
        self.VOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VOO_mode
        self.mode_frame.grid(row=1, column=0, columnspan=2)

        # parameters for this mode to be modified
        
        self.lrl_value = StringVar(self.VOO_mode)
        self.url_value = StringVar(self.VOO_mode)
        self.va_value = StringVar(self.VOO_mode)
        self.vpw_value = StringVar(self.VOO_mode)

        Label(self.VOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx= 85, pady=2)
        enter_lrl = Entry(self.VOO_mode, textvariable=self.lrl_value).grid(row=1, column=1)

        Label(self.VOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VOO_mode, textvariable=self.url_value).grid(row=2, column=1)

        Label(self.VOO_mode, text="Ventrical Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VOO_mode, textvariable=self.va_value).grid(row=3, column=1)

        Label(self.VOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VOO_mode, textvariable=self.vpw_value).grid(row=4, column=1)

        Button(self.VOO_mode, text="Update", padx=20, pady=10, command=self.send_VOO).grid(row=5, columnspan=2, pady=2)

    def send_VOO(self):
        mode = VOO(self.userName)
        errormsg = ""
        error = False

        message = Label(self.VOO_mode, text="", font=("Calibri", 30), fg="green")
        message.grid(row=6, column=0, columnspan=2, pady= 15)

        # make sure values entered are valid
        try:
            error, errormsg = self.check_LRL(int(self.lrl_value.get()))
            if error == False:
                error, errormsg = self.check_URL(int(self.url_value.get()))
                if error == False:
                    error, errormsg = self.check_VA(float(self.va_value.get()))
                    if error == False:
                        error, errormsg = self.check_VPW(float(self.vpw_value.get()))

            if error == False:
                mode.set_LRL(int(self.lrl_value.get()))
                mode.set_URL(int(self.url_value.get()))
                mode.set_VA(float(self.va_value.get()))
                mode.set_VPW(float(self.vpw_value.get()))
                mode.write_params()
                message.config(text="                         Update Success!                         ", fg="green")
            else:
                message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))


        except Exception as e:
            print(f"EXCEPTION: {e}")
            message.config(text="      Update Failed:       \n       Please use integers for lrl and url       \n       Please use floats for va and vpw      ", fg="red", font=("Calibri", 12))

        # AAI MODE PARAMETERS
    def set_mode_AAI(self):
        self.mode_name.config(text="AAI")
        self.AAI_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.AAI_mode
        self.mode_frame.grid(row=1, column=0, columnspan=2)

        # parameters for this mode to be modified
        self.lrl_value = StringVar(self.AAI_mode)
        self.url_value = StringVar(self.AAI_mode)
        self.aa_value = StringVar(self.AAI_mode)
        self.apw_value = StringVar(self.AAI_mode)
        self.arp_value = StringVar(self.AAI_mode)

        Label(self.AAI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85 , pady=2)
        enter_lrl = Entry(self.AAI_mode, textvariable=self.lrl_value).grid(row=1, column=1)

        Label(self.AAI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AAI_mode, textvariable=self.url_value).grid(row=2, column=1)

        Label(self.AAI_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AAI_mode, textvariable=self.aa_value).grid(row=3, column=1)

        Label(self.AAI_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AAI_mode, textvariable=self.apw_value).grid(row=4, column=1)

        Label(self.AAI_mode, text="ARP (ms): ").grid(row=5, column=0, pady=2)
        enter_arp = Entry(self.AAI_mode, textvariable=self.arp_value).grid(row=5, column=1)

        Button(self.AAI_mode, text="Update", padx=20, pady=10, command=self.send_AAI).grid(row=6, columnspan=2 , pady=2)

    def send_AAI(self):
        mode = AAI(self.userName)
        errormsg = ""
        error = False

        message = Label(self.AAI_mode, text="", font=("Calibri", 30), fg="green")
        message.grid(row=7, column=0, columnspan=2, pady= 15)

        # make sure values entered are valid
        try:
            error, errormsg = self.check_LRL(int(self.lrl_value.get()))
            if error == False:
                error, errormsg = self.check_URL(int(self.url_value.get()))
                if error == False:
                    error, errormsg = self.check_AA(float(self.aa_value.get()))
                    if error == False:
                        error, errormsg = self.check_APW(float(self.apw_value.get()))
                        if error == False:
                            error, errormsg = self.check_ARP(float(self.arp_value.get()))

            if error == False:
                mode.set_LRL(int(self.lrl_value.get()))
                mode.set_URL(int(self.url_value.get()))
                mode.set_AA(float(self.aa_value.get()))
                mode.set_APW(float(self.apw_value.get()))
                mode.set_ARP(int(self.arp_value.get()))
                mode.write_params()
                message.config(text="                         Update Success!                         ", fg="green")
            else:
                message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))
		except Exception as e:
            print(f"EXCEPTION: {e}")
            message.config(text="      Update Failed:       \n       Please use integers for lrl, url, and arp       \n       Please use floats for aa and apw      ", fg="red", font=("Calibri", 12))

        # VVI MODE PARAMETERS
    def set_mode_VVI(self):
        self.mode_name.config(text="VVI")

        self.VVI_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VVI_mode
        self.mode_frame.grid(row=1, column=0, columnspan=2)

        # parameters for this mode to be modified
        
        self.lrl_value = StringVar(self.VVI_mode)
        self.url_value = StringVar(self.VVI_mode)
        self.va_value = StringVar(self.VVI_mode)
        self.vpw_value = StringVar(self.VVI_mode)
        self.vrp_value = StringVar(self.VVI_mode)

        Label(self.VVI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady = 2)
        enter_lrl = Entry(self.VVI_mode, textvariable=self.lrl_value).grid(row=1, column=1)

        Label(self.VVI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VVI_mode, textvariable=self.url_value).grid(row=2, column=1)

        Label(self.VVI_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VVI_mode, textvariable=self.va_value).grid(row=3, column=1)

        Label(self.VVI_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VVI_mode, textvariable=self.vpw_value).grid(row=4, column=1)

        Label(self.VVI_mode, text="VRP (ms): ").grid(row=5, column=0, pady=2)
        enter_vrp = Entry(self.VVI_mode, textvariable=self.vrp_value).grid(row=5, column=1)

        Button(self.VVI_mode, text="Update", padx=20, pady=10, command=self.send_VVI).grid(row=6, columnspan=2, pady= 2)

    def send_VVI(self):
        mode = VVI(self.userName)
        errormsg = ""
        error = False

        message = Label(self.VVI_mode, text="", font=("Calibri",30), fg="green")
        message.grid(row=7, column=0, columnspan=2, pady = 15)

        # make sure values entered are valid
        try:
            error, errormsg = self.check_LRL(int(self.lrl_value.get()))
            if error == False:
                error, errormsg = self.check_URL(int(self.url_value.get()))
                if error == False:
                    error, errormsg = self.check_VA(float(self.va_value.get()))
                    if error == False:
                        error, errormsg = self.check_VPW(float(self.vpw_value.get()))
                        if error == False:
                            error, errormsg = self.check_VRP(float(self.vrp_value.get()))

            if(error == False):
                mode.set_LRL(int(self.lrl_value.get()))
                mode.set_URL(int(self.url_value.get()))
                mode.set_VA(float(self.va_value.get()))
                mode.set_VPW(float(self.vpw_value.get()))
                mode.set_VRP(int(self.vrp_value.get()))
                mode.write_params()
                message.config(text="              Update Success!              ", fg="green")
            else:
                message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))
		
		except Exception as e:
            print(f"EXCEPTION: {e}")
            message.config(text= "      Update Failed:       \n       Please use integers for lrl, url, and vrp       \n       Please use floats for va and vpw      ", fg="red", font=("Calibri", 12))

# PARAMETER VALIDITY CHECKS
    def check_LRL(self, lrlval):
        errormsg = ""
        error = False

        if (lrlval > 175 or lrlval < 30):
            error = True
            errormsg = "        Please make sure your lrl value         \n         is between 30-175 ppm.        "

        elif (lrlval >= 30 and lrlval <= 50 and (lrlval % 5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl        \n         by 5 ppm for vals of 30-50 ppm.        "

        elif (lrlval >= 90 and lrlval <= 175 and (lrlval % 5 != 0)):
            error = True
            errormsg = "        Please make sure you increment lrl         \n         by 5 ppm for vals of 90-175 ppm.        "

        return error, errormsg

    def check_URL(self, urlval):
        errormsg = ""
        error = False

        if (urlval > 175 or urlval < 50):
            error = True
            errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

        elif (urlval >= 50 and urlval <= 175 and (urlval % 5 != 0)):
                error = True
                errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "

        return error, errormsg

    def check_AA(self, aaval):
        errormsg = ""
        error = False

        if (aaval < 0 or aaval > 5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif (aaval >= 0 and aaval <= 5):
            if ((aaval * 100) % 5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "

        return error, errormsg

    def check_VA(self, vaval):
        errormsg = ""
        error = False

        if (vaval < 0 or vaval > 5):
            error = True
            errormsg = "        Please make sure your amplitude value         \n         is between 0 and 5 Volts.        "

        elif (vaval >= 0 and vaval <= 5):
            if ((vaval * 100) % 5 != 0):
                error = True
                errormsg = "        Please make sure you increment amplitude         \n         by values of 0.05 V.        "

        return error, errormsg

    def check_APW(self, apwval):
        errormsg = ""
        error = False

        if (apwval != 0.05 and not (0.1 <= apwval <= 1.9 and (apwval * 100) % 10 == 0)):
            error = True
            errormsg = "        Please make sure your apw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

        return error, errormsg

    def check_VPW(self, vpwval):
        errormsg = ""
        error = False

        if (vpwval != 0.05 and not (0.1 <= vpwval <= 1.9 and (vpwval * 100) % 10 == 0)):
            error = True
            errormsg = "        Please make sure your vpw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

        return error, errormsg

    def check_ARP(self, arpval):
        errormsg = ""
        error = False

        if (not (arpval >= 150 and arpval <= 500 and (arpval % 10 == 0))):
            error = True
            errormsg = "        Please make sure your arp value is between          \n         150ms and 500ms in increments of 10ms.        "

        return error, errormsg

    def check_VRP(self, vrpval):
        errormsg = ""
        error = False

        if (not (vrpval >= 150 and vrpval <= 500 and (vrpval % 10 == 0))):
            error = True
            errormsg = "        Please make sure your vrp value is between          \n         150ms and 500ms in increments of 10 ms.        "

        return error, errormsg
