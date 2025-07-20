import os
import matplotlib.pyplot as plt
from PIL import Image

IMAGE_DIR = "data/train"

for img in os.listdir(IMAGE_DIR):
    image_path = os.path.join(IMAGE_DIR, img)
    image = Image.open(image_path).convert("L")

    plt.imshow(image)
    plt.axis("off")
    plt.show(block=False)

    print(img)
    text = input("q or new label: ")
    plt.close()
    if text == "q":
        continue

    if len(text) != 4 or not text.isdigit():
        print("renew input")
        text = input("q or new label")

    base = os.path.join(IMAGE_DIR, text)
    i = 0
    filename = f"{base}.png"
    while os.path.exists(filename):
        i += 1
        filename = f"{base}_{i}.png"
    
    os.rename(image_path, filename)