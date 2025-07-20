import json
from bs4 import BeautifulSoup
from login import getSession

record = json.load(open("record.json"))
url = record["eventUrl"] + "/absentation_skip_school.asp"
page = getSession().get(url)
parser = BeautifulSoup(page.text, "html.parser")

def get_absentation_table():
    table = parser.find("table", class_="padding2 spacing0")

    return table

def get_absentation_total():
    table = parser.find("table", class_="si_12 collapse padding2 spacing0")

    return table