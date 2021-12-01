from serialcom import*
import serial
import struct
from time import sleep

class Mode():
    def __init__(self, user, mode):
        self.LRL = 0                # lower rate limit
        self.URL = 0                # upper rate limit
        self.AA = 0                 # atrial amplitude
        self.APW = 0                # atrial pulse width
        self.ARP = 0                # atrial refractory period
        self.AS = 0                 # atrial sensitivity
        self.PVARP = 0              # post ventricular atrial refractory period
        self.VA = 0                 # ventricular amplitude
        self.VPW = 0                # ventricular pulse width
        self.VRP = 0                # ventricular refractory period
        self.VS = 0                 # ventricular sensitivity
        self.MAX_SENSE_RATE = 0
        self.FIXED_AV_DELAY = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0
        self.MODE = mode             # current pacemaker mode

        self.paramList = []
        self.user = user

    def set_LRL(self, value):
        self.LRL = value

    def get_LRL(self):
        return self.LRL

    def set_URL(self, value):
        self.URL = value

    def get_URL(self):
        return self.URL

    def set_AA(self, value):
        self.AA = value

    def get_AA(self):
        return self.AA

    def set_APW(self, value):
        self.APW = value

    def get_APW(self):
        return self.APW

    def set_ARP(self, value):
        self.ARP = value

    def get_ARP(self):
        return self.ARP

    def set_AS(self, value):
        self.AS = value

    def get_AS(self):
        return self.AS

    def set_PVARP(self, value):
        self.PVARP = value

    def get_PVARP(self):
        return self.PVARP

    def set_VA(self, value):
        self.VA = value

    def get_VA(self):
        return self.VA

    def set_VPW(self, value):
        self.VPW = value

    def get_VPW(self):
        return self.VPW

    def set_VRP(self, value):
        self.VRP = value

    def get_VRP(self):
        return self.VRP

    def set_VS(self, value):
        self.VS = value

    def get_VS(self):
        return self.VS

    def set_MAX_SENSE_RATE(self, value):
        self.MAX_SENSE_RATE = value

    def get_MAX_SENSE_RATE(self):
        return self.MAX_SENSE_RATE

    def set_FIXED_AV_DELAY(self, value):
        self.FIXED_AV_DELAY = value

    def get_FIXED_AV_DELAY(self):
        return self.FIXED_AV_DELAY

    def set_ACT_THRESHOLD(self, value):
        if value == "V-Low (1)":
            self.ACT_THRESHOLD = 1
        if value == "Low (2)":
            self.ACT_THRESHOLD = 2
        if value == "Med-Low (3)":
            self.ACT_THRESHOLD = 3
        if value == "Med (4)":
            self.ACT_THRESHOLD = 4
        if value == "Med-High (5)":
            self.ACT_THRESHOLD = 5
        if value == "High (6)":
            self.ACT_THRESHOLD = 6
        if value == "V-High (7)":
            self.ACT_THRESHOLD = 7

    def get_ACT_THRESHOLD(self):
        return self.ACT_THRESHOLD

    def set_REACTION_TIME(self, value):
        self.REACTION_TIME = value

    def get_REACTION_TIME(self):
        return self.REACTION_TIME

    def set_RESPONSE_FACTOR(self, value):
        self.RESPONSE_FACTOR = value

    def get_RESPONSE_FACTOR(self):
        return self.RESPONSE_FACTOR

    def set_RECOVERY_TIME(self, value):
        self.RECOVERY_TIME = value

    def get_RECOVERY_TIME(self):
        return self.RECOVERY_TIME

    def write_params(self, serial):
        data_file = self.chooseDataFile(self.MODE)
        file = open(data_file, "r")
        data = file.readlines()
        file.close()

        old_data = []
        self.updateParamList()

        # keep other patients' data stored while ignoring current patient's (old) data
        for i in range(0, len(data), 2):
            if (data[i] == (self.user + "\n")):
                continue

            old_data.append(data[i])
            old_data.append(data[i + 1])

        # write other patients' data back to file and append new data for current patient
        file = open(data_file, "w")
        file.writelines(old_data)
        file.close()

        file = open(data_file, "a")
        file.write(self.user + "\n")
        for params in self.paramList:
            file.write(str(params) + ",")
        file.write("\n")
        file.close()

        # open serial port for writing data to pacemaker
        serial.ser.open()
        serial.ser.flushInput() # flush input buffer
        serial.ser.read_all()   # read data from pacemaker
        serial.ser.flushOutput()    # flush output buffer
        self.packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,81,self.MODE,self.URL,self.LRL,self.VPW,self.APW,self.VA,self.AA,self.VS,self.AS,self.VRP,self.ARP,self.FIXED_AV_DELAY,self.ACT_THRESHOLD,self.REACTION_TIME,self.RESPONSE_FACTOR,self.RECOVERY_TIME,self.MAX_SENSE_RATE)
        serial.ser.write(self.packed)   # send packed data
    
    def read_echo(self, serial):

        sleep(1.3)
        print("In waiting: " + str(serial.ser.in_waiting))
        read = serial.ser.read(160)
        print(read)
        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read) # unpack data from PM
        print(fromSim)

        serial.ser.flushInput()
        serial.ser.read_all()
        serial.ser.flushOutput()
        serial.ser.close()

        return fromSim

    def verify_write(self, echo):

        if (self.MODE != echo[0]):
            return False
        else:
            i = 0 # used to index through echo
            for param in self.paramList:
                if (round(param, 2) != round(echo[i], 2)):
                    return False
                else:
                    i = i + 1

        return True

    def updateParamList(self):
        self.paramList = [self.URL,self.LRL,self.VPW,self.APW,self.VA,self.AA,self.VS,self.AS,self.VRP,
                          self.ARP,self.FIXED_AV_DELAY,self.ACT_THRESHOLD,self.REACTION_TIME,self.RESPONSE_FACTOR,
                          self.RECOVERY_TIME,self.MAX_SENSE_RATE]

    def chooseDataFile(self, mode):
        if (mode == 1):
            return "voo_data.txt"
        elif (mode == 2):
            return "aoo_data.txt"
        elif (mode == 3):
            return "vvi_data.txt"
        elif (mode == 4):
            return "aai_data.txt"
        elif (mode == 5):
            return "doo_data.txt"
        elif (mode == 6):
            return "voor_data.txt"
        elif (mode == 7):
            return "aoor_data.txt"
        elif (mode == 8):
            return "vvir_data.txt"
        elif (mode == 9):
            return "aair_data.txt"
        elif (mode == 10):
            return "door_data.txt"
        else:
            return "ERROR! MODE DOESN'T EXIST!"     # this shouldn't be possible, but if the program
                                                    # ever reaches this point the error is traceable