import numpy as np

class PID():
    def __init__(self):
        # set gains
        self.kP = 20   # proportional gain
        self.kD = .1  # derivative gain
        self.kI = 0.001# integral gain

        # read file data
        self.fileName = 'Ideal_Flight_Profile.csv'
        self.data = self.load_data() #1482x2 numpy array

        self.ymax = 1354 # target altitude
        self.dt = 0.01   # simulation timestep

        self.maxPhi = 63.5#*np.pi/180      # max absolute value of phi in radians
        self.maxDeltaPhi = 60/.17#*np.pi/180/0.17*self.dt # rads
        
        # flags
        self.initialized = 0

    #Reads in ideal flight from CSV
    def load_data(self):
        with open(self.fileName) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.replace('\n', '').split(',')
            line = [float(i) for i in line]
            lines[i] = line

        lines = np.array(lines)

        return lines


    #Initialize the algorithm with sensor readinsgs from burnout
    def init_readings(self,y,vy):
        self.y =  [y]         # altitude at burnout (read in from sensors)
        self.vy = [vy]       # velocity at burnout (read in from sensors)

        err1 = vy - np.max(self.data[:,1]) #this should be current velocity minus max. velocity in ideal flight path
        self.err1 = [err1,err1]

        self.phi = [0]

        self.initialized = 1


    #Increments the PID one timestep
    def PID_step(self,y,vy):
        # add sensor data to log
        self.y.append(y)    #feet
        self.vy.append(vy)  #feet/s

        # update state
        self.err1.append(self.error1()) #new pos. vs flight path
        derivError = self.dError()    #derivative of error
        intError = self.iError()      #integral of error

        # determine shaft angle
        phi = self.kP*self.err1[-1] + self.kD*derivError + self.kI*intError
        print(phi)
        self.phi.append(self.check_phi(phi))


    #Finds proportion error
    def error1(self):
        yr = self.y[-1]
        yid = self.data[0,0]
        i = 0
        max_i = self.data.shape[0]

        while (yid <= yr) and (i < max_i):
            if i < max_i:
                yid = self.data[i,0]
                i += 1
            else:
                yid = self.ymax

        if i == max_i:
            return 10000

        m = (self.data[i,1] - self.data[i-1,1])/(self.data[i,0] - self.data[i-1,0])
        videal = m*(self.y[-1] - self.data[i-1,0]) + self.data[i-1,1]
        vrocket = self.vy[-1]
        err1 = vrocket - videal

        if yid < 300:
            err1 = 0

        return err1

    #Finds derivative of the error
    def dError(self):
        derivError = (self.err1[-1] - self.err1[-2])/(self.y[-1] - self.y[-2])

        return derivError


    #Finds integral of error
    def iError(self):
        intError = 0
        for i in range(1, len(self.y)):
            if self.err1[i] >= 0.1 or self.err1[i] <= -0.1:
                intError += ((self.y[i] - self.y[i-1])*(self.err1[i] + self.err1[i-1])/2)
            else:
                intError = 0

        return intError


    #Makes sure phi is within the correct bounds
    def check_phi(self,phi):
        old_phi = self.phi[-1]
        dPhi = phi-old_phi

        #limits excessive change
        if abs(dPhi) > self.maxDeltaPhi:
            if dPhi < 0:
                phi = old_phi - self.maxDeltaPhi
            else:
                phi = old_phi + self.maxDeltaPhi

        #ensures boundaries are respected
        if phi < 0:
            phi = 0
        elif phi > self.maxPhi:
            phi = self.maxPhi

        return phi

    
    #Outputs the current shaft rotation
    def get_phi(self):
        return self.phi[-1]#*180/np.pi

    def get_max(self):
        return self.maxPhi#*180/np.pi



#Test code
if __name__ == "__main__":
    piddle = PID()
    piddle.init_readings(100,500)
    piddle.PID_step(101,499)

    print(piddle.get_phi())
