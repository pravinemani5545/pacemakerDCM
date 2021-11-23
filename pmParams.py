from loginPage import *
from pacemakerModes import *
from paramChecking import *

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

        self.set_mode_VOO()
        self.set_mode_AAI()
        self.set_mode_VVI()
        self.set_mode_AOO()

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

    def set_mode_AOO(self):
        # set up AOO frame inside of pm_params frame
        self.mode_name.config(text="AOO")
        self.AOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one

        self.mode_frame.grid_forget()
        mode_frame = self.AOO_mode
        mode_frame.grid(row=1, column=0, columnspan=2)

        # parameters for this mode to be modified

        lrl = StringVar(self.AOO_mode)
        url = StringVar(self.AOO_mode)
        aa = StringVar(self.AOO_mode)
        apw = StringVar(self.AOO_mode)

        Label(self.AOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_url = Entry(self.AOO_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.AOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AOO_mode, textvariable=url).grid(row=2, column=1)

        Label(self.AOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AOO_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.AOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AOO_mode, textvariable=apw).grid(row=4, column=1)

        Button(self.AOO_mode, text="Update", padx=20, pady=10, command= lambda : self.send_AOO(lrl, url, aa, apw)).grid(row=5, columnspan=2)

    def send_AOO(self, lrl, url, aa, apw):
        mode = AOO(self.userName)
        errormsg = ""
        error = False

        message = Label(self.AOO_mode, text=" ", font=("Calibri", 30), fg="green")
        message.grid(row=6, column=0, columnspan=2, pady=15)

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(float(apw.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(float(apw.get()))
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
        
        lrl = StringVar(self.VOO_mode)
        url = StringVar(self.VOO_mode)
        va = StringVar(self.VOO_mode)
        vpw = StringVar(self.VOO_mode)

        Label(self.VOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx= 85, pady=2)
        enter_lrl = Entry(self.VOO_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VOO_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VOO_mode, text="Ventrical Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VOO_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VOO_mode, textvariable=vpw).grid(row=4, column=1)

        Button(self.VOO_mode, text="Update", padx=20, pady=10, command= lambda: self.send_VOO(lrl, url, va, vpw)).grid(row=5, columnspan=2, pady=2)

    def send_VOO(self, lrl, url, va, vpw):
        mode = VOO(self.userName)
        errormsg = ""
        error = True

        message = Label(self.VOO_mode, text="", font=("Calibri", 30), fg="green")
        message.grid(row=6, column=0, columnspan=2, pady= 15)

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(float(vpw.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(float(vpw.get()))
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
        lrl = StringVar(self.AAI_mode)
        url = StringVar(self.AAI_mode)
        aa = StringVar(self.AAI_mode)
        apw = StringVar(self.AAI_mode)
        arp = StringVar(self.AAI_mode)

        Label(self.AAI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85 , pady=2)
        enter_lrl = Entry(self.AAI_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.AAI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AAI_mode, textvariable=url).grid(row=2, column=1)

        Label(self.AAI_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AAI_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.AAI_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AAI_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.AAI_mode, text="ARP (ms): ").grid(row=5, column=0, pady=2)
        enter_arp = Entry(self.AAI_mode, textvariable=arp).grid(row=5, column=1)

        Button(self.AAI_mode, text="Update", padx=20, pady=10, command= lambda: self.send_AAI(lrl, url, aa, apw, arp)).grid(row=6, columnspan=2 , pady=2)

    def send_AAI(self, lrl, url, aa, apw, arp):
        mode = AAI(self.userName)
        errormsg = ""
        error = False

        message = Label(self.AAI_mode, text="", font=("Calibri", 30), fg="green")
        message.grid(row=7, column=0, columnspan=2, pady= 15)

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(float(apw.get()))
                        if error == False:
                            error, errormsg = check_ARP(int(lrl.get()), int(arp.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(float(apw.get()))
                mode.set_ARP(int(arp.get()))
                mode.write_params()
                message.config(text="                         Update Success!                         ", fg="green")
            else:
                message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))

        except:
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
        
        lrl = StringVar(self.VVI_mode)
        url = StringVar(self.VVI_mode)
        va = StringVar(self.VVI_mode)
        vpw = StringVar(self.VVI_mode)
        vrp = StringVar(self.VVI_mode)

        Label(self.VVI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady = 2)
        enter_lrl = Entry(self.VVI_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VVI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VVI_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VVI_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VVI_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VVI_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VVI_mode, textvariable=vpw).grid(row=4, column=1)

        Label(self.VVI_mode, text="VRP (ms): ").grid(row=5, column=0, pady=2)
        enter_vrp = Entry(self.VVI_mode, textvariable=vrp).grid(row=5, column=1)

        Button(self.VVI_mode, text="Update", padx=20, pady=10, command= lambda: self.send_VVI(lrl, url, va, vpw, vrp)).grid(row=6, columnspan=2, pady= 2)

    def send_VVI(self, lrl, url, va, vpw, vrp):
        mode = VVI(self.userName)
        errormsg = ""
        error = False

        message = Label(self.VVI_mode, text="", font=("Calibri",30), fg="green")
        message.grid(row=7, column=0, columnspan=2, pady = 15)

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(float(vpw.get()))
                        if error == False:
                            error, errormsg = check_VRP(int(lrl.get()), int(vrp.get()))

            if(error == False):
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(float(vpw.get()))
                mode.set_VRP(int(vrp.get()))
                mode.write_params()
                message.config(text="              Update Success!              ", fg="green")
            else:
                message.config(text= f"        Update Failed: \n {errormsg}        ", fg="red", font=("Calibri", 12))
		
        except:
            message.config(text= "      Update Failed:       \n       Please use integers for lrl, url, and vrp       \n       Please use floats for va and vpw      ", fg="red", font=("Calibri", 12))
