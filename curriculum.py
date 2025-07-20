import json
from bs4 import BeautifulSoup
from login import getSession

record = json.load(open("record.json"))
url = record["timetableUrl"] + "/select_preceptor.asp?action=open_sel"
timetable_list = getSession().get(url)
timetable_list_parser = BeautifulSoup(timetable_list.text, "html.parser")

def get_class_url():
    option = timetable_list_parser.find_all("option")

    for i in option:
        value = i.get("value")
        if value != "":
            return value
        
def get_class_timetable():
    url = record["timetableUrl"] + get_class_url()
    page = getSession().get(url)
    parser = BeautifulSoup(page.text, "html.parser")

    table = parser.find("table", class_="TimeTable top left spacing2 padding2")

    return table