# The main file
from Fake_Logger import *
from Kalman import *
from State_Manager import *
from PID import *
from Servo import *
from Scribe import *

import time

use_bno = 0

#TODO: consider adding parallelization
dlogger = DataLogger()
dfilter = DataFilter(use_bno)
piddle  = PID()
state_machine = StateManager()
servo = Servo()
scribe = Scribe(use_bno)

print('Successfully Initialized')

while True:
    time.sleep(.001)

    #Read in data from the data logger
    dlogger.read_data()
    raw_data = dlogger.get_data()

    #Filter the data
    t,theta,y,v,a = dfilter.process_data(raw_data)

    #Check flight state
    state_machine.check_transition(y,v,a)
    state = state_machine.get_state()

    err = 0

    #do PID stuff if necessary
    if state == 'Burnout':
        if not piddle.initialized:
            piddle.init_readings(y,v)
        
        piddle.PID_step(y,v)
        err = piddle.err1[-1]
        phi = piddle.get_phi()
    elif state == 'Overshoot':
        phi = piddle.get_max()
    else:
        phi = 0

    #actuate servo to phi radians
    servo.rotate(phi)

    #print(y,v,a)
    print(t,raw_data[2],raw_data[3][0],y,v,a,state,phi,err)
    scribe(t,raw_data[1],raw_data[2],raw_data[3],theta,y,v,a,state,phi)
