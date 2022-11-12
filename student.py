import requests, json
from bs4 import BeautifulSoup

from summary import summary
from students import split_after


def student(year, exam_type, school_number, student_number):
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

        if school_number.startswith('p'):
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

        if school_number.startswith('p'):
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

    if data.status_code == 200:
        s = summary(year, exam_type, school_number)
        student_data = {
            "examination_number": f"{school_number.upper()}/{student_number}",
            "year_of_exam": year,
            "exam_type": exam_type,
            "gender": "*",
            "school_name": s.get('school_name'),
            "division": "*",
            "points": "*",
            "subjects": {}
        }

        found = False

        students_table = soup.find_all("table")[index]
        for tr in students_table.find_all("tr"):
            row = []
            for td in tr.find_all("td"):
                row.append(td.text.strip('\n'))

            if row[0] == student_data['examination_number']:
                student_data["gender"] = row[1]
                student_data["division"] = row[3]
                student_data["points"] = row[2]
                student_data["subjects"] = split_after(row[4])

                found = True

        if not found:
            raise Exception(f"Wrong Examination Number {student_data['examination_number']}")
        else:
            return student_data
    else:
        raise Exception(f"failed to connect to server \n Error Code {data.status_code}")
