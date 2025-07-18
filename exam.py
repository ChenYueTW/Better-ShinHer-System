import json
from bs4 import BeautifulSoup
from login import getSession

record = json.load(open("record.json"))
session = getSession()

def get_exam_list():
    page = session.get(record["eventUrl"])
    parser = BeautifulSoup(page.text, "html.parser")

    return parser.find_all("option")

def get_exam_list_url():
    array = []
    for i in get_exam_list(session):
        value = i.get("value")
        if value in "student_subjects_number":
            array.append(value)
    
    return array

def get_exam_score_list(url):
    request = session.get(url)
    parser = BeautifulSoup(request.text, "html.parser")
    selfScore = parser.find("tr", id="color1")
    selfScore = list(filter((lambda s: s.text != ""), selfScore.find_all("td", class_="top center score")))
    
    return selfScore