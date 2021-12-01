from loginPage import *
from pacemakerModes import *
from paramChecking import *
from serialcom import*
from tkinter import *
import serial
import struct
import random
import numpy as np
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep
from eGramPage import *

class pmParams:
    def __init__(self, parent, *args, **kwargs):
        self.pmParams = parent
        self.userName = args[0]
        self.serial = args[1]
        self.DCM = args[2]

        # displays current mode name
        self.mode_name = Label(self.pmParams, text="                ")
        self.mode_name.grid(row=0, column=1)

        # displays current mode name
        self.verify = Label(self.pmParams, text="Current Pacemaker Settings: ")
        self.verify.grid(row=0, column=2)

        # initialize pacemaker mode windows
        self.mode_frame = Frame(self.pmParams)
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        self.message = Frame(self.pmParams)
        self.message.grid()

        self.set_mode_VOO()
        self.set_mode_AAI()
        self.set_mode_VVI()
        self.set_mode_DOO()
        self.set_mode_AOOR()
        self.set_mode_VOOR()
        self.set_mode_AAIR()
        self.set_mode_VVIR()
        self.set_mode_DOOR()
        self.set_mode_AOO()

        # set up menu to choose different pacemaker modes
        pm_modes = Menubutton(self.pmParams, text="Choose Pacing Mode: ", relief = GROOVE)
        pm_modes.menu = Menu(pm_modes, tearoff=0)
        pm_modes["menu"] = pm_modes.menu

        pm_modes.menu.add_command(label="AOO (2)", command=self.set_mode_AOO)
        pm_modes.menu.add_command(label="VOO (1)", command=self.set_mode_VOO)
        pm_modes.menu.add_command(label="AAI (4)", command=self.set_mode_AAI)
        pm_modes.menu.add_command(label="VVI (3)", command=self.set_mode_VVI)
        pm_modes.menu.add_command(label="DOO (5)", command=self.set_mode_DOO)
        pm_modes.menu.add_command(label="AOOR (7)", command=self.set_mode_AOOR)
        pm_modes.menu.add_command(label="VOOR (6)", command=self.set_mode_VOOR)
        pm_modes.menu.add_command(label="AAIR (9)", command=self.set_mode_AAIR)
        pm_modes.menu.add_command(label="VVIR (8)", command=self.set_mode_VVIR)
        pm_modes.menu.add_command(label="DOOR (10)", command=self.set_mode_DOOR)

        pm_modes.grid(row=0, column=0, pady=2, padx = 35)

        Button(self.pmParams, text="E-Gram", command= self.eGram).grid(row=2,column=3, ipadx = 20)

        self.pmParams.grid(row=1, column=0, sticky = W, pady = 5)

    def eGram(self):
        self.eGramPg = Toplevel(self.pmParams)
        self.eGramWindow = eGramPage(self.eGramPg, self.serial, self.DCM, self.userName)
        self.DCM.withdraw()
        
    # AOO MODE PARAMETERS
    def set_mode_AOO(self):
        # set up AOO frame inside of pm_params frame
        self.mode_name.config(text="AOO")
        self.AOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.AOO_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

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

        Button(self.AOO_mode, text="Update", padx=20, pady=10, command= lambda : self.send_AOO(lrl, url, aa, apw)).grid(row=5,column=1,pady=20)

        Label(self.AOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.AOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.AOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.AOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Button(self.AOO_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_AOOR).grid(row=5, column=3, pady=2)

    def send_AOO(self, lrl, url, aa, apw):
        mode = Mode(self.userName, 2)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.AOO_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(int(apw.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.AOO_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=6, columnspan=2, pady=15)

                    Label(self.AOO_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.AOO_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.AOO_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.AOO_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)

                
            else:
                self.message.destroy()
                self.message = Label(self.AOO_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),  fg="red")
                self.message.grid(row=6, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.AOO_mode, 
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=6, columnspan=2, pady=15)

    def retrieve_AOO(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.AOO_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.AOO_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.AOO_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.AOO_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.AOO_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=5, column=2,  pady=2)

    # VOO MODE PARAMETERS
    def set_mode_VOO(self):
        # set up VOO frame inside of pm_params frame
        self.mode_name.config(text="VOO")
        self.VOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VOO_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.VOO_mode)
        url = StringVar(self.VOO_mode)
        va = StringVar(self.VOO_mode)
        vpw = StringVar(self.VOO_mode)

        Label(self.VOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_lrl = Entry(self.VOO_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VOO_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VOO_mode, text="Ventrical Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VOO_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VOO_mode, textvariable=vpw).grid(row=4, column=1)

        Button(self.VOO_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_VOO(lrl, url, va, vpw)).grid(row=5, column=1, pady=20)

        Label(self.VOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.VOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.VOO_mode, text="Ventrical Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.VOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Button(self.VOO_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_VOO).grid(row=5, column=3, pady=2)

    def send_VOO(self, lrl, url, va, vpw):
        mode = Mode(self.userName, 1)
        errormsg = ""
        error = True

        # initialize message label
        self.message.destroy()
        self.message = Label(self.VOO_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.VOO_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=6, columnspan=2, pady=15)

                    Label(self.VOO_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.VOO_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.VOO_mode, text= round(echoFromSim[5], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.VOO_mode, text= echoFromSim[3]).grid(row=4, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.VOO_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),
                                     fg="red")
                self.message.grid(row=6, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.VOO_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=6, columnspan=2, pady=15)

    def retrieve_VOO(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.VOO_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.VOO_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.VOO_mode, text= fromSim[5]).grid(row=3, column=3,  pady=2)
        Label(self.VOO_mode, text= fromSim[3]).grid(row=4, column=3,  pady=2)
        Label(self.VOO_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=5, column=2,  pady=2)

    # AAI MODE PARAMETERS
    def set_mode_AAI(self):
        self.mode_name.config(text="AAI")
        self.AAI_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.AAI_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.AAI_mode)
        url = StringVar(self.AAI_mode)
        aa = StringVar(self.AAI_mode)
        apw = StringVar(self.AAI_mode)
        arp = StringVar(self.AAI_mode)
        sense = StringVar(self.AAI_mode)
        pvarp = StringVar(self.AAI_mode)

        Label(self.AAI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_lrl = Entry(self.AAI_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.AAI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AAI_mode, textvariable=url).grid(row=2, column=1)

        Label(self.AAI_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AAI_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.AAI_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AAI_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.AAI_mode, text="ARP (ms): ").grid(row=5, column=0, pady=2)
        enter_arp = Entry(self.AAI_mode, textvariable=arp).grid(row=5, column=1)

        Label(self.AAI_mode, text="Atrial Sensitivity (V): ").grid(row=6, column=0, padx=85, pady=2)
        enter_sense = Entry(self.AAI_mode, textvariable=sense).grid(row=6, column=1)

        Label(self.AAI_mode, text="Post VARP (ms): ").grid(row=7, column=0,pady=2)
        enter_pvarp = Entry(self.AAI_mode, textvariable=pvarp).grid(row=7, column=1)

        Button(self.AAI_mode, text="Update", padx=20, pady=10, command=lambda: 
        self.send_AAI(lrl, url, aa, apw, arp, sense, pvarp)).grid(row=8, column=1, pady=20)

        Label(self.AAI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="ARP (ms): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="Atrial Sensitivity (V): ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.AAI_mode, text="Post VARP (ms): ").grid(row=7, column=2, padx=85, pady=2)
        Button(self.AAI_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_AAI).grid(row=8, column=3, pady=2)
        

    def send_AAI(self, lrl, url, aa, apw, arp, sense, pvarp):
        mode = Mode(self.userName, 4)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.AAI_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(int(apw.get()))
                        if error == False:
                            error, errormsg = check_ARP(int(lrl.get()), int(arp.get()))
                            if error == False:
                                error, errormsg = check_AS(float(sense.get()))
                                if error == False:
                                    error, errormsg = check_PVARP(int(pvarp.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.set_ARP(int(arp.get()))
                mode.set_AS(float(sense.get()))
                mode.set_PVARP(int(pvarp.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.AAI_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=9, columnspan=2, pady=15)

                    Label(self.AAI_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.AAI_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.AAI_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.AAI_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)
                    Label(self.AAI_mode, text= echoFromSim[10]).grid(row=5, column=3,  pady=2)
                    Label(self.AAI_mode, text= round(echoFromSim[8], 2)).grid(row=6, column=3,  pady=2)
                    Label(self.AAI_mode, text= "").grid(row=7, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.AAI_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),
                                     fg="red")
                self.message.grid(row=9, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.AAI_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=9, columnspan=2, pady=15)

    def retrieve_AAI(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.AAI_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.AAI_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.AAI_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.AAI_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.AAI_mode, text= fromSim[10]).grid(row=5, column=3,  pady=2)
        Label(self.AAI_mode, text= fromSim[8]).grid(row=6, column=3,  pady=2)
        Label(self.AAI_mode, text= "").grid(row=7, column=3,  pady=2)
        Label(self.AAI_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=8, column=2,  pady=2)

    # VVI MODE PARAMETERS
    def set_mode_VVI(self):
        self.mode_name.config(text="VVI")

        self.VVI_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VVI_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.VVI_mode)
        url = StringVar(self.VVI_mode)
        va = StringVar(self.VVI_mode)
        vpw = StringVar(self.VVI_mode)
        vrp = StringVar(self.VVI_mode)
        sense = StringVar(self.VVI_mode)

        Label(self.VVI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_lrl = Entry(self.VVI_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VVI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VVI_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VVI_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VVI_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VVI_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VVI_mode, textvariable=vpw).grid(row=4, column=1)

        Label(self.VVI_mode, text="VRP (ms): ").grid(row=5, column=0, pady=2)
        enter_vrp = Entry(self.VVI_mode, textvariable=vrp).grid(row=5, column=1)

        Label(self.VVI_mode, text="Ventricular Sensitivity (V): ").grid(row=6, column=0)
        enter_sense = Entry(self.VVI_mode, textvariable=sense).grid(row=6, column=1)

        Button(self.VVI_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_VVI(lrl, url, va, vpw, vrp, sense)).grid(row=7, column=1, pady=20)

        Label(self.VVI_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.VVI_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.VVI_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.VVI_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.VVI_mode, text="VRP (ms): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.VVI_mode, text="Ventricular Sensitivity (V): ").grid(row=6, column=2, padx=85, pady=2)
        Button(self.VVI_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_VVI).grid(row=7, column=3, pady=2)

    def send_VVI(self, lrl, url, va, vpw, vrp, sense):
        mode = Mode(self.userName, 3)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.VVI_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))
                        if error == False:
                            error, errormsg = check_VRP(int(lrl.get()), int(vrp.get()))
                            if error == False:
                                error, errormsg = check_VS(float(sense.get()))
                                

            if (error == False):
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.set_VRP(int(vrp.get()))
                mode.set_VS(float(sense.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.VVI_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=8, columnspan=2, pady=15)

                    Label(self.VVI_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.VVI_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.VVI_mode, text= round(echoFromSim[5], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.VVI_mode, text= echoFromSim[3]).grid(row=4, column=3,  pady=2)
                    Label(self.VVI_mode, text= echoFromSim[9]).grid(row=5, column=3,  pady=2)
                    Label(self.VVI_mode, text= echoFromSim[7]).grid(row=6, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.VVI_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15), fg="red")
                self.message.grid(row=8, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.VVI_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=8, columnspan=2, pady=15)

    def retrieve_VVI(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.VVI_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.VVI_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.VVI_mode, text= fromSim[5]).grid(row=3, column=3,  pady=2)
        Label(self.VVI_mode, text= fromSim[3]).grid(row=4, column=3,  pady=2)
        Label(self.VVI_mode, text= fromSim[9]).grid(row=5, column=3,  pady=2)
        Label(self.VVI_mode, text= fromSim[7]).grid(row=6, column=3,  pady=2)
        Label(self.VVI_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=7, column=2,  pady=2)

    # DOO MODE PARAMETERS
    def set_mode_DOO(self):
        # set up DOO frame inside of pm_params frame
        self.mode_name.config(text="DOO")
        self.DOO_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.DOO_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.DOO_mode)
        url = StringVar(self.DOO_mode)
        va = StringVar(self.DOO_mode)
        vpw = StringVar(self.DOO_mode)
        aa = StringVar(self.DOO_mode)
        apw = StringVar(self.DOO_mode)
        av = StringVar(self.DOO_mode)

        Label(self.DOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_lrl = Entry(self.DOO_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.DOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.DOO_mode, textvariable=url).grid(row=2, column=1)

        Label(self.DOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.DOO_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.DOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.DOO_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.DOO_mode, text="Ventrical Amplitude (V): ").grid(row=5, column=0, pady=2)
        enter_va = Entry(self.DOO_mode, textvariable=va).grid(row=5, column=1)

        Label(self.DOO_mode, text="Ventrical Pulse Width (ms): ").grid(row=6, column=0, pady=2)
        enter_vpw = Entry(self.DOO_mode, textvariable=vpw).grid(row=6, column=1)

        Label(self.DOO_mode, text="Fixed AV Delay(ms): ").grid(row=7, column=0, pady=2)
        enter_av = Entry(self.DOO_mode, textvariable=av).grid(row=7, column=1)

        Button(self.DOO_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_DOO(lrl, url, va, vpw, aa, apw, av)).grid(row=8, column=1, pady=20)

        Label(self.DOO_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Ventricular Amplitude (V): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Ventricular Pulse Width (ms): ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.DOO_mode, text="Fixed AV Delay(ms): ").grid(row=7, column=2, padx=85, pady=2)
        Button(self.DOO_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_DOO).grid(row=8, column=3, pady=2)

    # DOO PARAMETERS
    def send_DOO(self, lrl, url, va, vpw, aa, apw, av):
        mode = Mode(self.userName, 5)
        errormsg = ""
        error = True

        # initialize message label
        self.message.destroy()
        self.message = Label(self.DOO_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))
                        if error == False:
                            error, errormsg = check_AA(float(aa.get()))
                            if error == False:
                                error, errormsg = check_APW(int(apw.get()))
                                if error == False:
                                    error, errormsg = check_AV_DELAY(int(av.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.set_FIXED_AV_DELAY(int(av.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.DOO_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=9, columnspan=2, pady=15)

                    Label(self.DOO_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.DOO_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.DOO_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.DOO_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)
                    Label(self.DOO_mode, text= round(echoFromSim[5], 2)).grid(row=5, column=3,  pady=2)
                    Label(self.DOO_mode, text= echoFromSim[3]).grid(row=6, column=3,  pady=2)
                    Label(self.DOO_mode, text= echoFromSim[11]).grid(row=7, column=3,  pady=2)
            else:
                self.message.destroy()
                self.message = Label(self.DOO_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15), fg="red")
                self.message.grid(row=9, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.DOO_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=9, columnspan=2, pady=15)
    
    def retrieve_DOO(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.DOO_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[5]).grid(row=5, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[3]).grid(row=6, column=3,  pady=2)
        Label(self.DOO_mode, text= fromSim[11]).grid(row=7, column=3,  pady=2)
        Label(self.DOO_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=8, column=2,  pady=2)

    # AOOR MODE PARAMETERS
    def set_mode_AOOR(self):
        # set up AOOR frame inside of pm_params frame
        self.mode_name.config(text="AOOR")
        self.AOOR_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.AOOR_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.AOOR_mode)
        url = StringVar(self.AOOR_mode)
        aa = StringVar(self.AOOR_mode)
        apw = StringVar(self.AOOR_mode)
        max = StringVar(self.AOOR_mode)
        threshold = StringVar(self.AOOR_mode)
        rxn = StringVar(self.AOOR_mode)
        response = StringVar(self.AOOR_mode)
        recovery = StringVar(self.AOOR_mode)

        Label(self.AOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_url = Entry(self.AOOR_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.AOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AOOR_mode, textvariable=url).grid(row=2, column=1)

        Label(self.AOOR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AOOR_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.AOOR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AOOR_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.AOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=5, column=0, pady=2)
        enter_max = Entry(self.AOOR_mode, textvariable=max).grid(row=5, column=1)

        thresh_vals = ("V-Low (1)", "Low (2)", "Med-Low (3)", "Med (4)", "Med-High (5)", "High (6)", "V-High (7)")
        Label(self.AOOR_mode, text="Activity Threshold : ").grid(row=6, column=0, pady=2)
        enter_threshold = Spinbox(self.AOOR_mode, values=thresh_vals, state="readonly", textvariable=threshold).grid(row=6, column=1)

        Label(self.AOOR_mode, text="Reaction Time (s): ").grid(row=7, column=0, pady=2)
        enter_rxn = Entry(self.AOOR_mode, textvariable=rxn).grid(row=7, column=1)

        Label(self.AOOR_mode, text="Response Factor : ").grid(row=8, column=0, pady=2)
        enter_response = Entry(self.AOOR_mode, textvariable=response).grid(row=8, column=1)

        Label(self.AOOR_mode, text="Recovery Time (mins) : ").grid(row=9, column=0, pady=2)
        enter_recovery = Entry(self.AOOR_mode, textvariable=recovery).grid(row=9, column=1)

        Button(self.AOOR_mode, text="Update", padx=20, pady=10,
               command= lambda : self.send_AOOR(lrl, url, aa, apw, max, threshold, rxn, response,
                                 recovery)).grid(row=10,column=1, pady=20)

        Label(self.AOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Activity Threshold : ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Reaction Time (s): ").grid(row=7, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Response Factor : ").grid(row=8, column=2, padx=85, pady=2)
        Label(self.AOOR_mode, text="Recovery Time (mins) : ").grid(row=9, column=2, padx=85, pady=2)
        Button(self.AOOR_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_AOOR).grid(row=10, column=3, pady=2)

    def send_AOOR(self, lrl, url, aa, apw, max, threshold, rxn, response, recovery):
        mode = Mode(self.userName, 7)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.AOOR_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(int(apw.get()))
                        if error == False:
                            error, errormsg = check_MAX_SENSE_RATE(int(max.get()),int(url.get()),int(lrl.get()))
                            if error == False:
                                error, errormsg = check_RXN_TIME(int(rxn.get()))
                                if error == False:
                                    error, errormsg = check_RESPONSE(int(response.get()))
                                    if error == False:
                                        error, errormsg = check_RECOVERY(int(recovery.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.set_MAX_SENSE_RATE(int(max.get()))
                mode.set_ACT_THRESHOLD(threshold.get())
                mode.set_REACTION_TIME (int(rxn.get()))
                mode.set_RESPONSE_FACTOR(int(response.get()))
                mode.set_RECOVERY_TIME(int(recovery.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)
                    
                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"
                
                else:
                    self.message.destroy()
                    self.message = Label(self.AOOR_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=11, columnspan=2, pady=15)
    
                    Label(self.AOOR_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.AOOR_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[16]).grid(row=5, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[12]).grid(row=6, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[13]).grid(row=7, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[14]).grid(row=8, column=3,  pady=2)
                    Label(self.AOOR_mode, text= echoFromSim[15]).grid(row=9, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.AOOR_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),  fg="red")
                self.message.grid(row=11, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.AOOR_mode, 
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=11, columnspan=2, pady=15)

    def retrieve_AOOR(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.AOOR_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[16]).grid(row=5, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[12]).grid(row=6, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[13]).grid(row=7, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[14]).grid(row=8, column=3,  pady=2)
        Label(self.AOOR_mode, text= fromSim[15]).grid(row=9, column=3,  pady=2)
        Label(self.AOOR_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=10, column=2,  pady=2)

    # VOOR MODE PARAMETERS
    def set_mode_VOOR(self):
        # set up VOOR frame inside of pm_params frame
        self.mode_name.config(text="VOOR")
        self.VOOR_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VOOR_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.VOOR_mode)
        url = StringVar(self.VOOR_mode)
        va = StringVar(self.VOOR_mode)
        vpw = StringVar(self.VOOR_mode)
        max = StringVar(self.VOOR_mode)
        threshold = StringVar(self.VOOR_mode)
        rxn = StringVar(self.VOOR_mode)
        response = StringVar(self.VOOR_mode)
        recovery = StringVar(self.VOOR_mode)

        Label(self.VOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_url = Entry(self.VOOR_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VOOR_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VOOR_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VOOR_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VOOR_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VOOR_mode, textvariable=vpw).grid(row=4, column=1)

        Label(self.VOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=5, column=0, pady=2)
        enter_max = Entry(self.VOOR_mode, textvariable=max).grid(row=5, column=1)

        thresh_vals = ("V-Low (1)", "Low (2)", "Med-Low (3)", "Med (4)", "Med-High (5)", "High (6)", "V-High (7)")
        Label(self.VOOR_mode, text="Activity Threshold : ").grid(row=6, column=0,pady=2)
        enter_threshold = Spinbox(self.VOOR_mode, values=thresh_vals, state="readonly", textvariable=threshold).grid(
            row=6, column=1)

        Label(self.VOOR_mode, text="Reaction Time (s): ").grid(row=7, column=0, pady=2)
        enter_rxn = Entry(self.VOOR_mode, textvariable=rxn).grid(row=7, column=1)

        Label(self.VOOR_mode, text="Response Factor : ").grid(row=8, column=0, pady=2)
        enter_response = Entry(self.VOOR_mode, textvariable=response).grid(row=8, column=1)

        Label(self.VOOR_mode, text="Recovery Time (mins) : ").grid(row=9, column=0, pady=2)
        enter_recovery = Entry(self.VOOR_mode, textvariable=recovery).grid(row=9, column=1)

        Button(self.VOOR_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_VOOR(lrl, url, va, vpw, max, threshold, rxn, response,
                                              recovery)).grid(row=10, column=1, pady=20)
        
        Label(self.VOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Activity Threshold : ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Reaction Time (s): ").grid(row=7, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Response Factor : ").grid(row=8, column=2, padx=85, pady=2)
        Label(self.VOOR_mode, text="Recovery Time (mins) : ").grid(row=9, column=2, padx=85, pady=2)
        Button(self.VOOR_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_VOOR).grid(row=10, column=3, pady=2)

    def send_VOOR(self, lrl, url, va, vpw, max, threshold, rxn, response, recovery):
        mode = Mode(self.userName, 6)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.VOOR_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))
                        if error == False:
                            error, errormsg = check_MAX_SENSE_RATE(int(max.get()),int(url.get()),int(lrl.get()))
                            if error == False:
                                error, errormsg = check_RXN_TIME(int(rxn.get()))
                                if error == False:
                                    error, errormsg = check_RESPONSE(int(response.get()))
                                    if error == False:
                                        error, errormsg = check_RECOVERY(int(recovery.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.set_MAX_SENSE_RATE(int(max.get()))
                mode.set_ACT_THRESHOLD(threshold.get())
                mode.set_REACTION_TIME(int(rxn.get()))
                mode.set_RESPONSE_FACTOR(int(response.get()))
                mode.set_RECOVERY_TIME(int(recovery.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.VOOR_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=11, columnspan=2, pady=15)

                    Label(self.VOOR_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.VOOR_mode, text= round(echoFromSim[5], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[3]).grid(row=4, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[16]).grid(row=5, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[12]).grid(row=6, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[13]).grid(row=7, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[14]).grid(row=8, column=3,  pady=2)
                    Label(self.VOOR_mode, text= echoFromSim[15]).grid(row=9, column=3,  pady=2)
                
            else:
                self.message.destroy()
                self.message = Label(self.VOOR_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),
                                     fg="red")
                self.message.grid(row=11, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.VOOR_mode, 
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=11, columnspan=2, pady=15)
    
    def retrieve_VOOR(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.VOOR_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[5]).grid(row=3, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[3]).grid(row=4, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[16]).grid(row=5, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[12]).grid(row=6, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[13]).grid(row=7, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[14]).grid(row=8, column=3,  pady=2)
        Label(self.VOOR_mode, text= fromSim[15]).grid(row=9, column=3,  pady=2)
        Label(self.VOOR_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=10, column=2,  pady=2)

    # AAIR MODE PARAMETERS
    def set_mode_AAIR(self):
        # set up AAIR frame inside of pm_params frame
        self.mode_name.config(text="AAIR")
        self.AAIR_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.AAIR_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.AAIR_mode)
        url = StringVar(self.AAIR_mode)
        aa = StringVar(self.AAIR_mode)
        apw = StringVar(self.AAIR_mode)
        sense = StringVar(self.AAIR_mode)
        arp = StringVar(self.AAIR_mode)
        pvarp = StringVar(self.AAIR_mode)
        max = StringVar(self.AAIR_mode)
        threshold = StringVar(self.AAIR_mode)
        rxn = StringVar(self.AAIR_mode)
        response = StringVar(self.AAIR_mode)
        recovery = StringVar(self.AAIR_mode)

        Label(self.AAIR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_url = Entry(self.AAIR_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.AAIR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.AAIR_mode, textvariable=url).grid(row=2, column=1)

        Label(self.AAIR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.AAIR_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.AAIR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.AAIR_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.AAIR_mode, text="ARP (ms): ").grid(row=5, column=0, pady=2)
        enter_arp = Entry(self.AAIR_mode, textvariable=arp).grid(row=5, column=1)

        Label(self.AAIR_mode, text="Post VARP (ms): ").grid(row=6, column=0, pady=2)
        enter_pvarp = Entry(self.AAIR_mode, textvariable=pvarp).grid(row=6, column=1)

        thresh_vals = ("V-Low (1)", "Low (2)", "Med-Low (3)", "Med (4)", "Med-High (5)", "High (6)", "V-High (7)")
        Label(self.AAIR_mode, text="Activity Threshold : ").grid(row=7, column=0, pady=2)
        enter_threshold = Spinbox(self.AAIR_mode, values=thresh_vals, state="readonly", textvariable=threshold).grid(
            row=7, column=1)

        Label(self.AAIR_mode, text="Max Sensor Rate (ppm): ").grid(row=8, column=0, pady=2)
        enter_max = Entry(self.AAIR_mode, textvariable=max).grid(row=8, column=1)

        Label(self.AAIR_mode, text="Reaction Time (s): ").grid(row=9, column=0, pady=2)
        enter_rxn = Entry(self.AAIR_mode, textvariable=rxn).grid(row=9, column=1)

        Label(self.AAIR_mode, text="Response Factor : ").grid(row=10, column=0, pady=2)
        enter_response = Entry(self.AAIR_mode, textvariable=response).grid(row=10, column=1)

        Label(self.AAIR_mode, text="Recovery Time (mins) : ").grid(row=11, column=0, pady=2)
        enter_recovery = Entry(self.AAIR_mode, textvariable=recovery).grid(row=11, column=1)

        Label(self.AAIR_mode, text= "Atrial Sensitivity (V): ").grid(row=12, column=0, pady=2)
        enter_sense = Entry(self.AAIR_mode, textvariable=sense).grid(row=12, column=1)

        Button(self.AAIR_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_AAIR(lrl, url, aa, apw, max, threshold, rxn, response,
                                              recovery, arp, pvarp, sense)).grid(row=13, column=1, pady=20)

        Label(self.AAIR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="ARP (ms): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Post VARP (ms): ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Activity Threshold : ").grid(row=7, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Max Sensor Rate (ppm): ").grid(row=8, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Reaction Time (s): ").grid(row=9, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Response Factor : ").grid(row=10, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Recovery Time (mins) : ").grid(row=11, column=2, padx=85, pady=2)
        Label(self.AAIR_mode, text="Atrial Sensitivity (V): ").grid(row=12, column=2, padx=85, pady=2)
        Button(self.AAIR_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_AAIR).grid(row=13, column=3, pady=2)


    def send_AAIR(self, lrl, url, aa, apw, max, threshold, rxn, response, recovery, arp, pvarp, sense):
        mode = Mode(self.userName, 9)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.AAIR_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_AA(float(aa.get()))
                    if error == False:
                        error, errormsg = check_APW(int(apw.get()))
                        if error == False:
                            error, errormsg = check_ARP(int(lrl.get()), int(arp.get()))
                            if error == False:
                                error, errormsg = check_PVARP(int(pvarp.get()))
                                if error == False:
                                    error, errormsg = check_MAX_SENSE_RATE(int(max.get()),int(url.get()),int(lrl.get()))            
                                    if error == False:
                                        error, errormsg = check_RXN_TIME(int(rxn.get()))
                                        if error == False:
                                            error, errormsg = check_RESPONSE(int(response.get()))
                                            if error == False:
                                                error, errormsg = check_RECOVERY(int(recovery.get()))
                                                if error == False:
                                                    error, errormsg = check_AS(float(sense.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.set_ARP(int(arp.get()))
                mode.set_PVARP(int(pvarp.get()))
                mode.set_ACT_THRESHOLD(threshold.get())
                mode.set_MAX_SENSE_RATE(int(max.get()))
                mode.set_REACTION_TIME(int(rxn.get()))
                mode.set_RESPONSE_FACTOR(int(response.get()))
                mode.set_RECOVERY_TIME(int(recovery.get()))
                mode.set_AS(float(sense.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.AAIR_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=14, columnspan=2, pady=15)

                    Label(self.AAIR_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.AAIR_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[10]).grid(row=5, column=3,  pady=2)
                    Label(self.AAIR_mode, text= "").grid(row=6, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[12]).grid(row=7, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[16]).grid(row=8, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[13]).grid(row=9, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[14]).grid(row=10, column=3,  pady=2)
                    Label(self.AAIR_mode, text= echoFromSim[15]).grid(row=11, column=3,  pady=2)
                    Label(self.AAIR_mode, text= round(echoFromSim[8], 2)).grid(row=12, column=3,  pady=2)
                
            else:
                self.message.destroy()
                self.message = Label(self.AAIR_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),
                                     fg="red")
                self.message.grid(row=14, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.AAIR_mode, 
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=14, columnspan=2, pady=15)

    def retrieve_AAIR(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.AAIR_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[10]).grid(row=5, column=3,  pady=2)
        Label(self.AAIR_mode, text= "").grid(row=6, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[12]).grid(row=7, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[16]).grid(row=8, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[13]).grid(row=9, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[14]).grid(row=10, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[15]).grid(row=11, column=3,  pady=2)
        Label(self.AAIR_mode, text= fromSim[8]).grid(row=12, column=3,  pady=2)
        Label(self.AAIR_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=13, column=2,  pady=2)

    
    # VVIR MODE PARAMETERS
    def set_mode_VVIR(self):
        # set up VVIR frame inside of pm_params frame
        self.mode_name.config(text="VVIR")
        self.VVIR_mode = Frame(self.pmParams)

        # forget previous mode frame and set this vs new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.VVIR_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.VVIR_mode)
        url = StringVar(self.VVIR_mode)
        va = StringVar(self.VVIR_mode)
        vpw = StringVar(self.VVIR_mode)
        sense = StringVar(self.VVIR_mode)
        vrp = StringVar(self.VVIR_mode)
        max = StringVar(self.VVIR_mode)
        threshold = StringVar(self.VVIR_mode)
        rxn = StringVar(self.VVIR_mode)
        response = StringVar(self.VVIR_mode)
        recovery = StringVar(self.VVIR_mode)

        Label(self.VVIR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_url = Entry(self.VVIR_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.VVIR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.VVIR_mode, textvariable=url).grid(row=2, column=1)

        Label(self.VVIR_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_va = Entry(self.VVIR_mode, textvariable=va).grid(row=3, column=1)

        Label(self.VVIR_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_vpw = Entry(self.VVIR_mode, textvariable=vpw).grid(row=4, column=1)

        Label(self.VVIR_mode, text="VRP (ms): ").grid(row=5, column=0, pady=2)
        enter_vrp = Entry(self.VVIR_mode, textvariable=vrp).grid(row=5, column=1)

        Label(self.VVIR_mode, text="Ventricular Sensitivity (V): ").grid(row=6, column=0, padx=85, pady=2)
        enter_sense = Entry(self.VVIR_mode, textvariable=sense).grid(row=6, column=1)

        thresh_vals = ("V-Low (1)", "Low (2)", "Med-Low (3)", "Med (4)", "Med-High (5)", "High (6)", "V-High (7)")
        Label(self.VVIR_mode, text="Activity Threshold : ").grid(row=7, column=0, pady=2)
        enter_threshold = Spinbox(self.VVIR_mode, values=thresh_vals, state="readonly",
                                  textvariable=threshold).grid(row=7, column=1)

        Label(self.VVIR_mode, text="Max Sensor Rate (ppm): ").grid(row=8, column=0, pady=2)
        enter_max = Entry(self.VVIR_mode, textvariable=max).grid(row=8, column=1)

        Label(self.VVIR_mode, text="Reaction Time (s): ").grid(row=9, column=0, pady=2)
        enter_rxn = Entry(self.VVIR_mode, textvariable=rxn).grid(row=9, column=1)

        Label(self.VVIR_mode, text="Response Factor : ").grid(row=10, column=0, pady=2)
        enter_response = Entry(self.VVIR_mode, textvariable=response).grid(row=10, column=1)

        Label(self.VVIR_mode, text="Recovery Time (mins) : ").grid(row=11, column=0, pady=2)
        enter_recovery = Entry(self.VVIR_mode, textvariable=recovery).grid(row=11, column=1)

        Button(self.VVIR_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_VVIR(lrl, url, va, vpw, max, threshold, rxn, response,
                                              recovery, vrp, sense)).grid(row=12, column=1, pady=20)
        
        Label(self.VVIR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Ventricular Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Ventricular Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="VRP (ms): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Ventricular Sensitivity (V): ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Activity Threshold :").grid(row=7, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Max Sensor Rate (ppm): ").grid(row=8, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Reaction Time (s): ").grid(row=9, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Response Factor : ").grid(row=10, column=2, padx=85, pady=2)
        Label(self.VVIR_mode, text="Recovery Time (mins) : ").grid(row=11, column=2, padx=85, pady=2)
        Button(self.VVIR_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_VVIR).grid(row=12, column=3, pady=2)

    def send_VVIR(self, lrl, url, va, vpw, max, threshold, rxn, response, recovery, vrp, sense):
        mode = Mode(self.userName, 8)
        errormsg = ""
        error = False

        # initialize message label
        self.message.destroy()
        self.message = Label(self.VVIR_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))
                        if error == False:
                            error, errormsg = check_VRP(int(lrl.get()), int(vrp.get()))
                            if error == False:
                                error, errormsg = check_MAX_SENSE_RATE(int(max.get()),int(url.get()),int(lrl.get()))
                                if error == False:
                                    error, errormsg = check_RXN_TIME(int(rxn.get()))
                                    if error == False:
                                        error, errormsg = check_RESPONSE(int(response.get()))
                                        if error == False:
                                            error, errormsg = check_RECOVERY(int(recovery.get()))
                                            if error == False:
                                                error, errormsg = check_VS(float(sense.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.set_VRP(int(vrp.get()))
                mode.set_ACT_THRESHOLD(threshold.get())
                mode.set_MAX_SENSE_RATE(int(max.get()))
                mode.set_REACTION_TIME(int(rxn.get()))
                mode.set_RESPONSE_FACTOR(int(response.get()))
                mode.set_RECOVERY_TIME(int(recovery.get()))
                mode.set_VS(float(sense.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.VVIR_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=13, columnspan=2, pady=15)

                    Label(self.VVIR_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.VVIR_mode, text= round(echoFromSim[5], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[3]).grid(row=4, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[9]).grid(row=5, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[7]).grid(row=6, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[12]).grid(row=7, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[16]).grid(row=8, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[13]).grid(row=9, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[14]).grid(row=10, column=3,  pady=2)
                    Label(self.VVIR_mode, text= echoFromSim[15]).grid(row=11, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.VVIR_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15),
                                     fg="red")
                self.message.grid(row=13, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.VVIR_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=13, columnspan=2, pady=15)

    def retrieve_VVIR(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.VVIR_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[5]).grid(row=3, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[3]).grid(row=4, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[9]).grid(row=5, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[7]).grid(row=6, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[12]).grid(row=7, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[16]).grid(row=8, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[13]).grid(row=9, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[14]).grid(row=10, column=3,  pady=2)
        Label(self.VVIR_mode, text= fromSim[15]).grid(row=11, column=3,  pady=2)
        Label(self.VVIR_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=12, column=2,  pady=2)

# DOOR MODE PARAMETERS
    def set_mode_DOOR(self):
        # set up DOOR frame inside of pm_params frame
        self.mode_name.config(text="DOOR")
        self.DOOR_mode = Frame(self.pmParams)

        # forget previous mode frame and set this as new one
        self.mode_frame.grid_forget()
        self.mode_frame = self.DOOR_mode
        self.mode_frame.grid(row=1, column=0, columnspan=4)

        # parameters for this mode to be modified
        lrl = StringVar(self.DOOR_mode)
        url = StringVar(self.DOOR_mode)
        va = StringVar(self.DOOR_mode)
        vpw = StringVar(self.DOOR_mode)
        aa = StringVar(self.DOOR_mode)
        apw = StringVar(self.DOOR_mode)
        av = StringVar(self.DOOR_mode)
        max = StringVar(self.DOOR_mode)
        threshold = StringVar(self.DOOR_mode)
        rxn = StringVar(self.DOOR_mode)
        response = StringVar(self.DOOR_mode)
        recovery = StringVar(self.DOOR_mode)

        Label(self.DOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=0, padx=85, pady=2)
        enter_lrl = Entry(self.DOOR_mode, textvariable=lrl).grid(row=1, column=1)

        Label(self.DOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=0, pady=2)
        enter_url = Entry(self.DOOR_mode, textvariable=url).grid(row=2, column=1)

        Label(self.DOOR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=0, pady=2)
        enter_aa = Entry(self.DOOR_mode, textvariable=aa).grid(row=3, column=1)

        Label(self.DOOR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=0, pady=2)
        enter_apw = Entry(self.DOOR_mode, textvariable=apw).grid(row=4, column=1)

        Label(self.DOOR_mode, text="Ventrical Amplitude (V): ").grid(row=5, column=0, pady=2, padx=50)
        enter_va = Entry(self.DOOR_mode, textvariable=va).grid(row=5, column=1)

        Label(self.DOOR_mode, text="Ventrical Pulse Width (ms): ").grid(row=6, column=0, pady=2, padx=50)
        enter_vpw = Entry(self.DOOR_mode, textvariable=vpw).grid(row=6, column=1)

        thresh_vals = ("V-Low (1)", "Low (2)", "Med-Low (3)", "Med (4)", "Med-High (5)", "High (6)", "V-High (7)")
        Label(self.DOOR_mode, text="Activity Threshold : ").grid(row=7, column=0, pady=2)
        enter_threshold = Spinbox(self.DOOR_mode, values=thresh_vals, state="readonly", textvariable=threshold).grid(row=7, column=1)

        Label(self.DOOR_mode, text="Fixed AV Delay(ms): ").grid(row=8, column=0, pady=2, padx=50)
        enter_av = Entry(self.DOOR_mode, textvariable=av).grid(row=8, column=1)

        Label(self.DOOR_mode, text="Reaction Time (s): ").grid(row=9, column=0, pady=2)
        enter_rxn = Entry(self.DOOR_mode, textvariable=rxn).grid(row=9, column=1)

        Label(self.DOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=10, column=0, pady=2)
        enter_max = Entry(self.DOOR_mode, textvariable=max).grid(row=10, column=1)

        Label(self.DOOR_mode, text="Response Factor : ").grid(row=11, column=0, pady=2)
        enter_response = Entry(self.DOOR_mode, textvariable=response).grid(row=11, column=1)

        Label(self.DOOR_mode, text="Recovery Time (mins) : ").grid(row=12, column=0, pady=2)
        enter_recovery = Entry(self.DOOR_mode, textvariable=recovery).grid(row=12, column=1)

        Button(self.DOOR_mode, text="Update", padx=20, pady=10,
               command=lambda: self.send_DOOR(lrl, url, va, vpw, aa, apw, av, threshold, rxn, max, response, recovery)).grid(row=13, column=1, pady=20)
       
        Label(self.DOOR_mode, text="Lower Rate Limit (ppm): ").grid(row=1, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Upper Rate Limit (ppm): ").grid(row=2, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Atrial Amplitude (V): ").grid(row=3, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Atrial Pulse Width (ms): ").grid(row=4, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Ventricular Amplitude (V): ").grid(row=5, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Ventricular Pulse Width (ms): ").grid(row=6, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Activity Threshold :").grid(row=7, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Fixed AV Delay(ms): ").grid(row=8, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Reaction Time (s): ").grid(row=9, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Max Sensor Rate (ppm): ").grid(row=10, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Response Factor : ").grid(row=11, column=2, padx=85, pady=2)
        Label(self.DOOR_mode, text="Recovery Time (mins) : ").grid(row=12, column=2, padx=85, pady=2)
        Button(self.DOOR_mode, text="Get Current Settings", padx=20, pady=10, command = self.retrieve_DOOR).grid(row=13, column=3, pady=2)

    def send_DOOR(self, lrl, url, va, vpw, aa, apw, av, threshold, rxn, max, response, recovery):
        mode = Mode(self.userName, 10)
        errormsg = ""
        error = True

        # initialize message label
        self.message.destroy()
        self.message = Label(self.DOOR_mode)
        self.message.grid()

        # make sure values entered are valid
        try:
            error, errormsg = check_LRL(int(lrl.get()))
            if error == False:
                error, errormsg = check_URL(int(url.get()),int(lrl.get()))
                if error == False:
                    error, errormsg = check_VA(float(va.get()))
                    if error == False:
                        error, errormsg = check_VPW(int(vpw.get()))
                        if error == False:
                            error, errormsg = check_AA(float(aa.get()))
                            if error == False:
                                error, errormsg = check_APW(int(apw.get()))
                                if error == False:
                                    error, errormsg = check_AV_DELAY(int(av.get()))
                                    if error == False:
                                        error, errormsg = check_RXN_TIME(int(rxn.get()))
                                        if error == False:
                                            error, errormsg = check_MAX_SENSE_RATE(int(max.get()),int(url.get()),int(lrl.get()))
                                            if error == False:
                                                error, errormsg = check_RESPONSE(int(response.get()))
                                                if error == False:
                                                    error, errormsg = check_RECOVERY(int(recovery.get()))

            if error == False:
                mode.set_LRL(int(lrl.get()))
                mode.set_URL(int(url.get()))
                mode.set_VA(float(va.get()))
                mode.set_VPW(int(vpw.get()))
                mode.set_AA(float(aa.get()))
                mode.set_APW(int(apw.get()))
                mode.set_FIXED_AV_DELAY(int(av.get()))
                mode.set_MAX_SENSE_RATE(int(max.get()))
                mode.set_ACT_THRESHOLD(threshold.get())
                mode.set_REACTION_TIME (int(rxn.get()))
                mode.set_RESPONSE_FACTOR(int(response.get()))
                mode.set_RECOVERY_TIME(int(recovery.get()))
                mode.write_params(self.serial)
                echoFromSim = mode.read_echo(self.serial)

                if (mode.verify_write(echoFromSim)):
                    errormsg = "Data retrieved from pacemaker doesn't match data sent from DCM"

                else:
                    self.message.destroy()
                    self.message = Label(self.DOOR_mode, text="Update Success!", font=("Calibri", 25), fg="green")
                    self.message.grid(row=14, columnspan=2, pady=15)

                    Label(self.DOOR_mode, text= echoFromSim[2]).grid(row=1, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[1]).grid(row=2, column=3,  pady=2)
                    Label(self.DOOR_mode, text= round(echoFromSim[6], 2)).grid(row=3, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[4]).grid(row=4, column=3,  pady=2)
                    Label(self.DOOR_mode, text= round(echoFromSim[5], 2)).grid(row=5, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[3]).grid(row=6, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[12]).grid(row=7, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[11]).grid(row=8, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[13]).grid(row=9, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[16]).grid(row=10, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[14]).grid(row=11, column=3,  pady=2)
                    Label(self.DOOR_mode, text= echoFromSim[15]).grid(row=12, column=3,  pady=2)

            else:
                self.message.destroy()
                self.message = Label(self.DOOR_mode, text=f"Update Failed: \n {errormsg}", font=("Calibri", 15), fg="red")
                self.message.grid(row=14, columnspan=2, pady=15)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            self.message.destroy()
            self.message = Label(self.DOOR_mode,
                                 text="Update Failed: \nPlease use floats for ventricular amplitude/sensitivity\n"
                                      "Please use integers for all other values\n"
                                      "Make sure you have connected to the UART COM", font=("Calibri", 15), fg="red")
            self.message.grid(row=14, columnspan=2, pady=15)

    def retrieve_DOOR(self):
        self.serial.ser.open()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.serial.ser.write(packed)
        unpacked = struct.unpack('<BBBIIBBffffIIIBBBBB', packed)
        print(unpacked)

        sleep(1)
        print("In waiting: " + str(self.serial.ser.in_waiting))
        read = self.serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        self.serial.ser.close()

        Label(self.DOOR_mode, text= fromSim[2]).grid(row=1, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[1]).grid(row=2, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[6]).grid(row=3, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[4]).grid(row=4, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[5]).grid(row=5, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[3]).grid(row=6, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[12]).grid(row=7, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[11]).grid(row=8, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[13]).grid(row=9, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[16]).grid(row=10, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[14]).grid(row=11, column=3,  pady=2)
        Label(self.DOOR_mode, text= fromSim[15]).grid(row=12, column=3,  pady=2)
        Label(self.DOOR_mode, text= "Current Mode number: " + str(fromSim[0])).grid(row=13, column=2,  pady=2)