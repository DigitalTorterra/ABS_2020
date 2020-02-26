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
#import adafruit_bno055
from Adafruit_BNO055 import BNO055 #Import the new library 
import adafruit_adxl34x
# from gpiozero import LED




class DataLogger():
    def __init__(self,use_BNO=True):
        #Constants
        self.delay_time = .001
        self.use_BNO = use_BNO

        #I2C Initialization
        self.i2c = busio.I2C(board.SCL, board.SDA)

        if use_BNO:
            #BNO Initialization
            #self.bno = adafruit_bno055.BNO055(self.i2c)
            self.bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
            #self.bno.use_external_crystal = True
        else:
            self.bno_euler = [0,0,0]

        #MPL Initialization
        self.mpl = adafruit_mpl3115a2.MPL3115A2(self.i2c)
        self.mpl._ctrl_reg1 = adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_OS1 |adafruit_mpl3115a2._MPL3115A2_CTRL_REG1_ALT
        time.sleep(1)
        self.zero_mpl()

       # self.led = LED(21)

        #Initialize ADXL
        self.adxl = adafruit_adxl34x.ADXL345(self.i2c)
        self.adxl.range = adafruit_adxl34x.Range.RANGE_16_G
        self.adxl.data_rate = adafruit_adxl34x.DataRate.RATE_100_HZ


    #Take a running sample and create a new reference for the MPL sensor
    def zero_mpl(self):
        total = 0
        for i in range(200):
            #print(i)
            total += self.mpl.pressure
            time.sleep(.005)
        self.mpl.sealevel_pressure = int(total / 200)


    #Read sensor data
    def read_data(self):
       # self.led.on()

        self.timestamp = time.time()

        #Read MPL data
        self.mpl_altitude = self.mpl.altitude
        self.mpl_altitude = self.mpl_altitude if self.mpl_altitude is not None else 0

        if self.use_BNO:
            #Read BNO data
            #bno_accel = bno.acceleration
            #bno_accel = tuple([i if i is not None else 0 for i in bno_accel])
                    
            #bno_mag = bno.magnetic
            #print(bno_mag)
            #bno_mag = tuple([i if i is not None else 0 for i in bno_mag])
            #bno_gyro = bno.gyro
            #bno_gyro = tuple([i if i is not None else 0 for i in bno_gyro])
            self.bno_euler = self.bno.read_euler()
            #print(bno_euler)
            self.bno_euler = tuple([i if i is not None else 0 for i in self.bno_euler])
            #bno_quaternion = bno.quaternion
            #bno_linac = bno.linear_acceleration
            #bno_gravy = bno.gravity
            #bno_gravy = tuple([i if i is not None else 0 for i in bno_gravy])

        #Read ADXL data
        self.adxl_accel = self.adxl.acceleration
        self.adxl_accel = tuple([i if i is not None else 0 for i in self.adxl_accel])

       # self.led.off()


    #Outputs the current data
    def get_data(self):
        return self.timestamp,self.bno_euler,self.mpl_altitude,self.adxl_accel
