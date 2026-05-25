import os
import json
import glob
import torch
import numpy as np

from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T

class EEGImageDataset(Dataset):

    def __init__(self, json_files, image_root):

        self.files = json_files
        self.image_root = image_root

        # -------------------------
        # Build image index
        # -------------------------

        self.image_index = {}

        image_paths = glob.glob(
            os.path.join(image_root, "**", "*.jpg"),
            recursive=True
        )

        for path in image_paths:

            name = os.path.splitext(
                os.path.basename(path)
            )[0]

            self.image_index[name] = path

        # -------------------------
        # Image transforms
        # -------------------------

        self.transform = T.Compose([
            T.Resize((64, 64)),
            T.ToTensor(),
            T.Normalize(
                mean=[0.5, 0.5, 0.5],
                std=[0.5, 0.5, 0.5]
            )
        ])

    def __len__(self):
        return len(self.files)

    def _load_eeg(self, raw):

        channels = ["TP9", "AF7", "AF8", "TP10"]

        eeg = []

        for ch in channels:
            eeg.append(raw[ch])

        eeg = np.stack(eeg)

        eeg = torch.tensor(
            eeg,
            dtype=torch.float32
        )

        eeg = (
            eeg - eeg.mean(dim=1, keepdim=True)
        ) / (
            eeg.std(dim=1, keepdim=True) + 1e-6
        )

        return eeg

    def _resolve_image_path(self, data):

        phase = data["phase"]
        image_name = data["image_name"]

        # -------------------------
        # Perception
        # -------------------------

        if phase == "perception":

            filename = os.path.basename(image_name)
            name = os.path.splitext(filename)[0]

            return self.image_index[name]

        # -------------------------
        # Imagination
        # -------------------------

        elif phase == "imagination":

            return self.image_index[image_name]

        else:
            raise ValueError(
                f"Unknown phase: {phase}"
            )

    def __getitem__(self, idx):

        path = self.files[idx]

        with open(path, "r") as f:
            data = json.load(f)

        eeg = self._load_eeg(data["raw"])

        img_path = self._resolve_image_path(data)

        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)

        return eeg, image