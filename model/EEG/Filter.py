from scipy.signal import butter, lfilter, iirnotch, filtfilt
from numpy import ndarray, max as np_max, abs as np_abs

class Filter:

    @staticmethod
    def bandpass_filter(data: ndarray, low: int, high: int, fs:int, order=5):
        """Bandpass filter for EEG data.

        Args:
            data (ndarray): EEG Raw data.
            low (int): Lower cutoff frequency.
            high (int): Higher cutoff frequency.
            fs (int): Sampling frequency.
            order (int, optional):  Defaults to 5.

        Returns:
            list: The output of the digital filter

            list: optional, If zi is None, this is not returned, otherwise, zf holds the final filter delay values.
        """
        nyq = 0.5 * fs
        low /= nyq
        high /= nyq
        b, a = butter(order, [low, high], btype='band')
        return lfilter(b, a, data)
    
    @staticmethod
    def notch_filter(signal: ndarray, fs=256, f0=50.0, Q=30.0) -> ndarray:
        b, a = iirnotch(f0, Q, fs)
        return filtfilt(b, a, signal)

    @staticmethod
    def is_clean(signal: ndarray, threshold: float = 150.0) -> bool:
        return np_max(np_abs(signal)) < threshold