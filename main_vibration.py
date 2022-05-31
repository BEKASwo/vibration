import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft

from modules.unitSignal import *
from modules.signal import Signal

from settings import *


from modules.test import *


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

mods = []
for i in range(len(x)):
    mod = np.sqrt(x[i] * x[i] + y[i] * y[i] + z[i] * z[i])
    mods.append(mod)
mods = np.array(mods)


#plt.plot(time, x)
#plt.plot(time, y + 7)
#plt.plot(time, z + 14)
#plt.plot(time, mods - 7)

Sx = x.std()
Sy = y.std()
Sz = z.std()


sig_x = []
for i in np.abs(x):
    if i > 2*Sx:
        sig_x.append(1)
    else:
        sig_x.append(0)

signals = GetSignals(x, next=40, prev=40)
for i in range(len(signals)):
    plt.plot(signals[i] + 5 * np.floor(i/100))
print(len(signals))
#plt.plot(time, sig_z)



#signals = FormSignals(MPU_FILE_NAME, KEY_FILE_NAME, PREV_SIGNAL, NEXT_SIGNAL, 2)
#for signal in signals:
#    plt.plot(signal)


#signals = UnitSignal.FormUnitSignlasFromKeyboardAndMPU(KEY_FILE_NAME, MPU_FILE_NAME, NEXT_SIGNAL, PREV_SIGNAL)
#for signal in signals:
#    plt.plot(signal.X)
#    plt.plot(signal.Y + 5)
#    plt.plot(signal.Z + 10)


plt.show()



