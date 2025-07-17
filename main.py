from bs4 import BeautifulSoup
import json
import login

record = json.load(open("record.json"))
session = login.login()

exam_list_page = session.get(record["selectExamUrl"])
exam_list_parser = BeautifulSoup(exam_list_page.text, "html.parser")
exam_list = exam_list_parser.findAll("option")

for i in exam_list:
    value = i.get("value")
    if "student_subjects_number.asp" in value:
        print(value)