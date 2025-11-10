from numpy import ndarray, trapezoid

class Band:
    
    bands = {
        'Delta': (0.5, 4),
        'Theta': (4, 8),
        'Alpha': (8, 12),
        'Beta': (12, 30),
        'Gamma': (30, 50)
    }

    @staticmethod
    def compute_bandpower(freqs: ndarray, psd: ndarray) -> dict:
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
        for name, (low, high) in Band.bands.items():
            mask = (freqs >= low) & (freqs <= high)
            powers[name] = float(trapezoid(psd[mask], freqs[mask]))
        return powers