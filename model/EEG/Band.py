from numpy import ndarray, trapezoid

from model.EEG.Filter import Filter

class Band:

    @staticmethod
    def compute_bandpower(freqs: ndarray, psd: ndarray) -> float:
        """Calculate the average power of the signal in a specific frequency band.

        Args:
            freqs (ndarray): frequencies correspondents to the psd
            psd (ndarray): density power spectrum of the signal
            low (float): lower bound frequency
            high (float): higher bound frequency

        Returns:
            float: total power in the frequency band
        """
        powers = {}
        for name, (low, high) in Filter.bands.items():
            mask = (freqs >= low) & (freqs <= high)
            powers[name] = float(trapezoid(psd[mask], freqs[mask]))
        return powers