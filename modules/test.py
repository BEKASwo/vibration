import numpy as np
import csv

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



def FormSignals(file_name_mpu, file_name_key, prev=10, next=118, sigma=2):
    mpu_data = ReadDataWithMPU(file_name_mpu)
#    key_data = ReadDataWithKey(file_name_key)

    x = mpu_data['x'] - mpu_data['x'].mean()
    y = mpu_data['y'] - mpu_data['y'].mean()
    z = mpu_data['z'] - mpu_data['z'].mean()
    t = mpu_data['time']

    mods = []
    for i in range(len(x)):
        mod = np.sqrt(x[i] * x[i] + y[i] * y[i] + z[i] * z[i])
        mods.append(mod)
    mods = np.array(mods)



    print(mods.mean())
    tmp_mods = mods - mods.mean()
    S = tmp_mods.std()

    tmp_mods = np.abs(tmp_mods)
    
    signals = []

    i = prev
    while i < tmp_mods.size - next:
        if tmp_mods[i] > sigma * S:
            ss = []
            for j in range(i - prev, i + next):
                ss.append(mods[j])

            signals.append(np.array(ss))
            
            i += next

        i += 1

    return signals