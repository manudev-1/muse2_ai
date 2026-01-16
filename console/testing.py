import matplotlib.pyplot as plt
import time
from collections import deque

from model.EEG.Reader import Reader

def main():
    reader = Reader()
    print("✅ EEG stream found. Starting live plot...")

    channels = ['TP9', 'AF7', 'AF8', 'TP10']
    bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

    powers_over_time = {ch: deque(maxlen=50) for ch in channels}

    plt.ion()
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for ax, ch in zip(axes, channels):
        ax.set_title(f"Canale {ch}")
        ax.set_xlabel("Finestra temporale")
        ax.set_ylabel("Potenza (µV²)")
        ax.grid(True)

    while True:
        bandpowers = reader.raw_to_psd(seconds=2)

        if bandpowers is None:
            continue

        print(bandpowers)
        for ch in channels:
            powers_over_time[ch].append(bandpowers[ch])

        for i, ch in enumerate(channels):
            ax = axes[i]
            ax.cla()
            ax.set_xlabel("Finestra temporale")
            ax.set_ylabel("Potenza (µV²)")
            ax.grid(True)

            for band in bands:
                y = [sample[band] for sample in powers_over_time[ch]]
                ax.plot(range(len(y)), y, label=band)

            ax.legend()

        plt.tight_layout()
        plt.pause(0.01)

        print("Bandpowers:", bandpowers)


