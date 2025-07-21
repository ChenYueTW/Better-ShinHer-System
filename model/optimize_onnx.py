import onnx
from onnxsim import simplify

model = onnx.load("outputs/convert_2/captcha.onnx")

model_simplified, check = simplify(model)

if check:
    onnx.save(model_simplified, "outputs/convert_2/captcha_optimized.onnx")
    print("Succeess optimize model!")
else:
    print("Failed")