from bs4 import BeautifulSoup
import json
import login
import exam
import moral
import absentation
import curriculum

session = login.getSession()

for i in exam.get_exam_list():
    print(i)
# print(exam.get)