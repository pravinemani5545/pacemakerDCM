# PARAMETER VALIDITY CHECKS
def check_LRL(lrlval):
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

def check_URL(urlval):
    errormsg = ""
    error = False

    if (urlval > 175 or urlval < 50):
        error = True
        errormsg = "        Please make sure your url value         \n         is between 50-175 ppm.        "

    elif (urlval >= 50 and urlval <= 175 and (urlval % 5 != 0)):
            error = True
            errormsg = "        Please make sure you increment url         \n         by 5 ppm for vals of 50-175 ppm.        "

    return error, errormsg

def check_AA(aaval):
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

def check_VA(vaval):
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

def check_APW(apwval):
    errormsg = ""
    error = False

    if (apwval != 0.05 and not (0.1 <= apwval <= 1.9 and (apwval * 100) % 10 == 0)):
        error = True
        errormsg = "        Please make sure your apw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

    return error, errormsg

def check_VPW(vpwval):
    errormsg = ""
    error = False

    if (vpwval != 0.05 and not (0.1 <= vpwval <= 1.9 and (vpwval * 100) % 10 == 0)):
        error = True
        errormsg = "        Please make sure your vpw value is either         \n         0.05ms or 0.1ms - 1.9ms in increments of 0.1ms.        "

    return error, errormsg

def check_ARP(lrlval, arpval):
    errormsg = ""
    error = False

    if (not (arpval >= 150 and arpval <= 500 and (arpval % 10 == 0))):
        error = True
        errormsg = "        Please make sure your arp value is between          \n         150ms and 500ms in increments of 10ms.        "

    if (60000//lrlval >= arpval):
        error = True
        errormsg = "        Please make sure the pacewidth (lrl value in ms)     \n         is less than the pulse period (arp)"

    return error, errormsg

def check_VRP(lrlval, vrpval):
    errormsg = ""
    error = False

    if (not (vrpval >= 150 and vrpval <= 500 and (vrpval % 10 == 0))):
        error = True
        errormsg = "        Please make sure your vrp value is between          \n         150ms and 500ms in increments of 10 ms.        "

    if (60000//lrlval >= vrpval):
        error = True
        errormsg = "        Please make sure the pacewidth (lrl value in ms)     \n         is less than the pulse period (vrp)"

    return error, errormsg