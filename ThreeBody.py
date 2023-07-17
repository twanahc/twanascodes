import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

fig, ax = plt.subplots()
ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5), ylabel='meters', xlabel='meters', title='3-Body problem')

#Parameters
t = 10
K = 5
r0 = 1
l = 3 #total lattices
m = 0.3

dt = 0.05
N = int(t/dt)

v = np.zeros((N+1, 3, 2))
r = np.zeros((N+1, 3, 2))
f = np.zeros((N+1, 3, 2))

r[0,0] = np.array([0,2])
r[0,1] = np.array([2,0])
r[0,2] = np.array([-1,0])

def compute_forces(n):
    for i in range(l):
        for j in range(l):
            if i != j:
                rij = r[n,i]-r[n,j]
                rij_abs = np.linalg.norm(rij)
                f[n,i] -= K*(rij_abs-r0)*rij / rij_abs

for n in range(N):
    compute_forces(n)
    v[n+1] = v[n] + f[n]/m * dt
    r[n+1] = r[n] + v[n+1] * dt

scat = ax.scatter(r[0,:,0], r[0,:,1], marker='o', c=['b', 'k', 'r'], s=1000)

def animate(i):
    scat.set_offsets(r[i])

ani = animation.FuncAnimation(fig, animate, frames=N)
plt.close()
writergif = animation.PillowWriter(fps=N)
ani.save('threebody.gif',writer=writergif)
