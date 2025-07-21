import torch
import os
from model import CaptchaCNN

model = CaptchaCNN(num_chars=10, captcha_len=4)
model.load_state_dict(torch.load("outputs/run_3/captcha_cnn.pth", map_location="cpu"))
model.eval()

base_foldername = "convert"
foldername = "convert_1"
i = 1
while os.path.exists(f"outputs/{foldername}"):
    i += 1
    foldername = f"{base_foldername}_{i}"
os.makedirs(f"outputs/{foldername}", exist_ok=True)

dummy_input = torch.randn(1, 1, 60, 160)
torch.onnx.export(model, dummy_input, f"outputs/{foldername}/captcha.onnx",
                  export_params=True,
                  input_names=["input"], output_names=["output"],
                  dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
                    opset_version=11)