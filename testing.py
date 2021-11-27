import serial

stuff = serial.Serial()
thing = stuff.tools.list_ports.comports(include_links=False)
print(thing)