import onnxruntime as ort
import numpy as np
from PIL import Image
import os

def preprocess(img_path):
    img = Image.open(img_path).convert("L").resize((160, 60))
    img_np = (np.array(img) / 255.0 - 0.5) / 0.5
    img_np = img_np.astype(np.float32)[None, None, :, :]
    return img_np

session = ort.InferenceSession("outputs/convert_1/captcha.onnx", providers=["DmlExecutionProvider"])
error_num = 0
for img in os.listdir("data/vaild"):
    # print(img)
    label_str = img.split('_')[0] 
    if len(label_str) != 4 or not label_str.isdigit():
        continue

    img_np = preprocess(f"data/vaild/{img}")
    outputs = session.run(None, {"input": img_np})
    preds = np.argmax(outputs[0], axis=2)
    preds = preds[0]

    label_np = np.array([int(c) for c in label_str])

    if not np.array_equal(preds, label_np):
        print("Predict: ", preds)
        print("Label:   ", label_np)
        error_num += 1

if error_num == 0:
    print(": )")
else:
    print(f"model have {error_num} errors")
