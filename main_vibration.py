import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft

from modules.unitSignal import *
from modules.signal import Signal

from settings import *



def ReadDataWithMPU(file_name: str) -> None:
        with open(file_name) as File:
            reader = csv.reader(File, delimiter=',', quotechar=',',
                                quoting=csv.QUOTE_MINIMAL)
            x = []
            y = []
            z = []
            t = []
            for row in reader:
                x.append(float(row[0]))
                y.append(float(row[1]))
                z.append(float(row[2]))
                t.append(float(row[3]))

        return {'x' : np.array(x), 'y' : np.array(y), 'z' : np.array(z), 'time' : np.array(t)}

def GetSignals(signal, sigma=2, prev=10, next=118):
    tmp_signal = signal - signal.mean()
    S = tmp_signal.std()

    tmp_signal = np.abs(tmp_signal)
    
    signals = []

    i = prev
    while i < tmp_signal.size - next:
        if tmp_signal[i] > sigma * S:
            ss = []
            for j in range(i - prev, i + next):
                ss.append(signal[j])

            signals.append(np.array(ss))
            
            i += next

        i += 1

    return signals

    


a = ReadDataWithMPU(MPU_FILE_NAME)

time = a['time']        
time = time - time.min()

print(1 / (time.max() / time.size))

x = a['x'] - a['x'].mean()
y = a['y'] - a['y'].mean()
z = a['z'] - a['z'].mean()


plt.plot(time, x)
plt.plot(time, y + 7)
plt.plot(time, z + 14)

Sx = x.std()
Sy = y.std()
Sz = z.std()


sig_z = []
for i in np.abs(z):
    if i > 2*Sz:
        sig_z.append(1)
    else:
        sig_z.append(0)

#signals = GetSignals(z, next=50)
#for i in signals:
#    plt.plot(i)

#plt.plot(time, sig_z)



plt.show()



