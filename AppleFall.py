import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

#fig= plt.subplot(figsize=(8,8))
#fig, ax = plt.subplot(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
fig, ax = plt.subplots()
ax.set(xlim=(-2, 2), ylim=(0, 600), xlabel='Position, meters', ylabel='Height, meters', title='Apple falling from CN tower')


t = 10 #s
m = 5.3 #kg
g = 9.8 #m/s^2
v0x = -0.15 #m/s
h = 553 #m

dt = 0.1 #50 ms
N = int(t/dt)  # amount of iterations

#create two dimensional arrays
v = np.zeros((N+1,2))
r = np.zeros((N+1,2))
f = np.zeros((N+1,2))
v1 = np.zeros((N+1,2))
r1 = np.zeros((N+1,2))
f1 = np.zeros((N+1,2))

#Initial conditions
r[0] = np.array([0,h])
v[0] = np.array([-v0x,0])
r1[0] = np.array([0,h-20])
v1[0] = np.array([v0x+0.1,0])

#the only gorce is gravity
f[:] = np.array([0,-m*g])
f1[:] = np.array([0,-m*g])

for n in range(N):
    v[n+1] = v[n]+(f[n]*dt)/m
    r[n+1] = r[n]+v[n+1]*dt
    v1[n+1] = v1[n]+(f1[n]*dt)/m
    r1[n+1] = r1[n]+v1[n+1]*dt

scat = ax.scatter(r[0,0], r[0,1], marker='o', c='g', s=200)
scat1 = ax.scatter(r1[0,0], r1[0,1], marker='o', c='y', s=200)

def animate(i):
    scat.set_offsets(r[i])
    scat1.set_offsets(r1[i])

ani = animation.FuncAnimation(fig, func=animate, frames=N)
#ani.save('CNtower.html', writer=animation.HTMLWriter(fps= 1//dt))
plt.close()
writergif = animation.PillowWriter(fps=N)
ani.save('filename.gif',writer=writergif)
