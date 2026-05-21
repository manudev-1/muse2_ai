import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()

        self.block = nn.Sequential(
            nn.Linear(dim, dim * 2),
            nn.GELU(),
            nn.Linear(dim * 2, dim),
            nn.LayerNorm(dim)
        )

    def forward(self, x):
        return x + self.block(x)

class LatentMapper(nn.Module):
    def __init__(self):
        super().__init__()

        # -------------------------
        # Feature Extraction Blocks
        # -------------------------

        self.input_proj = nn.Sequential(
            nn.Linear(256, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(0.2),
        )

        self.res_blocks = nn.Sequential(
            ResidualBlock(512),
            ResidualBlock(512),
        )

        self.output_proj = nn.Sequential(
            nn.Linear(512, 768),
            nn.LayerNorm(768),
            nn.Tanh()
        )

    def forward(self, z_egg):
        # [B, 256] -> [B, 512]
        x = self.input_proj(z_egg)

        # residual blocks
        x = self.res_blocks(x)

        # [B, 512] -> [B, 768]
        z_img = self.output_proj(x)

        return z_img