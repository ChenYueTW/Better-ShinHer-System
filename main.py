from bs4 import BeautifulSoup
import json
import login
import exam
import moral
import absentation
import curriculum

session = login.getSession()

print(curriculum.get_class_timetable())