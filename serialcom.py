import serial
from serial.tools.list_ports import comports

class serialcom():

    def __init__(self):
        ser = serial.Serial()
        ser.baudrate = 115200
        ports = list(comports())
        print(ports)