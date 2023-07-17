import pandas as pd
import matplotlib.pyplot as plt

def readcsv(data):
    """Here we read the csv file"""
    dataframe = pd.read_csv(data, sep=',')
    return dataframe

def trapezoidmethod(time,energy):
    """Here we approximate the integral of discrete points
        using the trapezoid method, O(h^2)"""
    integral = []
    n = len(energy)
    dt = 1/n
    length = len(time)

    integral.append((dt/2)*energy[0])
    for i in range(1,len(time)-1):
        integral.append(dt*energy[i])
    integral.append((dt/2)*energy[length-1])

    return sum(integral)


def plot(time,y1,y2):
    """We plot the actual data here"""
    t  = [i*1/len(y1) for i in range(0,len(y1))]
    plt.title('Voltage and current profile over and through CDI over time')
    """fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(time, y1, 'g-')
    ax2.plot(time, y2, 'b-')
    ax1.set_xlabel('X data')
    ax1.set_ylabel('Y1 data', color='g')
    ax2.set_ylabel('Y2 data', color='b')"""
    plt.xlabel('Time [s]')
    plt.plot(time,y1,time,y2)
    plt.legend(['Voltage [V]','Current [A]'])
    #plt.legend(['Prussian Blue','Activated carbon cloth'])
    plt.show()

def powercalculation(voltage,current):
    """Here we calculate the voltage multiplied with current for every
        datapoint to get the power"""
    energy = []
    for i in range(len(voltage)):
        energy.append(voltage[i]*current[i])
    return energy

def energyquotient(Ein,Eout):
    return abs(Eout/Ein)

def main():
    ###Raw data
    UIdata = readcsv("data13_CobaltFibreACC.csv") ##ACC/PBCoFibre electrodes
    time = UIdata['Time'].tolist()
    voltage = UIdata['Value '].tolist()
    current = UIdata['Value_2ND '].tolist()
    ##########
    UIdata2 = readcsv("data7_ACCACCconstcur2.csv") ##ACC/ACC electrodes
    time2 = UIdata2['Time'].tolist()
    voltage2 = UIdata2['Value '].tolist()
    current2 = UIdata2['Value_2ND '].tolist()


    #One cycle ACC/PBCoFibre
    index1 = 905 #retrieved from csv
    index2 = 2256
    index1discharge= 905 #discharging phase is upwards (positive volts)
    index2discharge= 1635
    index1charge= 1636
    index2charge= 5500
    dischargecycleindex = 730
    chargecycleindex = 627

    t = [i*0.5 for i in range(5500-905)]
    power1 = powercalculation(voltage[index1charge:index2charge],current[index1charge:index2charge])
    power = powercalculation(voltage[index1discharge:index2discharge],current[index1discharge:index2discharge])
    #plot(time[index1discharge:index2charge],voltage[index1discharge:index2charge],current[index1discharge:index2charge])
    plot(t,voltage[index1discharge:index2charge],current[index1discharge:index2charge])

    integral1 = trapezoidmethod(time[index1charge:index2charge],power)
    integral = trapezoidmethod(time[index1discharge:index2discharge],power)
    print(str(integral) + " discharge" )
    print(str(integral1)+ " charge")
    print(index2charge-index1charge)
    print(index2discharge-index1discharge)

    ##ACC/ACC
    #power2 = powercalculation(volt)
    index1acharge = 3400
    index2acharge = 18381 #1901 charge indexes
    index1adischarge = 18381
    index2adischarge = 19770 #1378
    t1 = [i*0.5 for i in range(index2adischarge-index1acharge)]
    #plot(time2,voltage2,current2)
    power1a = powercalculation(voltage2[index1acharge:index2acharge],current2[index1acharge:index2acharge])
    powera = powercalculation(voltage2[index1adischarge:index2adischarge],current2[index1adischarge:index2adischarge])
    print(len(current2[index1acharge:index2adischarge]))
    print(len(t1))
    #plot(t1,voltage2[index1acharge:index2adischarge],current2[index1acharge:index2adischarge])
    integral1a = trapezoidmethod(time2[index1acharge:index2acharge],power1a)
    integrala = trapezoidmethod(time[index1discharge:index2discharge],powera)
    print(str(integrala) + " dischargea" )
    print(str(integral1a)+ " chargea")



    #Energyrecovery1 ACCPBCo
    cyclelist = [1,2,3,4]
    dischargeEnergy = [-0.010841654774467514,-0.010440944995801008,-0.010735511507274836,-0.010822006156299033]
    chargeEnergy = [-0.008585447997117496,-0.00838441528174686,-0.008374624116221772,-0.008709781258816711]
    EnergyQuotient = []
    for i in range(len(cyclelist)):
        EnergyQuotient.append(energyquotient(dischargeEnergy[i],chargeEnergy[i]))
    """plt.scatter(cyclelist,EnergyQuotient)
    plt.ylim(-0.50,1.5)
    plt.title('Discharged energy/Charged energy')
    plt.xlabel('Cycle number')
    plt.ylabel('Edischarge/Echarge')
    plt.show()"""


    #Energyrecovery2 ACCACC
    dischargeEnergya =[0.004436298232318473,0.003079379499787617,0.003990081639848111,0.003478907867619099 ]
    chargeEnergya = [-0.005222753883614867,-0.003921102447141667,-0.004964301966856197,-0.004414313076355094]
    EnergyQuotienta = []

    for i in range(len(cyclelist)):
        EnergyQuotienta.append(energyquotient(chargeEnergya[i],dischargeEnergya[i]))
"""
    print(sum(EnergyQuotienta)/4)
    print(sum(EnergyQuotient)/4)
    plt.scatter(cyclelist,EnergyQuotienta,s=50)
    #plt.scatter(cyclelist,EnergyQuotient,s=20)
    plt.legend(['ACC/ACC electrodes', 'ACC/PBCo electrodes'])
    plt.ylim(0.50,1.0)
    plt.title('Discharged energy/Charged energy for ACC/ACC electrodes')
    plt.xlabel('Cycle number')
    plt.ylabel('Edischarge/Echarge')
    plt.show()"""

if __name__ == '__main__':
    main()
