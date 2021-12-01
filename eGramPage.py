import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import serial
import struct
import numpy as np
from time import sleep
from tkinter import *

class eGramPage:

    def __init__(self, parent, *args, **kwargs):
        self.eGram = parent
        self.eGram.title("Egram")
        self.eGram.geometry("130x160")
        self.serial = args[0]
        self.DCM = args[1]
        self.username = args[2]

        Button(self.eGram, text="Ventrical ECG", command = self.VEcg).grid(row=1, column=1, pady = 5, ipadx = 15,)
        Button(self.eGram, text="Atrial ECG", command = self.AEcg).grid(row=2, column=1, pady = 5, ipadx = 20)
        Button(self.eGram, text="Atrial & Ventrical ECG", command = self.AVEcg).grid(row=3, column=1, pady = 5)
        Button(self.eGram, text="Return", command = self.backToPm).grid(row=4, column=1, pady = 5)


    def AEcg(self):
                # Parameters
        x_len = 200         # Number of points to display
        y_range = [0, 0.7]  # Range of possible Y values to display

        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = list(range(0, 200))
        ys = [0] * x_len
        ax.set_ylim(y_range)

        # Initialize communication with TMP102

        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color = "r")

        # Add labels
        plt.title('Atrial Electrogram')
        plt.xlabel('Samples (Every 20 ms)')
        plt.ylabel('Voltage (V)')

        self.serial.ser.open()
        sleep(1)

        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        self.serial.ser.read_all()
        print("ser: " + str(self.serial.ser.in_waiting))

        print("connected to: " + self.serial.ser.portstr)
        print()

        print("ser: " + str(self.serial.ser.in_waiting))
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,14,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        print("ser: " + str(self.serial.ser.in_waiting))
        print("opened")
        sleep(0.05)

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            print("ser: " + str(self.serial.ser.in_waiting))
            read = self.serial.ser.read(160)
            fromSim = struct.unpack('ffffffffffffffffffffffffffffffffffffffff', read)
            #print(fromSim)
            print()
            
            # Read temperature (Celsius) from TMP102
            #temp_c = round(tmp102.read_temp(), 2)
            
            # Add y to list
            ys.append(sum(fromSim[21:41])/20)

            # Limit y list to set number of items
            ys = ys[-x_len:]

            # Update line with new Y values
            line.set_ydata(ys)

            return line,

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig,
            animate,
            fargs=(ys,),
            interval=10,
            blit=True)
        plt.tight_layout()
        plt.show()

        self.serial.ser.read_all()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,49,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        self.serial.ser.close()



    def VEcg(self):
                # Parameters
        x_len = 200         # Number of points to display
        y_range = [0, 0.7]  # Range of possible Y values to display

        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = list(range(0, 200))
        ys = [0] * x_len
        ax.set_ylim(y_range)

        # Initialize communication with TMP102

        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color = "b")

        # Add labels
        plt.title('Ventrical Electrogram')
        plt.xlabel('Samples (Every 20 ms)')
        plt.ylabel('Voltage (V)')

        self.serial.ser.open()
        sleep(1)

        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        self.serial.ser.read_all()
        print("ser: " + str(self.serial.ser.in_waiting))

        print("connected to: " + self.serial.ser.portstr)
        print()

        print("ser: " + str(self.serial.ser.in_waiting))
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,14,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        print("ser: " + str(self.serial.ser.in_waiting))
        print("opened")
        sleep(0.05)

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            print("ser: " + str(self.serial.ser.in_waiting))
            read = self.serial.ser.read(160)
            fromSim = struct.unpack('ffffffffffffffffffffffffffffffffffffffff', read)
            #print(fromSim)
            print()
            
            # Read temperature (Celsius) from TMP102
            #temp_c = round(tmp102.read_temp(), 2)
            
            # Add y to list
            ys.append(sum(fromSim[0:20])/20)

            # Limit y list to set number of items
            ys = ys[-x_len:]

            # Update line with new Y values
            line.set_ydata(ys)

            return line,

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig,
            animate,
            fargs=(ys,),
            interval=10,
            blit=True)
        plt.tight_layout()
        plt.show()

        self.serial.ser.read_all()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,49,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        self.serial.ser.close()

    


    def AVEcg(self):

        # Parameters
        x_len = 200         # Number of points to display
        y_range = [0, 0.7]  # Range of possible Y values to display

        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = list(range(0, 200))
        ys = [0] * x_len
        ys2 = [0] * x_len
        ax.set_ylim(y_range)

        # Initialize communication with TMP102

        # Create a blank line. We will update the line in animate
        line1, = ax.plot(xs, ys, color = "b", label = "Ventrical Sigal")
        line2, = ax.plot(xs, ys2, color = "r", label = "Atrial Sigal")

        # Add labels
        plt.title('Atrial and Ventrical Electrogram')
        plt.xlabel('Samples (Every 20 ms)')
        plt.ylabel('Analog Voltage')

        self.serial.ser.open()
        sleep(1)

        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        self.serial.ser.read_all()
        print("ser: " + str(self.serial.ser.in_waiting))

        print("connected to: " + self.serial.ser.portstr)
        print()

        print("ser: " + str(self.serial.ser.in_waiting))
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,14,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        print("ser: " + str(self.serial.ser.in_waiting))
        print("opened")
        sleep(0.05)

        # This function is called periodically from FuncAnimation
        def animate(i, ys, ys2):

            print("ser: " + str(self.serial.ser.in_waiting))
            read = self.serial.ser.read(160)
            fromSim = struct.unpack('ffffffffffffffffffffffffffffffffffffffff', read)
            #print(fromSim)
            print()
            
            # Read temperature (Celsius) from TMP102
            #temp_c = round(tmp102.read_temp(), 2)

            # Add y to list
            ys.append(sum(fromSim[0:20])/20)
            ys2.append(sum(fromSim[20:40])/20)

            # Limit y list to set number of items
            ys = ys[-x_len:]
            ys2 = ys2[-x_len:]

            # Update line with new Y values
            line1.set_ydata(ys)
            line2.set_ydata(ys2)

            return [line1,line2]

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig,
            animate,
            fargs=(ys, ys2),
            interval=10,
            blit=True)

        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()

        self.serial.ser.read_all()
        self.serial.ser.flushInput()
        self.serial.ser.flushOutput()
        packed = struct.pack('<BBBIIBBffffIIIBBBBB',34,49,1,1,1,1,1,1.0,1.0,1.0,1.0,1,1,1,1,1,1,1,1)
        self.serial.ser.write(packed)
        self.serial.ser.close()
    
    
    def backToPm(self):
        self.DCM.deiconify()
        self.eGram.destroy()

