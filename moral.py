import json
from bs4 import BeautifulSoup
from login import getSession
from flask import Blueprint

moral_app = Blueprint("moral", __name__)
record = json.load(open("record.json"))
url = record["eventUrl"] + "/moralculture_%20bonuspenalty.asp"
page = getSession().get(url)
parser =  BeautifulSoup(page.text, "html.parser")

@moral_app.get("/moral/award_list")
def get_award_list():
    data_row = parser.find_all("tr", class_="dataRow")
    data_row = list(filter(lambda s: s.find("td", class_="txt_02 si_15 center").text == "獎勵", data_row))
    return data_row

@moral_app.get("/moral/punish_list")
def get_punish_list():
    data_row = parser.find_all("tr", class_="dataRow")
    data_row = list(filter(lambda s: s.find("td", class_="txt_02 si_15 center").text == "懲處", data_row))
    
    if data_row is None or data_row == []:
        return "Not have punish!"
    else:
        return data_row