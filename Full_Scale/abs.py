# The main file
from Data_Logger import *
from Kalman import *
from State_Manager import *
from PID import *
from Servo import *
from Scribe import *

use_bno = 0

#TODO: consider adding parallelization
dlogger = DataLogger(use_bno)
dfilter = DataFilter(use_bno)
piddle  = PID()
state_machine = StateManager()
servo = Servo()
scribe = Scribe(use_bno)

print('Successfully Initialized')

while True:
    try:
        #Read in data from the data logger
        dlogger.read_data()
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

<<<<<<< HEAD
        print(y,v,a)
        scribe(t,raw_data[1],raw_data[2],raw_data[3],theta,y,v,a,state,phi)
    except:
        pass
=======
        #print(y,v,a)
        scribe(t,raw_data[1],raw_data[2],raw_data[3],theta,y,v,a,state,phi)
    except:
        print('Row failed. Oops')
>>>>>>> 60f260a80d180c90143d4f9e77efdfc12e9320ef
