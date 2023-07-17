import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np
import matplotlib.ticker as ticker
import math

timestep = 0.5 #500 ms
t = 0
sum = 0
epsilon = 0.05
N = 5
d = 0
u = 1
n = np.zeros(N+1)
n1 = np.zeros(N+1)
capacitance = np.zeros(1)
timecap = np.zeros(1)
ti = np.zeros(N+1)
ti1 = np.zeros(N+1)
discontinuity = np.zeros(N+1)
time = np.zeros(N+1)

def timeelapsed(data):
    """Here we convert the time of the timerlist to seconds elapsed
       The time format is HOUR:MINUTE:SECOND.MS            """
    temp= [i*0 for i in range(0,len(data))]
    temp2 = [i*0 for i in range(0,len(data))]
    for n in range(0,len(data)):
        templist=  data[n].split(':')
        temp[n] += int(templist[0])*3600*1000 #The hours converted to seconds
        temp[n] += int(templist[1])*60*1000 #minutes
        temp[n] += int(templist[2].split(".")[0])*1000
        temp[n] += int(templist[2].split(".")[1])
        #print(templist[2].split(".")[1])
    for k in range(1,len(temp)):
        #print(temp[k])
        #print(temp[k-1])
        temp2[k] = temp[k]-temp[k-1] + temp2[k-1]

    for j in range(0,len(temp2)):
        #Convert to seconds from miliseconds
        temp2[j] = temp2[j]/1000
    return temp2

def readtxt(data):
    """Input should be a string"""
    #print(len(data))

    with open(data,'r') as file:
        data = file.read()
        processeddata = data.split()
        #print(processeddata)
    processeddata1 = [i*0 for i in range(0,int(len(processeddata)/3))]
    timer = [i*0 for i in range(0,int(len(processeddata)/3))]
    for i in range(0,len(processeddata1)):
        #print(processeddata1[3*i+2])
        processeddata1[i] = float(processeddata[i*3+2])
        timer[i] = str(processeddata[i*3])
    for time in timer:
        time.split()

    return processeddata1,timer

def differenceapproximation(Vi,Ti):
    """Here we approximate the discrete derivative
       using a first order approximation. Vi,Ti are lists"""
    difflist = np.array(N+1)
    #print(difflist)
    for i in range(0,N-1):
        difflist = np.append(difflist,(Vi[i]-Vi[i+1])/(Ti[i+1]-Ti[i]))
    print(difflist)
    return difflist

def capacitancee(Vi,Ti):
    """Here we calculate the observed capacitance """
    global ti1, n1, timecap, capacitance
    sum = 0
    sum1 = 0
    Vin = 5 #This is the reference value from the microcontroller
    nn = 5
    R1 = 680000 #This is the resistance value of the circuit.
    nnVR1 = 2*nn*Vin*R1
    topvalue = 0
    belowvalue = 0

    for i in range(1,N):
        if n1[i] == 0:
            n1[i] = Vi
            ti1[i] = Ti
            break
            return
    if n1[N-1] !=0:
        timediff = ti1[N-1]-ti1[0]
        #dvdt = differenceapproximation(n1,ti1)
        sum += (n1[0]+n1[N-1])*timediff
        #sum1 += (dvdt[0]+dvdt[N-1])*timediff
        for j in range(1,N-1):
            sum += 2*n1[j]*timediff
            #sum1 += 2*dvdt[j]*timediff
        sum = sum/nnVR1
        topvalue = sum
        belowvalue = 1#-sum1/(nn*Vin)
        cap = topvalue/belowvalue

        capacitance=np.append(capacitance,cap)
        timecap=np.append(timecap,timediff+ti[0])
        for i in range(1,N):
            n1[i] = 0
            ti[i] = 0
            dvdt = 0
        #print(capacitance)
    #    return capacitance,timecap




