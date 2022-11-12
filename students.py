import requests
from bs4 import BeautifulSoup
from summary import summary


def students(year, exam_type, school_number):
    url = ""
    return students


def scrap_students(soup, index):
    data = []
    return data


def split_after(text):
    subjects = {}
    values = []
    temp = ""

    for i in range(0, len(text) - 1):
        temp += text[i]
        if text[i] == '\'' and text[i + 1] == ' ':
            values.append(temp)
            temp = ""

    for v in values:
        q = v.split('-')
        subject = q[0].strip()
        grade = q[1].strip().strip('\'')
        subjects.update({subject: grade})

    return subjects
