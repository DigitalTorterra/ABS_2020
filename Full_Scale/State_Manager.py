#Manages state transitions for the ABS system
from gpiozero import LED

class StateManager():
    def __init__(self):
        self.state_list = ['Armed','Launched','Burnout','Apogee','Overshoot','Landed']
        self.current_state = 0
        
        self.liftoff_height = 30
        self.liftoff_accel = 40

        self.burnout_accel = -6.125
        self.burnout_height = 305

        self.apogee = 1354
        self.led = LED(21)

    #Takes in input data from Kalman Filter and adjusts the current state if necessary
    def check_transition(self,height,velocity,acceleration):
        #Use the syntax "self.current_state" to get the number representing the current state
        #Use the syntax "self.get_state()" to get the name of the state as a string
        #Use the syntax "self.current_state" to get the number representing the current state
        #Use the syntax "self.get_state()" to get the name of the state as a string
        next_state = self.current_state

        if self.current_state == 0: #Armed
            self.led.on()
            if acceleration > self.liftoff_accel or height > self.liftoff_height:
                next_state = 1

        if self.current_state == 1: #Launched
            if acceleration < self.burnout_accel or height > self.burnout_height:
                next_state = 2

        if self.current_state == 2: #Burnout
            if acceleration > self.burnout_accel:
                next_state = 1
                #Return to the Launched stage because the noises in acceleration
            if velocity < 0:
                next_state = 3
                #Change to the Apogee stage
            if height > self.apogee and velocity > 0:
                next_state = 4
                #Change to the Overshot stage
                
        if self.current_state == 3: #Apogee
            self.led.on()
            if velocity > 0:
                next_state = 2
                #Return to the Burnout stage if the velocity is still greater than 0
            if velocity <= 10 and height <=10 and acceleration <=0:
                next_state = 5
                #Change to the Landed Stage
                
        if self.current_state == 4: #Overshot
            if velocity <= 0:
                next_state = 3
            #Change to Apogee stage

        self.current_state = next_state
        self.led.off()

    def get_state(self):
        return self.state_list[self.current_state]
