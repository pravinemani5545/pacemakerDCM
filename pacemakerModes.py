class AOO:
    def __init__(self, user):
        self.LRL = 0        # lower rate limit
        self.URL = 0        # upper rate limit
        self.AA = 0         # atrial amplitude
        self.APW = 0        # atrial pulse width

        self.paramList = [self.LRL, self.URL, self.AA, self.APW]
        self.user = user
        self.data_file = "aoo_data.txt"

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

    def write_params(self):
        file = open(self.data_file, "r")
        data = file.readlines()
        file.close()

        old_data = []
        self.updateParamList()

        # keep other patients' data stored while ignoring current patient's (old) data
        for i in range(0, len(data), 2):
            if (data[i] == (self.user+"\n")):
                continue;

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

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW]

class VOO(AOO):
    def __init__(self, user):
        self.LRL = 0        # lower rate limit
        self.URL = 0        # upper rate limit
        self.VA = 0         # ventricular amplitude
        self.VPW = 0        # ventricular pulse width

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW]
        self.user = user
        self.data_file = "voo_data.txt"

    def set_VA(self, value):
        self.VA = value

    def get_VA(self):
        return self.VA

    def set_VPW(self, value):
        self.VPW = value

    def get_VPW(self):
        return self.VPW

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW]

class AAI(AOO):

    def __init__(self, user):
        self.LRL = 0        # lower rate limit
        self.URL = 0        # upper rate limit
        self.AA = 0         # atrial amplitude
        self.APW = 0        # atrial pulse width
        self.ARP = 0

        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.ARP]
        self.user = user
        self.data_file = "aai_data.txt"

    def set_ARP(self, value):
        self.ARP = value

    def get_ARP(self):
        return self.ARP

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.AA, self.APW, self.ARP]

class VVI(VOO):

    def __init__(self, user):
        self.LRL = 0        # lower rate limit
        self.URL = 0        # upper rate limit
        self.VA = 0         # ventricular amplitude
        self.VPW = 0        # ventricular pulse width
        self.VRP = 0

        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VRP]
        self.user = user
        self.data_file = "vvi_data.txt"

    def set_VRP(self, value):
        self.VRP = value

    def get_VRP(self):
        return self.VRP

    def updateParamList(self):
        self.paramList = [self.LRL, self.URL, self.VA, self.VPW, self.VRP]