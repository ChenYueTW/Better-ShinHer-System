import os
import requests
from PIL import Image
from io import BytesIO
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import ddddocr

record = json.load(open("../record.json"))
session = requests.Session()
ocr = ddddocr.DdddOcr()
ocr.set_ranges("0123456789")

SAVE_DIR = "data/train"
os.makedirs(SAVE_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": record["informationUrl"]
}

while True:
    info_page = session.get(record["informationUrl"])
    info_page_parser = BeautifulSoup(info_page.text, "html.parser")

    img_scr = info_page_parser.find("img", id="imgvcode")["src"]
    capcha_url = requests.compat.urljoin(info_page.url, img_scr)

    response = session.get(capcha_url, headers=headers)
    img = Image.open(BytesIO(response.content))
    result = ocr.classification(img)
    plt.imshow(img)
    plt.axis("off")
    plt.show(block=False)

    print(result)
    label = input("q or new label: ")
    plt.close()

    if (label.lower() == "q"):
        label = result

    if len(label) != 4 or not label.isdigit():
        print("ERROR")
        continue

    base_filename = os.path.join(SAVE_DIR, label)
    i = 1
    filename = f"{base_filename}.png"
    while os.path.exists(filename):
        filename = f"{base_filename}_{i}.png"
        i += 1
    img.save(filename)
    print(f"已儲存 {filename}")
