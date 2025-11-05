import matplotlib.pyplot as plt
import time
from collections import deque

from model.EEGReader import EEGReader

def main():
    reader = EEGReader()
    print("✅ EEG stream found. Starting live plot...")

    channels = ['TP9', 'AF7', 'AF8', 'TP10']
    bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

    # deque per memorizzare la storia delle potenze (50 finestre massime)
    powers_over_time = {ch: deque(maxlen=50) for ch in channels}

    # --- Setup grafico ---
    plt.ion()  # modalità interattiva
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for ax, ch in zip(axes, channels):
        ax.set_title(f"Canale {ch}")
        ax.set_xlabel("Finestra temporale")
        ax.set_ylabel("Potenza (µV²)")
        ax.grid(True)

    while True:
        # leggi nuovi dati
        bandpowers = reader.raw_to_psd(seconds=2)

        if bandpowers is None:
            continue

        print(bandpowers)
        # aggiorna deque con nuovi dati
        for ch in channels:
            powers_over_time[ch].append(bandpowers[ch])

        # aggiorna il grafico
        for i, ch in enumerate(channels):
            ax = axes[i]
            ax.cla()  # cancella vecchie linee
            ax.set_title(f"Canale {ch}")
            ax.set_xlabel("Finestra temporale")
            ax.set_ylabel("Potenza (µV²)")
            ax.grid(True)

            # disegna ogni banda
            for band in bands:
                y = [sample[band] for sample in powers_over_time[ch]]
                ax.plot(range(len(y)), y, label=band)

            ax.legend()

        plt.tight_layout()
        plt.pause(0.01)  # breve pausa per aggiornare il grafico

        # stampa opzionale dei valori correnti
        print("Bandpowers:", bandpowers)