def differential(Ri,Ti):
    """Here we calculate the observed points of
       discontinuity"""
    global t,sum,n,u,ti

    for i in range(1,N):
        if n[i] == 0:
            #print(R)
            n[i] = Ri
            ti[i] = Ti
            break
            return
    #print(n[N-1])
    #print(n[N-1])
    #print('a')
    if n[N-1] != 0:
        for j in range(1,N-1):
            if discontinuity[N-1] != 0:
                break
            print(n)
            #t += 3*0.5

            for p in range(1,N):
                sum+=n[p]
            avr = sum/(N-1)
            d = abs(avr-n[N-1])/avr

            print(d>epsilon and n[N-1] != 0)
            print(t)
            print(str(d) + ' d')
            print(str(sum) + ' sum')
            print(str(avr) + ' avr')
            print(str(n[N-1]) + ' xj')
            if d>epsilon and n[N-1]!=0:
                while u < N-1:
                    if discontinuity[u] == 0:
                        discontinuity[u] = 1

                        time[u] = ti[u]
                        break
                    u=u+1
                for k in range(1,N-1):
                    n[k]=0
                    ti[k]=0
                sum = 0
                for i in range(1,N-1):
                    sum+= n[i]
                n = n[::-1]
                ti = ti[::-1]
                break
            for k in range(1,N-1):
                n[k] = 0

            sum = 0
            for i in range(1,N-1):
                sum+= n[i]
            n = n[::-1]
            ti = ti[::-1]
            break


            """
            if d>epsilon:
                discontinuity[j] = 1
                time[j] = t
                for k in range(j):
                    n[k] = 0
                sum = 0
                #print(t)
            else:
                for k in range(j):
                    n[k] = 0
                    sum = 0


            print(n)
            sum = 0"""

    #print(n)


    """for i in range(1,N):

        if n[i] == 0:
            #n = n[::-1]
            #print(n)
            n[i] = R
            #print(n[i])
            #print('a')
            break
        elif n[N-1] != 0:
            for k in range(1,N):
                print(n)
                t=t+1
                sum += n[k]
                avr = sum/k
                print(str(avr) + ' avr')
                print(n[k])
                #print(n[k])
                print(abs(n[k]-avr)/(avr+1))
                if avr != 0 and abs(n[k]-avr)/(avr+1) > epsilon:
                    discontinuity[k] = 1
                    time[k] = t*timestep
                    sum = 0
                    for j in range(0,N):
                        n[j] = 0

                    break
                else:
                    for j in range(0,N-4):
                        n[j] = 0
                    sum = 0
        break

                    for j in range(0,N-2):
                        n[j] = 0
                    n = n[::-1]
                    #print(n)
                    sum = 0
                    for l in range(0,N):
                        sum+= n[l]

                    break
                elif n[N-1] != 0:
                    for p in range(0,N-2):
                        n[p] = 0
                    n = n[::-1]
                    #sum = 0
                    for u in range(0,N):
                        sum+= n[u]
                    break"""
    #print(discontinuity)


def main():


    global capacitance,timecap
    ##Data readout
    """data1 = readtxt('data1.txt')
    data2 = readtxt('data2.txt')
    data3 = readtxt('data3.txt')
    data4 = readtxt('data4.txt')
    data5 = readtxt('data5.txt')
    data6  = readtxt('data6.txt')
    data7 = readtxt('data7.txt')
    data8 = readtxt('data8.txt')
    data9,timer9 = readtxt('data9.txt')"""
    data14,timer14 = readtxt('data14.txt')
    data11,timer11 = readtxt('data11.txt')
    timer14 = timeelapsed(timer14)
    timer11 = timeelapsed(timer11)
    data12,timer12 = readtxt('data12.txt')
    data13,timer13 = readtxt('data13.txt')
    timer13 = timeelapsed(timer13)
    timer12 = timeelapsed(timer12)

    #print(timer10)
    #print(timer11)
    for i in range(len(data11)):
        differential(data11[i],timer11[i])

    #plt.plot(timer12,data12)
    #cap1 = capacitance
    #time1 = timecap
    #capacitance = np.zeros(1)
    #timecap = np.zeros(1)
    #for i in range(len(data11)):
    #    capacitancee(data11[i],timer11[i])
    #cap2 = capacitance
    #time2 = timecap

    #print(capacitance)
    #print(timecap)
    #for R,Ti in data10:
    #    differential(R)

        #print(R)
    #plt.plot(time,discontinuity)
    #print(discontinuity)
    #print(time)
    ###Graphical analysis
    """x1 = [i*timestep for i in range(len(data1))]
    x2 = [i*timestep for i in range(len(data2))]
    x3 = [i*timestep for i in range(len(data3))]
    x4 = [i*timestep for i in range(len(data4))]
    x5 = [i*timestep for i in range(len(data5))]
    x6 = [i*timestep for i in range(len(data6))]
    x7 = [i*timestep for i in range(len(data7))]
    x8 = [i*timestep for i in range(len(data8))]
    """


    x = np.array(timer13)
    y = np.array(data13)
    x1 = np.array(timer14)
    y1 = np.array(data14)
    print(timecap)
    print(capacitance)
        # setup figures
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    # plot two identical plots
    ax1.plot(x, y)
    ax1.plot(x1,y1)


    disc = np.zeros(152)
    disc1 = np.zeros(152)
    time = np.array([i for i in range(0,152)])
    disc[55] = 1
    disc[103]=1
    disc1[61] = 1
    disc1[101] = 1

    ax2 = fig.add_subplot(212,sharex=ax1)
    ax2.plot(time, disc1)
    ax2.plot(time, disc)


    # Change only ax1
    scale_x = 1
    scale_y = 1e6
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax1.xaxis.set_major_formatter(ticks_x)

    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    ax1.yaxis.set_major_formatter(ticks_y)

    ax1.legend(["h","h1"])
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel('Resistance [MΩ]')
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel('Discontinuity')

    plt.show()

    #spl = UnivariateSpline(x, y)
    #spl.set_smoothing_factor(100)
    #xs = np.linspace(0, 140, 100000)
    #yinterp = np.interp(xs, x, y)
    #plt.plot(xs, yinterp, 'g', lw=2)
    #plt.plot(x,y)

    #plt.plot(x1, data1,x2 ,data2,x3,data3,x4,data4,x5,data5)
    #plt.xlabel('Time [s]')
    #plt.legend(['Data 1, black unit', 'Data 2, black unit', 'Data3, white unit', 'Data4, white unit', 'Data5, black unit'])
    #plt.ylabel('Resistance [ohm]')
    #plt.ylabel('Discontinuity')
    #plt.show()

    ########################################

if __name__ == '__main__':
    main()
