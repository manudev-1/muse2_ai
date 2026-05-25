import os
import glob

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision.transforms as T
from torchvision.utils import save_image

# ============================================
# IMPORT MODELS
# ============================================

from pipeline.training.EEGImageDataset import EEGImageDataset
from pipeline.EEGEncoder import EEGEncoder
from pipeline.LatentMapper import LatentMapper
from pipeline.ImageDecoder import ImageDecoder

def train():

    # ----------------------------------------
    # Device
    # ----------------------------------------

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"\nUsing device: {device}\n")

    # ----------------------------------------
    # Dataset
    # ----------------------------------------

    dataset_path = "dataset"
    image_root = "trainer/images"

    json_files = glob.glob(
        os.path.join(dataset_path, "*.json")
    )

    dataset = EEGImageDataset(
        json_files=json_files,
        image_root=image_root
    )

    loader = DataLoader(
        dataset,
        batch_size=4,      # piccolo batch per PC meno potenti
        shuffle=True,
        num_workers=0
    )

    print(f"Dataset size: {len(dataset)}")

    # ----------------------------------------
    # Models
    # ----------------------------------------

    eeg_encoder = EEGEncoder().to(device)
    latent_mapper = LatentMapper().to(device)
    image_decoder = ImageDecoder().to(device)

    # ----------------------------------------
    # Optimizer
    # ----------------------------------------

    optimizer = torch.optim.AdamW(
        list(eeg_encoder.parameters()) +
        list(latent_mapper.parameters()) +
        list(image_decoder.parameters()),
        lr=1e-4,
        weight_decay=1e-2
    )

    # ----------------------------------------
    # Training settings
    # ----------------------------------------

    epochs = 20

    # ----------------------------------------
    # Training loop
    # ----------------------------------------

    for epoch in range(epochs):

        eeg_encoder.train()
        latent_mapper.train()
        image_decoder.train()

        total_loss = 0.0

        for batch_idx, (eeg, target_img) in enumerate(loader):

            eeg = eeg.to(device)
            target_img = target_img.to(device)

            # --------------------------------
            # Forward
            # --------------------------------

            z_eeg = eeg_encoder(eeg)

            z_img = latent_mapper(z_eeg)

            pred_img = image_decoder(z_img)

            # --------------------------------
            # Reconstruction loss
            # --------------------------------

            loss = F.l1_loss(
                pred_img,
                target_img
            )

            # --------------------------------
            # Backprop
            # --------------------------------

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

            # --------------------------------
            # Logs
            # --------------------------------

            if batch_idx % 10 == 0:

                print(
                    f"Epoch [{epoch+1}/{epochs}] "
                    f"Batch [{batch_idx}/{len(loader)}] "
                    f"Loss: {loss.item():.4f}"
                )

        avg_loss = total_loss / len(loader)

        print(
            f"\nEpoch {epoch+1} completed "
            f"| Avg Loss: {avg_loss:.4f}\n"
        )

        # ------------------------------------
        # Save sample output
        # ------------------------------------

        with torch.no_grad():

            sample = (pred_img[:4] + 1) / 2

            save_image(
                sample,
                f"sample_epoch_{epoch+1}.png",
                nrow=2
            )

        # ------------------------------------
        # Save checkpoints
        # ------------------------------------

        torch.save(
            eeg_encoder.state_dict(),
            "eeg_encoder.pt"
        )

        torch.save(
            latent_mapper.state_dict(),
            "latent_mapper.pt"
        )

        torch.save(
            image_decoder.state_dict(),
            "image_decoder.pt"
        )

    print("\nTraining completed.\n")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    train()