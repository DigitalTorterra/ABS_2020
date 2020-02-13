import RPI.GPIO as GPIO
from time import sleep

class Servo():
    def __init__(self):
        #set rotation bounds
        self.min_phi = 0
        self.max_phi = 67.5

        self.min_dc = 1400
        self.max_dc = 2100
        
        GPIO.setmode(GPIO.BOARD)

        #Set up PWM pin
        GPIO.setup(32,GPIO.OUT)
        self.p = GPIO.PWM(32,50)
        self.p.start(0)

    def rotate(self,phi):
        #write some conversion between phi and duty cycle
        if phi >= self.min_phi and phi <= self.max_phi:
            norm_phi = (phi-self.min_phi)/(self.max_phi-self.min_phi)
            new_cycle = self.min_dc + norm_phi*(self.max_dc-self.min_dc)
        
            self.p.ChangeDutyCycle(new_cycle)
        else:
            print('Invalid rotation given')

    def __del__(self):
        self.p.stop()
        GPIO.cleanup()
