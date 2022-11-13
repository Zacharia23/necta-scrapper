import requests
from bs4 import BeautifulSoup
from summary import summary


def students(year, exam_type, school_number):
    url = ""
    exam_type = exam_type.lower()
    school_number = school_number.lower()
    year = int(year)
    index = 0

    if exam_type == 'acsee':
        if year == 2022:
            url = f"https://matokeo.necta.go.tz/acsee2022/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/results/{school_number}.htm"

        if school_number.startswith("p"):
            if year > 2019:
                index = 1
            else:
                index = 0
        else:
            if year > 2019:
                index = 2
            else:
                index = 0

    elif exam_type == 'csee':
        if int(year) == 2021:
            url = f"https://onlinesys.necta.go.tz/results/2021/csee/results/{school_number}.htm"
        elif int(year) > 2014:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/{school_number}.htm"

        if school_number.startswith("p"):
            if year > 2018:
                index = 1
            else:
                index = 0

        else:
            if year > 2018:
                index = 2
            else:
                index = 0

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    if data.status_code != 200:
        raise Exception(f"Failed to connect to the server \nError Code {data.status_code}")
    else:
        s = summary(year, exam_type, school_number)

        students = {
            "school_number": school_number,
            "school_name": s.get('school_name'),
            "year_of_exam": year,
            "exam_type": exam_type,
            "number_of_students": s.get('number_of_students'),
            "students": []
        }

        student_data = scrap_students(soup, index)
        students["students"] = student_data

    return students


def scrap_students(soup, index):
    students_table = soup.find_all("table")[index]
    data = []

    for tr in students_table.find_all("tr")[1:]:
        row = []
        for td in tr.find_all("td"):
            row.append(td.text.strip('\n'))

        subjects = split_after(row[4])

        student = {
            "examination_number": row[0],
            "gender": row[1],
            "division": row[3],
            "points": row[2],
            "subjects": subjects
        }

        data.append(student)

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
