import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import random as rnd
import math

fig, ax = plt.subplots()
#ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5), ylabel='meters', xlabel='meters', title='3-Body problem')

#Parameters
t = 10
K = 5
r0 = 1
M = 10 #total lattices
u = 1.66053904*10**-27
m = 39.948*u
kb = 1.38064852 * 10**-23
T = 273 #kelvin
kbT = 273 * kb

numbersPerRow = 6
Lx = numbersPerRow *1.12
Ly = numbersPerRow *1.12



epsilon = 120*kb # argon
sigma = 0.34*10**-9 #argon

dt = 0.05
N = int(t/dt)

v = np.zeros((N+1, M, 2))
r = np.zeros((N+1, M, 2))
f = np.zeros((N+1, M, 2))



#Initial positions
for i in range(M-1):
    for k in range(M-1):
        r[0,i] = np.array([0,k/2+1])


def gaussianRandomNumbers(sigma):
    #Used to assign random velocities
    w = 2
    while (w >= 1):
        rx1 = 2 * rnd.random() - 1
        rx2 = 2 * rnd.random() - 1
        w = rx1 * rx1 + rx2 * rx2

    w = math.sqrt(-2 * math.log(w) / w);
    return sigma * rx1 * w, sigma * rx2 * w

def thermalize(v, kineticEnergyPerParticle):
    for i in range(M):
        v[i] = gaussianRandomNumbers(kineticEnergyPerParticle)

thermalize(v, kbT)


def compute_forces(n):
    for i in range(M):
        for j in range(M):
            if i != j:
                rij = r[n,i]-r[n,j]
                print(rij)
                rij_abs = np.linalg.norm(rij)
                #print(rij_abs)
                f[n,i] = -4*epsilon*(6*(sigma/rij_abs)**7-12*(sigma/rij_abs)**13)
                #f[n,i] = 24*epsilon*((sigma/rij_abs)**6-2*(sigma/rij_abs)**12)

for n in range(N):
    compute_forces(n)
    v[n+1] = v[n] +f[n]/m * dt
    r[n+1] = r[n]+v[n+1]*dt

scat = ax.scatter(r[0,:,0], r[0,:,1], marker='o', s=1000)

def animate(i):
    scat.set_offsets(r[i])

ani = animation.FuncAnimation(fig, animate, frames=N)
plt.close()
writergif = animation.PillowWriter(fps=N)
ani.save('LJgas.gif',writer=writergif)
