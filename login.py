import requests
import json
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from MyModel import MyModel

session = None

def getSession(max_retries=3):
    global session
    if session is not None:
        return session
    
    record = json.load(open("record.json"))
    session = requests.Session()
    ocr = MyModel("model/outputs/convert_2/captcha_optimized.onnx")

    for attempt in range(1, max_retries + 1):
        try:
            info_page = session.get(record["informationUrl"])
            parser = BeautifulSoup(info_page.text, "html.parser")
            
            token_input = parser.find("input", {"name": "__RequestVerificationToken"})
            token = token_input["value"] if token_input else ""

            img_scr = parser.find("img", id="imgvcode")["src"]
            capcha_url = requests.compat.urljoin(info_page.url, img_scr)
    
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Referer": record["informationUrl"]
            }

            resp = session.get(capcha_url, headers=headers)
            img = Image.open(BytesIO(resp.content))
            result = ocr.classify(img)
            print("Predict verify number: ", result)

            payload = {
                "__RequestVerificationToken": token,
                "division": "senior",
                "Loginid": record["userId"],
                "LoginPwd": record["userPwd"],
                "Uid": "",
                "vcode": result,
            }

            login_response = session.post(record["loginUrl"], data=payload, headers=headers)

            if "登入失敗" in login_response.text:
                raise Exception("登入失敗，請檢查帳號密碼或驗證碼")
            else:
                print("Login success!")
                return session

        except Exception as e:
            print(f"Error: {e}")

    return session