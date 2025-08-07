import json
from bs4 import BeautifulSoup
from login import getSession
from flask import Blueprint, request

exam_app = Blueprint("exam", __name__)
record = json.load(open("record.json"))
session = getSession()

@exam_app.get("/exam/list")
def get_exam_list():
    page = session.get(record["selectExamUrl"])
    parser = BeautifulSoup(page.text, "html.parser")

    result = [x.text.strip() for x in parser.find_all("option")]
    return {"result": result}

@exam_app.get("/exam/url")
def get_exam_list_url():
    page = session.get(record["selectExamUrl"])
    parser = BeautifulSoup(page.text, "html.parser")
    result = []

    for i in parser.find_all("option"):
        value = i.get("value")
        if "student_subjects_number" in value:
            result.append(value.strip())

    return {"result": result}

@exam_app.post("/exam/score_list")
def get_exam_self_score_list():
    data = request.json
    
    url = data.get("url")
    if not url:
        return {"error": "Missing URL"}, 400
    
    response = session.get(record["eventUrl"] + url)
    parser = BeautifulSoup(response.text, "html.parser")
    selfScore = parser.find("tr", id="color1")
    if not selfScore:
        return {"error": "Missing self score"}, 404
    
    cells = selfScore.find_all("td", class_="top center score")
    cells = list(filter((lambda s: s.text != ""), cells))
    
    result = [x.text.strip() for x in cells]
    return {"result": result}