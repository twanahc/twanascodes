#this sets up a graph
import matplotlib.pyplot as plt

#starting values
C=5e-3
L=300e-3
V0=3
Q=V0*C
t=0
dt=0.001
dQ=0

#added a value for the resitance
#you can try changing this value to see what happens
R=3

#run the calculations for 2 seconds
while t<2:
  #calculate the second derivative of charge
  #this is based on the loop rule
  ddQ=-Q/(L*C)-dQ*R/L

  #update the current (dQ) using ddQ
  dQ=dQ+ddQ*dt

  #update Q
  Q=Q+dQ*dt

  #update time
  t=t+dt

  #plot stuff
  #now I'm plotting voltage across the capacitor
  plt.plot(t,Q/C)
  plt.show()
