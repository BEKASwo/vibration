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


a = ReadDataWithMPU(MPU_FILE_NAME)

#time = a['time']
#time = time - time.min()

#x = a['x']
#y = a['y']
#z = a['z']


#plt.plot(time, x)
plt.plot(a['time'], a['y'] + 0.5)
#plt.plot(time, z + 1)

#a = UnitSignal.FormUnitSignlasFromKeyboardAndMPU(KEY_FILE_NAME, MPU_FILE_NAME,
#                                                    NEXT_SIGNAL, PREV_SIGNAL)

#for signal in a:
#    plt.plot(signal.Y)

plt.show()




pass
pass
