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
from gpiozero import LED




class Scribe():
    def __init__(self,use_BNO=True):
        #Constants
        self.delay_time = .001
        self.use_BNO = use_BNO

        #Initialize file and write header
        self.filename = self.gen_filename()
        with open(self.filename,'w') as f:
            f.write("Time ms,")
            #f.write("BNO X Acceleration m/s^2,")
            #f.write("BNO Y Acceleration m/s^2,")
            #f.write("BNO Z Acceleration m/s^2,")
            #f.write("BNO Gyro X rad/s,")    
            #f.write("BNO Gyro Y rad/s,")    
            #f.write("BNO Gyro Z rad/s,")
            if use_BNO: 
                f.write("BNO Euler Angle X,")    
                f.write("BNO Euler Angle Y,")    
                f.write("BNO Euler Angle Z,")    
            #f.write("BNO Magnetometer X,")    
            #f.write("BNO Magnetometer Y,")    
            #f.write("BNO Magnetometer Z,")    
            #f.write("BNO Gravity X,")    
            #f.write("BNO Gravity Y,")    
            #f.write("BNO Gravity Z,")    
            f.write("Altitude m,")    
            f.write("ADXL X Acceleration,")    
            f.write("ADXL Y Acceleration,")    
            f.write("ADXL Z Acceleration,")
            f.write("Kalman Theta,")
            f.write("Kalman Height,")
            f.write("Kalman Acceleration,")
            f.write("Current State,")
            f.write("Phi")
            f.write("\n") 

    #Figure out what to name the file
    def gen_filename(self):
        files = glob.glob('./data*')
        x = 0
        found = False
        while not found:
            found = True
            for file in files:
                num = int(''.join([i for i in file if i in '1234567890']))
                if num == x:
                    found = False

            if not found:
                x += 1
        filename = 'data'+str(x) + '.csv'   

        return filename         


    #Write current sensor data to a file
    def __call__(self,t,euler,alt,adxl,k_theta,k_alt,k_vel,k_accel,state,phi):
        with open(self.filename,'a') as f:
            f.write(str(t)+', ')
            if self.use_BNO:
                f.write('%f, %f, %f,'%euler)
            f.write(str(alt))
            f.write(', %f, %f, %f, '%adxl)
            f.write(str(k_theta)+', ')
            f.write(str(k_alt)+', ')
            f.write(str(k_vel)+', ')
            f.write(str(k_accel)+', ')
            f.write(state+', ')
            f.write(str(phi))
            f.write('\n')
