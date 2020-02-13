import RPI.GPIO as GPIO
from time import sleep

class Servo():
    def __init__(self):
        #set rotation bounds
        self.min_phi = 0
        self.max_phi = 67.5
        
        GPIO.setmode(GPIO.BOARD)

        #Set up PWM pin
        GPIO.setup(32,GPIO.OUT)
        self.p = GPIO.PWM(32,50)
        self.p.start(0)

    def rotate(self,phi):
        #write some conversion between phi and duty cycle
        new_cycle = phi
        self.p.ChangeDutyCycle(new_cycle)
    
    def __del__(self):
        self.p.stop()
        GPIO.cleanup()
