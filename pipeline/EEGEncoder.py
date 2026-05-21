import torch
import torch.nn as nn
import torch.nn.functional as F


class EEGEncoder(nn.Module):
    def __init__(self, embedding_dim=256, dropout=0.3):
        super().__init__()

        # -------------------------
        # Feature Extraction Blocks
        # -------------------------

        self.features = nn.Sequential(

            nn.Conv1d(
                in_channels=4,
                out_channels=32,
                kernel_size=7,
                padding=3
            ),
            
            nn.BatchNorm1d(32),
            nn.GELU(),
            nn.MaxPool1d(kernel_size=2),

            nn.Conv1d(
                in_channels=32,
                out_channels=64,
                kernel_size=5,
                padding=2
            ),
            nn.BatchNorm1d(64),
            nn.GELU(),
            nn.MaxPool1d(kernel_size=2),

            nn.Conv1d(
                in_channels=64,
                out_channels=128,
                kernel_size=5,
                padding=2
            ),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.MaxPool1d(kernel_size=2),

            nn.Conv1d(
                in_channels=128,
                out_channels=256,
                kernel_size=3,
                padding=1
            ),
            nn.BatchNorm1d(256),
            nn.GELU(),
        )

        # Temporal aggregation
        self.pool = nn.AdaptiveAvgPool1d(1)

        # -------------------------
        # Projection Head
        # -------------------------

        self.projection = nn.Sequential(
            nn.Linear(256, 256),
            nn.GELU(),
            nn.LayerNorm(256),
            nn.Dropout(dropout),
            nn.Linear(256, embedding_dim)
        )

    def forward(self, x):
        """
        x shape:
        [B, 4, 512]
        """

        x = self.features(x)

        # Shape:
        # [B, 256, 64]

        x = self.pool(x)

        # Shape:
        # [B, 256, 1]

        x = x.squeeze(-1)

        # Shape:
        # [B, 256]

        z = self.projection(x)

        z = F.normalize(z, p=2, dim=1)

        return z
    
if __name__ == "__main__":

    model = EEGEncoder()

    dummy_input = torch.randn(
        8,      # batch size
        4,      # EEG channels
        512     # time samples
    )

    output = model(dummy_input)

    print("Output shape:", output.shape)