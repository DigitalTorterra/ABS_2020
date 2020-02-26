"""
Usage: automatically initializes sensors upon startup
Methods:
zero_mpl-should call periodically before launch
read_data-queries all the sensor data
write_data-writes current data to file
get_data-returns the data in the following format:
(timestamp, euler, altitude, acceleration)

"""


#Import libraries here
import time,sys
import board,busio
import glob

import adafruit_mpl3115a2
from Adafruit_BNO055 import BNO055 #Import the new library 
import adafruit_adxl34x
from gpiozero import LED

import csv




class DataLogger():
    def __init__(self,use_BNO=True):
        #Constants
        self.delay_time = .001
        self.use_BNO = use_BNO

        with open('Overshoot_to_ideal.csv') as f:
            reader = csv.reader(f)
            self.data = list(reader)

        self.row = 0
        self.t = 0

    def read_data(self):
        self.row += 1

    def get_data(self):
        return float(self.data[self.row][0]),[0,0,0],float(self.data[self.row][1]),(float(self.data[self.row][2]),0,0)
