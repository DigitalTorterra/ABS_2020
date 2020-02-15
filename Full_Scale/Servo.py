import pigpio
from time import sleep
import os

os.system('sudo pigpiod')

class Servo():
    def __init__(self):
        #set rotation bounds
        self.min_phi = 0
        self.max_phi = 67.5

        #2100/2500 (2500==1)
        self.min_dc = int(.6*255)
        self.max_dc = int(.84*255)
        
        self.pin = 12
        self.freq = 400

        #Set up PWM pin
        self.pi = pigpio.pi()
        self.pi.set_PWM_frequency(self.pin,self.freq)

    def rotate(self,phi):
        #write some conversion between phi and duty cycle
        if phi >= self.min_phi and phi <= self.max_phi:
            norm_phi = (phi-self.min_phi)/(self.max_phi-self.min_phi)
            new_cycle = self.min_dc + norm_phi*(self.max_dc-self.min_dc)
            new_cycle = int(new_cycle)

            self.pi.set_PWM_dutycycle(self.pin,new_cycle)
        else:
            print('Invalid rotation given')
    def __del__(self):
        os.system('sudo pkill pigpiod')

