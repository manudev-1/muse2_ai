import torch
import torch.nn as nn

class ResBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()

        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
            nn.GELU(),
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
        )

        self.act = nn.GELU()

    def forward(self, x):
        return self.act(x + self.block(x))
    
class SelfAttention2D(nn.Module):
    def __init__(self, channels):
        super().__init__()

        self.query = nn.Conv2d(channels, channels // 8, 1)
        self.key   = nn.Conv2d(channels, channels // 8, 1)
        self.value = nn.Conv2d(channels, channels, 1)

        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        B, C, H, W = x.shape

        q = self.query(x).view(B, -1, H * W)
        k = self.key(x).view(B, -1, H * W)
        v = self.value(x).view(B, -1, H * W)

        attn = torch.softmax(q.transpose(1, 2) @ k, dim=-1)

        out = v @ attn.transpose(1, 2)
        out = out.view(B, C, H, W)

        return self.gamma * out + x

class ImageDecoder(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Linear(768, 1024 * 4 * 4),
            nn.GELU(),
            nn.LayerNorm(1024 * 4 * 4)
        )

        self.up1 = self._block(1024, 512)
        self.up2 = self._block(512, 256)
        self.up3 = self._block(256, 128)
        self.up4 = self._block(128, 64)

        self.out = nn.Conv2d(64, 3, kernel_size=3, padding=1)

    def _block(self, in_c, out_c):
        return nn.Sequential(
            nn.ConvTranspose2d(in_c, out_c, kernel_size=4, stride=2, padding=1),
            nn.GELU(),
            ResBlock(out_c),
            SelfAttention2D(out_c)
        )

    def forward(self, z):

        x = self.fc(z)

        x = x.view(x.size(0), 1024, 4, 4)

        x = self.up1(x)
        x = self.up2(x)
        x = self.up3(x)
        x = self.up4(x)

        x = self.out(x)

        x = torch.tanh(x)

        return x