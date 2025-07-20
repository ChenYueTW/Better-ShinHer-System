import os
import torch
from torch.utils.data import Dataset
from PIL import Image

class CaptchaDataset(Dataset):
    def __init__(self, image_dir, transform=None, captcha_len=4, allowed_chars="0123456789"):
        self.image_dir = image_dir
        self.transform = transform
        self.captcha_len = captcha_len
        self.allowed_chars = allowed_chars
        self.char_to_index = {c: i for i, c in enumerate(allowed_chars)}

        self.image_files = []
        for f in os.listdir(image_dir):
            name, ext = os.path.splitext(f)
            label_part = name.split('_')[0]
            if ext.lower() in [".png", ".jpg", "jpeg"] and \
                len(label_part) == captcha_len and \
                all(c in self.allowed_chars for c in label_part):
                self.image_files.append(f)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, index):
        image_name = self.image_files[index]
        # print(image)
        label_str = os.path.splitext(image_name)[0].split('_')[0]
        
        label = torch.tensor([self.char_to_index[c] for c in label_str], dtype=torch.long)

        image_path = os.path.join(self.image_dir, image_name)
        image = Image.open(image_path).convert("L")

        if self.transform:
            image = self.transform(image)

        return image, label