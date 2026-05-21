import torch
import matplotlib.pyplot as plt

from pipeline.EEGEncoder import EEGEncoder
from pipeline.LatentMapper import LatentMapper
from pipeline.ImageDecoder import ImageDecoder

def show_image(tensor_img):
    img = tensor_img.detach().cpu()

    img = (img + 1) / 2

    img = img.permute(1, 2, 0)  

    plt.imshow(img)
    plt.axis("off")
    plt.show()

def main():
    x_eeg = torch.randn(8, 4, 512)

    eeg_encoder = EEGEncoder()
    mapper = LatentMapper()
    image_decoder = ImageDecoder()

    z_eeg = eeg_encoder(x_eeg)
    print(z_eeg.shape)
    z_img = mapper(z_eeg)
    print(z_img.shape)
    image = image_decoder(z_img)
    print(image.shape)

    show_image(image[0])


if __name__ == "__main__":
    main()