import torch
import torch.nn as nn
import torch.nn.functional as Function

class CaptchaCNN(nn.Module):
    def __init__(self, num_chars=10, captcha_len=4):
        super(CaptchaCNN, self).__init__()
        self.captcha_len = captcha_len
        self.num_chars = num_chars

        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )

        self.flatten = nn.Flatten()
        self.fc = nn.Sequential(
            nn.Linear(128 * 7 * 20, 1024),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(1024, captcha_len * num_chars)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.flatten(x)
        x = self.fc(x)
        x = x.view(-1, self.captcha_len, self.num_chars)

        return x