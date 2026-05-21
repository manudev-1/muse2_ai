from pipeline.EEGEncoder import EEGEncoder
import torch

def main():
    model = EEGEncoder()

    dummy_input = torch.randn(
        8,      # batch size
        4,      # EEG channels
        512     # time samples
    )

    output = model(dummy_input)

    print("Output shape:", output.shape)


if __name__ == "__main__":
    main()