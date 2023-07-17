#Rewrite the code for the electrochemistry project
import pandas as pd
import matplotlib.pyplot as plt
#pd.set_option('display.max_columns', 100)

#Global variables
massPB = 0.75 #750mg
massACC = 0.35 #350mg
referencepotential = .197 #197 mV, Normal hydrogen, source: Gamry
samplingrate = 0.5 #500 ms

def readcsv(data):
    """Here we read the csv file"""
    df = pd.read_csv(data, sep=',')
    return df

def potentialdifference(df1,df2):
    """Here is calculated the potential difference from the reference
       electrode"""
    PBpotential = []
    for i in range(0,len(df1['Value '])):
        PBpotential.append(df1['Value '][i] + df2[i])
    return PBpotential

def opotentialdifference(df1,df2):
    """Here is calculated the potential difference from the reference
       electrode but with opposite polarity"""
    PBpotential = []
    for i in range(0,len(df2['Value '])):
        PBpotential.append(df2['Value '][i] + df1[i])
    return PBpotential

def plot(y1,y2):
    """We plot the actual data here"""
    q1 = [0]
    q2 = [0]
    x  = [i*samplingrate for i in range(0,len(y1))]
    for i in range(1,len(y2)):
        q1.append(samplingrate*2.13+q1[i-1])
    for i in range(1,len(y2)):
        q2.append(samplingrate*0.245+q2[i-1])
    plt.title('Potential across each electrode')
    plt.ylabel('Potential [V]')
    plt.xlabel('Time [s]')
    plt.plot(x,y1,x,y2)
    plt.legend(['Prussian Blue, K = 2.13 mA/cm^2','Activated carbon cloth, K = 2.13 mA/cm^2', 'Activated carbon cloth, K = 0.245 mA/cm^2','Prussian Blue, K = 0.245 mA/cm^2'])
    plt.show()

def charge(current1,y1):
    t = [i*samplingrate for i in range(0,len(y1))]
    x1 = []
    for i in range(0,len(t)):
        x1.append(samplingrate*float(current1[i]))
    return x1

def main():
    df1 = readcsv('data4_CobaltFibreACC.csv')
    df2 = readcsv('data4_CobaltFibreACCReference.csv')
    df3 = readcsv('data10_CobaltFibreACC1.5_4.7mA.csv')
    df4 = readcsv('data10_CobaltFibreACCReference1.5_4.7mA.csv')
    y2 = []
    y4 = []
    current1 = []
    current2 = []
    for k in range(0,len(df2['Value '])):
        y2.append(df2['Value '][k])
        current1.append(df2['Value_2ND '][k])
    for k in range(0,len(df2['Value '])):
        y4.append(df4['Value '][k])
        #current2.append(df4['Value_2ND '][k])


    #print(len(y4))
    #print(len(y2))
    y1 = potentialdifference(df1,y2)
    #y3 = opotentialdifference(y4,df3[:len(y4)],)
    y3 = opotentialdifference(y4,df3[:len(y4)])
    #q1= charge(current1,y1)
    #q2= charge(current2,y1)
    #plt.plot(y1,y2)
    #plt.show()
    plot(y1,y2)

if __name__ == '__main__':
    main()
