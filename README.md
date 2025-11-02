# Muse2_ai 🧠✨

**Brainwave-powered image generation using the Muse 2 EEG headset**

---

## 🧩 Overview

**Muse2_ai** is an experimental project that explores the intersection between **neuroscience and artificial intelligence**.
The goal is to capture real-time EEG (electroencephalography) data from the **Muse 2 headband**, process the signals, and train an AI model capable of **visualizing what a person perceives or imagines** — effectively turning brain activity into visual representations.

The long-term objective is to train a generative model that can recreate **mental imagery** directly from EEG input.

---

## ⚙️ Features

- Real-time EEG data acquisition from **Muse 2** headset
- Signal preprocessing (filtering, normalization, feature extraction)
- Dataset generation for both *perception* and *imagination* phases
- JSON-based dataset structure for easy integration and debugging
- Modular AI pipeline for training and testing
- Visualization of reconstructed mental images

---

## 🧠 Data Pipeline

### 1. EEG Acquisition

Data is collected via the **Muse 2 SDK** or **Bluetooth interface**, streaming raw EEG signals from multiple channels.

### 2. Preprocessing

- Bandpass filtering (e.g., 1–40 Hz)
- Noise reduction and artifact removal (e.g., eye blinks, motion)
- Feature extraction (e.g., power spectrum, frequency bands)

### 3. Dataset Structure

Each sample consists of:

```json
{
  "timestamp": 1730337600,
  "mode": "perception", 
  "stimulus": "apple.jpg",
  "eeg_data": [...],
  "label": "apple"
}
```
