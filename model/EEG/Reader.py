from pylsl import StreamInlet, resolve_streams
from numpy import array
from scipy.signal import welch

from model.EEG.Filter import Filter
from model.EEG.Band import Band
from log.__print import print

class Reader:
    def __init__(self, fs: int = 256):
        streams = resolve_streams()
        if not streams:
            raise RuntimeError("No EEG stream found. Make sure your EEG device is ON, connected and streaming data. Also Have you \"muselsl stream\" on another terminal?")
        
        self.inlet = StreamInlet(streams[0])
        self.fs = fs

    def read_sample(self):
        sample, timestamp = self.inlet.pull_sample()
        return sample, timestamp
    
    def raw_to_psd(self, seconds: int = 2) -> tuple[dict, dict] | None:
        n_samples = self.fs * seconds
        channels_data = {ch: [] for ch in ['TP9', 'AF7', 'AF8', 'TP10']}

        while len(channels_data['TP10']) < n_samples:
            sample, _ = self.read_sample()
            for ch_name, value in zip(channels_data.keys(), sample):
                channels_data[ch_name].append(value)
        print("Channel data has been loaded")

        for ch_name in channels_data:
            channels_data[ch_name] = array(channels_data[ch_name])

        result = {}
        for ch_name, data in channels_data.items():
            if not Filter.is_clean(data):
                print("Channel data was unclear")
                return None

        for ch_name, data in channels_data.items():
            filtered = Filter.bandpass_filter(data, low=1, high=50, fs=self.fs, order=5)

            filtered = Filter.notch_filter(filtered, fs=self.fs, f0=50.0, Q=30.0)

            freqs, psd = welch(filtered, fs=self.fs, nperseg=256)

            result[ch_name] = Band.compute_bandpower(freqs, psd)
            
            print("Clear channel data has been found")

        return result, channels_data