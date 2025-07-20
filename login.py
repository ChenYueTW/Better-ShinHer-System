import requests
import json
from bs4 import BeautifulSoup
import ddddocr
from io import BytesIO
from PIL import Image

session = None

def getSession():
    global session
    if session is not None:
        return session
    
    record = json.load(open("record.json"))
    session = requests.Session()
    
    info_page = session.get(record["informationUrl"])
    parser = BeautifulSoup(info_page.text, "html.parser")

    ocr = ddddocr.DdddOcr(beta=True)
    ocr.set_ranges("0123456789")

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
    result = ocr.classification(img)

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