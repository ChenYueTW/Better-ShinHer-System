import json
from bs4 import BeautifulSoup
from login import getSession
from flask import Blueprint

curriculum_app = Blueprint("curriculum", __name__)
record = json.load(open("record.json"))
url = record["timetableUrl"] + "/select_preceptor.asp?action=open_sel"
timetable_list = getSession().get(url)
timetable_list_parser = BeautifulSoup(timetable_list.text, "html.parser")

@curriculum_app.get("/curriculum/class_url")
def get_class_url():
    option = timetable_list_parser.find_all("option")

    for i in option:
        value = i.get("value")
        if value != "":
            return value
    
@curriculum_app.get("/curriculum/class_timetable")
def get_class_timetable():
    url = record["timetableUrl"] + get_class_url()
    page = getSession().get(url)
    parser = BeautifulSoup(page.text, "html.parser")

    table = parser.find("table", class_="TimeTable top left spacing2 padding2")

    return table