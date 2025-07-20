import json
import requests
from bs4 import BeautifulSoup
import requests.compat
from PIL import Image
from model import CaptchaCNN
from io import BytesIO
import torch
import matplotlib.pyplot as plt
from torchvision import transforms

record = json.load(open("../record.json"))
session = requests.Session()

model = CaptchaCNN()
model.load_state_dict(torch.load("outputs/run_2/captcha_cnn.pth"))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": record["informationUrl"]
}

transform = transforms.Compose([
    transforms.Resize((60, 160)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

true_num = 0
false_num = 0

while True:
    info_page = session.get(record["informationUrl"])
    info_page_parseer = BeautifulSoup(info_page.text, "html.parser")

    img_scr = info_page_parseer.find("img", id="imgvcode")["src"]
    capcha_url = requests.compat.urljoin(info_page.url, img_scr)

    response = session.get(capcha_url, headers=headers)
    img = Image.open(BytesIO(response.content))

    model.eval()
    plt.imshow(img)
    plt.axis("off")
    plt.show(block=False)

    with torch.no_grad():
        input_tensor = transform(img).unsqueeze(0)
        outputs = model(input_tensor)
        preds = torch.argmax(outputs, dim=2)

    print("predict: ", preds)

    text = input("true of false: ")
    plt.close()
    if text.lower() == "q":
        break
    elif text.lower() == "t":
        true_num += 1
    elif text.lower() == "f":
        false_num += 1

print(f"{true_num} True and {false_num} False")
print(f"Accuratly {true_num / (true_num + false_num) * 100:.2f}%")