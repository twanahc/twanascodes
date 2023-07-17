import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from mpl_toolkits import mplot3d

#Parameters
C = 10 #The capacitance of the CDI
q0 = 0.75 #start charge across capacitor
vc = q0/C #The voltage threshhold, which is when you discharge.
dt = 0.00005 #timestep
L = 0.2
dH = 0.01 #Change in inductance
dR = 0.1 #Change in resistance
R = 0.8
maxefficiency = 0.5*vc #the coefficient tells us what efficiency we expect
t = 40# 10 seconds
henryList = [i*dH for i in range(1,100)]
resistanceList = [i*dR for i in range(1,100)]
#q0 = 0.75 #start charge across capacitor
N = int(t/dt) #number of iterations



def current(t,R,L):
    """The current in the system, it is in series"""
    i = 0
    #if (1/L*C)-(R/(2*L))**2 >= 0:
    #if R < 2*np.sqrt(L/C): #Undamped condition
    if (1/L*C)-(R/(2*L))**2 >= 0:
        wd = np.sqrt((1/L*C)-(R/(2*L))**2)
        i = (vc/(L*wd))*np.exp(-(R/2*L)*t)*np.sin(wd*t)
    return i

def energylost(R,i):
    return R*i**2

def energycalculation(R,L):
    """Here we calculate how many cycles to get to the desired efficiency
        for a given value of R,L"""
    maxEnergy = np.zeros((100,1,3))
    R = []
    H = []
    E = []
    i = []
    for i in range(len(maxEnergy)): #Setting up the initial voltage on the capacitor
        maxEnergy[i,0,2] = vc




def voltage(t,R,L):
    """The voltage across the inductor <-- we are probably not using this"""
    u = 0
    if (1/L*C)-(R/(2*L))**2 >= 0:
        w0 = math.sqrt((1/L*C)-(R/(2*L))**2)
        u = vc*(1-math.cos(w0*t)*math.exp(-R*t/(2*L)))
    return u

def energystoredinductor(i,L):
    """This calculates the energy stored in an inductor"""
    return (L/2)*(i**2)

def plot(x,y):
    """Here we plot the values of interest in a 3d plot"""
    plt.plot(x,y)
    plt.title('Energy stored in inductor over time')
    plt.xlabel('Time [ms]')
    plt.ylabel('Energy [J]')
    plt.show()

def main():
    x = []
    y = []
    z = []
    energyLost = []
    i= []
    maxEnergy = np.zeros((100,1,3))



    for inductor in range(1,100):
        for resistance in resistanceList:
            i = []
            energyinductor = []
        #if (1/inductor*C)-(resistance/(2*0.01*inductor))**2 >= 0:
            for time in range(N):
                 #underdamped
                    i.append(current(time*dt,resistance,inductor))
                    energyLost.append(energylost(resistance,i[time]))
                    #print(float(i[time]))
                    energyinductor.append(energystoredinductor(i[time],inductor*0.01))
                #print(maxEnergy[inductor])
            maxEnergy[inductor] = np.array((inductor*0.01,resistance,max(energyinductor, default = 0)))

            if maxEnergy[inductor][0][2] != 0.0:
                x.append(maxEnergy[inductor][0][0])
                y.append(maxEnergy[inductor][0][1])
                z.append(maxEnergy[inductor][0][2]/(10**-6))
                #print(y)"""

    """t = [i*dt for i in range(N)]
    for k in range(N):
        i.append(current(k*dt,R,L))
        #print(i[k])
    plt.plot(t,i)
    plt.ylabel('I [A]')
    plt.xlabel('Time [s]')
    plt.title('Current over time for L = 0.0967, R = 0.0947')
    plt.show()
            #print(maxEnergy[inductor])
    #x,y,z = maxEnergy.nonzero()
    #np.savetxt('myfile.csv', maxEnergy, delimiter=',')"""

    """for i in range(len(maxEnergy)):
        if maxEnergy[i][0][2] != 0.0:
            x+= maxEnergy[i][0][0]
            print(x)
    for i in range(len(maxEnergy)):
        if maxEnergy[i][0][2] != 0.0:
            y+= maxEnergy[i][0][1]
    for i in range(len(maxEnergy)):
        if maxEnergy[i][0][2] != 0.0:
            z+= maxEnergy[i][0][2]

"""
    ax = plt.axes(projection='3d')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(x,y,z)
    plt.title('Energy (micro Joules) over R and L')
    plt.xlabel('Inductance [H]')
    plt.ylabel('Resistance [Ohm]')
    ax.set_zlabel('Energy [uJ]')
    #plt.zlabel('Energy [J]')
    plt.show()#"""


if __name__ == '__main__':
    main()
