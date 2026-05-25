import torch

from pipeline.EEGEncoder import EEGEncoder
from pipeline.LatentMapper import LatentMapper

def main():
    x_eeg = torch.randn(8, 4, 512)
    eeg_encoder = EEGEncoder()

    mapper = LatentMapper()

    z_eeg = eeg_encoder(x_eeg)
    z_img = mapper(z_eeg)
    z_img_mean = z_img.mean(dim=0, keepdim=True)

    print(z_eeg.shape)
    print(z_img_mean.shape)

if __name__ == "__main__":
    main()