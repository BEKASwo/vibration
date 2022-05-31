import numpy as np
import csv
import json

from modules.signal import Signal

class UnitSignal:
    def __init__(self, key=None, X=None, Y=None, Z=None, time=None):
        self.__key = key
        self.__signal_X = np.array(X)
        self.__signal_Y = np.array(Y)
        self.__signal_Z = np.array(Z)
        self.__time = np.array(time)

    @property
    def X(self):
        return self.__signal_X.copy()

    @property
    def Y(self):
        return self.__signal_Y.copy()

    @property
    def Z(self):
        return self.__signal_Z.copy()

    @property
    def Key(self):
        return self.__key

    @property
    def Time(self):
        return self.__time.copy()


    # Поворот относительно одной из осей
    # fi - угол вращения в радианах
    # axis - ось вращения (x, y, z)
    def Rotate(self, fi: float, axis: str):
        axis = axis.lower()

        if axis == 'x':
            matrix = np.array([
                [1, 0, 0],
                [0, np.cos(fi), -np.sin(fi)],
                [0, np.sin(fi), np.cos(fi)]
            ])

        elif axis == 'y':
            matrix = np.array([
                [np.cos(fi), 0, -np.sin(fi)],
                [0, 1, 0],
                [np.sin(fi), 0, np.cos(fi)]
            ])

        elif axis == 'z':
            matrix = np.array([
                [np.cos(fi), -np.sin(fi), 0],
                [np.sin(fi), np.cos(fi), 0],
                [0, 0, 1]
            ])

        else:
            return

        signals = np.array([self.__signal_X, self.__signal_Y, self.__signal_Z])

        result = matrix.dot(signals)
        self.__signal_X = result[0]
        self.__signal_Y = result[1]
        self.__signal_Z = result[2]


    def FilterSignal(self, axis: str ='xyz', alpha: float = 1, beta: float = 0.15):
        axis = axis.lower()

        if 'x' in axis:
            signal = Signal(signal=self.X)
            self.__signal_X = signal.MakeFilterSignal(alpha, beta).Signal

        if 'y' in axis:
            signal = Signal(signal=self.Y)
            self.__signal_Y = signal.MakeFilterSignal(alpha, beta).Signal

        if 'z' in axis:
            signal = Signal(signal=self.Z)
            self.__signal_Z = signal.MakeFilterSignal(alpha, beta).Signal


        
    def MakeFFTSignal(self, normalize: bool = False):
        new_x = Signal(signal=self.X).MakeFFTSignal(normalize).Signal
        new_y = Signal(signal=self.Y).MakeFFTSignal(normalize).Signal
        new_z = Signal(signal=self.Z).MakeFFTSignal(normalize).Signal

        return UnitSignal(self.Key, new_x, new_y, new_z)

    
    def NoiseSignal(self, axis: str = 'xyz', noise: float = 0.08):
        axis = axis.lower()

        if 'x' in axis:
            signal = Signal(signal=self.X)
            self.__signal_X = signal.MakeNoiseSignal(noise).Signal

        if 'y' in axis:
            signal = Signal(signal=self.Y)
            self.__signal_Y = signal.MakeNoiseSignal(noise).Signal

        if 'z' in axis:
            signal = Signal(signal=self.Z)
            self.__signal_Z = signal.MakeNoiseSignal(noise).Signal


    def Normalize(self, min: float = 0, max: float = 1):
        signal = Signal(signal=self.X)
        signal.Normalize(min, max)
        self.__signal_X = signal.Signal

        signal = Signal(signal=self.Y)
        signal.Normalize(min, max)
        self.__signal_Y = signal.Signal

        signal = Signal(signal=self.Z)
        signal.Normalize(min, max)
        self.__signal_Z = signal.Signal


    @staticmethod
    def WriteUnitSignals(file_name: str, unit_signals):
        data = []
        for unit_signal in unit_signals:
            key = unit_signal.Key
            X = list(unit_signal.X)
            Y = list(unit_signal.Y)
            Z = list(unit_signal.Z)

            if None not in unit_signal.Time:
                time = list(unit_signal.Time)
            else:
                time = None

            data.append({'key': key, 'X': X, 'Y': Y, 'Z': Z, 'time': time})

        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


    @staticmethod
    def ReadUnitSignals(file_name: str):
        data = None

        with open(file_name) as file:
            data = json.load(file)

        unit_signals = []

        for unit_signal in data:
            key = unit_signal['key']
            X = unit_signal['X']
            Y = unit_signal['Y']
            Z = unit_signal['Z']
            time = unit_signal['time']

            unit_signals.append(UnitSignal(key, X, Y, Z, time))

        return unit_signals


    def __ReadDataWithKey(file_name: str) -> None:
        key_data = []

        with open(file_name) as File:
            reader = csv.reader(File, delimiter=',', quotechar=',',
                                quoting=csv.QUOTE_MINIMAL)
            
            for row in reader:
                data = {'key': row[0], 'time': float(row[1])}
                key_data.append(data)

        return key_data


    def __ReadDataWithMPU(file_name: str) -> None:
        mpu_data = []

        with open(file_name) as File:
            reader = csv.reader(File, delimiter=',', quotechar=',',
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                x = float(row[0])
                y = float(row[1])
                z = float(row[2])
                t = float(row[3])

                data = {'x' : x, 'y' : y, 'z' : z, 'time' : t}
                mpu_data.append(data)

        return mpu_data


    @staticmethod
    def FormUnitSignlasFromKeyboardAndMPU(keyboard_file_name: str,
                                      mpu_file_name: str,
                                      next_signal: int,
                                      prev_signal: int):

        key_data = UnitSignal.__ReadDataWithKey(keyboard_file_name)
        mpu_data = UnitSignal.__ReadDataWithMPU(mpu_file_name)

        unit_signals = []

        if key_data == [] or mpu_data == []:
            return 

        i = 0
        # Проход по каждой клавише
        for key in key_data:
            # Проход по каждому значению сигнала
            while i + next_signal < len(mpu_data):
                # Если время сигнала и клавиши не совпадает, то пропускаем
                if (key['time'] > mpu_data[i]['time']):
                    i += 1
                    continue

                # Иначе кидаем диапазон в список
                x = []
                y = []
                z = []
                time = []
                for j in range(i - prev_signal, i + next_signal + 1):
                    x.append(mpu_data[j]['x'])
                    y.append(mpu_data[j]['y'])
                    z.append(mpu_data[j]['z'])
                    time.append(mpu_data[j]['time'])

                i += next_signal
                unit_signals.append(UnitSignal(key['key'], x, y, z, time))
                break

        return unit_signals


    @staticmethod
    def GetTrainAndTestUnitSignals(signals: list, share: float):
        if share <= 0 or share >= 1:
            return

        train_signals = signals.copy()
        test_signals = []

        all_len = len(train_signals)
        
        while (len(train_signals) / all_len) > share:
            index = np.random.randint(len(train_signals))
            test_signals.append(train_signals.pop(index))

        return train_signals, test_signals




    




