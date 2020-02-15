# The main file
from Data_Logger import *
from Kalman import *
from State_Manager import *
from PID import *
from Servo import *

use_bno = 0

#TODO: consider adding parallelization
dlogger = DataLogger(use_bno)
dfilter = DataFilter(use_bno)
piddle  = PID()
state_machine = StateManager()
servo = Servo()

while True:
    #Read in data from the data logger
    dlogger.read_data()
    dlogger.write_data()
    raw_data = dlogger.get_data()

    #Filter the data
    t,theta,y,v,a = dfilter.process_data(raw_data)

    #Check flight state
    state_machine.check_transition(y,v,a)
    state = state_machine.get_state()

    #do PID stuff if necessary
    if state == 'Burnout':
        if not piddle.initialized:
            piddle.init_readings(y,v)
        
        piddle.PID_step(y,v)
        phi = piddle.get_phi()
    elif state == 'Overshoot':
        phi = piddle.maxPhi
    else:
        phi = 0

    #actuate servo to phi radians
    servo.rotate(phi)

    print(y,v,a)
