import numpy as np
import onnxruntime as ort
from PIL import Image
import torchvision.transforms as transfroms

class MyModel:
    def __init__(self, model_path, captcha_len=4):
        self.captcha_len = captcha_len
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.transform = transfroms.Compose([
            transfroms.Resize((60, 160)),
            transfroms.Grayscale(),
            transfroms.ToTensor(),
            transfroms.Normalize((0.5,), (0.5,))
        ])

    def preprocess(self, image):
        if not isinstance(image, Image.Image):
            raise TypeError("Input must be a PIL.Image")
        tensor = self.transform(image).unsqueeze(0)
        return tensor.numpy()
    
    def classify(self, image):
        input_tensor = self.preprocess(image)
        outputs = self.session.run(None, {"input": input_tensor})
        preds = np.argmax(outputs[0], axis=2)
        return ''.join(str(d) for d in preds[0])