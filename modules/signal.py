import numpy as np
from scipy.fft import rfft
from scipy import signal as sci_signal

class Signal:
    def __init__(self, key=None, signal=None): 
        self.__key = key
        self.__signal = np.array(signal)

    def SetKey(self, key):
        self.__key = key

    def SetSignal(self, signal: list) -> None:
        self.__signal = np.array(signal)

    @property
    def Key(self) -> str:
        return self.__key

    @property
    def Signal(self):
        return self.__signal.copy()

    # Нормализация сигнала в заданных рамках
    def Normalize(self, min=0, max=1):
        sig = self.__signal

        sig -= sig.min()
        sig = sig / sig.max()
        sig = sig * (max - min) + min

        self.__signal = sig


    # Создание зашумленного сигнала
    # Случайные значения имеют нормальное распределение с мат. ожиданием 0 и сред. квад. = noise
    def MakeNoiseSignal(self, noise=0.08):
        rng = np.random.default_rng()

        noise_signal = self.__signal + rng.standard_normal(self.__signal.size) * noise

        return Signal(self.Key, noise_signal)

    
    # Создание сигнала с БПФ 
    # Если включена нормалищация, то будет выдавать действительное значение преобразования сигнала
    def MakeFFTSignal(self, normilize=False) -> Signal:
        fft_signal = np.abs(rfft(self.Signal))
        if normilize:
            fft_signal /= fft_signal.size
            fft_signal *= 2

        return Signal(self.Key, fft_signal)


    # Создание фильтрованного сигнала
    # alpha и beta лучше смотреть на сайте, базовые значения подирались перебором
    # Get from https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html
    def MakeFilterSignal(self, alpha=1, beta=0.15) -> Signal:
        b, a = sci_signal.butter(alpha, beta)
        zi = sci_signal.lfilter_zi(b, a)

        z, _ = sci_signal.lfilter(b, a, self.Signal, zi=zi * self.Signal[0])
        z2, _ = sci_signal.lfilter(b, a, z, zi=zi * z[0])

        result_signal = sci_signal.filtfilt(b, a, self.Signal)

        return Signal(self.Key, result_signal)