from serialcom import*
import serial
import struct


class ALL():
    def __init__(self, user):
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
        self.MODE = 0

        self.paramList = []
        self.user = user
        self.data_file = ""

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
        if value == "V-Low":
            self.ACT_THRESHOLD = 0
        if value == "Low":
            self.ACT_THRESHOLD = 1
        if value == "Med-Low":
            self.ACT_THRESHOLD = 2
        if value == "Med":
            self.ACT_THRESHOLD = 3
        if value == "Med-High":
            self.ACT_THRESHOLD = 4
        if value == "High":
            self.ACT_THRESHOLD = 5
        if value == "V-High":
            self.ACT_THRESHOLD = 6

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
        file = open(self.data_file, "r")
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
        file = open(self.data_file, "w")
        file.writelines(old_data)
        file.close()

        file = open(self.data_file, "a")
        file.write(self.user + "\n")
        for params in self.paramList:
            file.write(str(params) + ",")
        file.write("\n")
        file.close()

        serial.ser.open()
        self.packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,14,1,self.URL,self.LRL,self.VPW,self.APW,self.VA,self.AA,self.VS,self.AS,self.VRP,self.ARP,self.FIXED_AV_DELAY,self.ACT_THRESHOLD,self.REACTION_TIME,self.RESPONSE_FACTOR,self.RECOVERY_TIME,self.MAX_SENSE_RATE)
        serial.ser.write(self.packed)
    
    def read_echo(self, serial):
        read = serial.ser.readline(160)
        print(read)

        fromSim = struct.unpack('<BIIBBffffIIIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', read)
        print(fromSim)

        serial.ser.close()

    def updateParamList(self):
        self.paramList = []

class AOO(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.AA = 0
        self.APW = 0

        self.paramList = [self.LRL, self.URL, self.AA, self.APW]
        self.user = user
        self.data_file = "aoo_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW]

class VOO(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.VA = 0
        self.VPW = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW]
        self.user = user
        self.data_file = "voo_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW]

class AAI(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.AA = 0
        self.APW = 0
        self.ARP = 0
        self.AS = 0
        self.PVARP = 0

        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.ARP, self.AS, self.PVARP]
        self.user = user
        self.data_file = "aai_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.ARP, self.AS, self.PVARP]


class VVI(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.VA = 0
        self.VPW = 0
        self.VRP = 0
        self.VS = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VRP, self.VS]
        self.user = user
        self.data_file = "vvi_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VRP, self.VS]

class DOO(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.AA = 0
        self.APW = 0
        self.VA = 0
        self.VPW = 0
        self.FIXED_AV_DELAY = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.AA, self.APW, self.FIXED_AV_DELAY]
        self.user = user
        self.data_file = "doo_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.AA, self.APW, self.FIXED_AV_DELAY]

class AOOR(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.AA = 0
        self.APW = 0
        self.MAX_SENSE_RATE = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0

        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.MAX_SENSE_RATE, self.ACT_THRESHOLD,
                          self.REACTION_TIME, self.RESPONSE_FACTOR, self.RECOVERY_TIME]
        self.user = user
        self.data_file = "aoor_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.MAX_SENSE_RATE, self.ACT_THRESHOLD,
                          self.REACTION_TIME, self.RESPONSE_FACTOR, self.RECOVERY_TIME]

class AAIR(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.AA = 0
        self.APW = 0
        self.AS = 0
        self.ARP = 0
        self.PVARP = 0
        self.MAX_SENSE_RATE = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0

        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.AS, self.ARP, self.PVARP, self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME,
                          self.RESPONSE_FACTOR, self.RECOVERY_TIME]
        self.user = user
        self.data_file = "aair_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.AS, self.ARP, self.PVARP, self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME,
                          self.RESPONSE_FACTOR, self.RECOVERY_TIME]

class VOOR(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.VA = 0
        self.VPW = 0
        self.MAX_SENSE_RATE = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.MAX_SENSE_RATE, self.ACT_THRESHOLD,
                          self.REACTION_TIME, self.RESPONSE_FACTOR, self.RECOVERY_TIME]
        self.user = user
        self.data_file = "voor_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.MAX_SENSE_RATE, self.ACT_THRESHOLD,
                          self.REACTION_TIME, self.RESPONSE_FACTOR, self.RECOVERY_TIME]

class VVIR(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.VA = 0
        self.VPW = 0
        self.VS = 0
        self.VRP = 0
        self.MAX_SENSE_RATE = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VS, self.VRP, self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME,
                          self.RESPONSE_FACTOR, self.RECOVERY_TIME]
        self.user = user
        self.data_file = "vvir_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VS, self.VRP, self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME,
                          self.RESPONSE_FACTOR, self.RECOVERY_TIME]

class DOOR(ALL):
    def __init__(self, user):
        self.LRL = 0
        self.URL = 0
        self.VA = 0
        self.VPW = 0
        self.AA = 0
        self.APW = 0
        self.FIXED_AV_DELAY = 0
        self.MAX_SENSE_RATE = 0
        self.ACT_THRESHOLD = 0
        self.REACTION_TIME = 0
        self.RESPONSE_FACTOR = 0
        self.RECOVERY_TIME = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.AA ,self.APW, self.FIXED_AV_DELAY,
                          self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME, self.RESPONSE_FACTOR,
                          self.RECOVERY_TIME]
        self.user = user
        self.data_file = "door_data.txt"

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.AA, self.APW, self.FIXED_AV_DELAY,
                          self.MAX_SENSE_RATE, self.ACT_THRESHOLD, self.REACTION_TIME, self.RESPONSE_FACTOR,
                          self.RECOVERY_TIME]