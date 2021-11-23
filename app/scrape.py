from bs4 import BeautifulSoup
import requests


def schools(year, exam_type):
    url = ""
    if (exam_type.lower() == 'csee'):
        url = f"https://onlinesys.necta.go.tz/results/{year}/csee/csee.htm"
    elif exam_type.lower() == 'acsee':
        url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/index.htm"
    else:
        url = f"https://onlinesys.necta.go.tz/results/{year}/csee/csee.htm"

    schools = {}

    data = requests.get(url)
    if data.status_code == 200:
        soup = BeautifulSoup(data.text, 'html.parser')

        schools = []

        for font in soup.find_all('font'):
            for a in font.find_all('a'):
                clean = a.text.strip('\n')
                school = clean.split(' ')

                school_name = ""
                for s in school[1:]:
                    school_name = f"{school_name} {s}"

                schools.append({"school_name": school_name,
                               "registration_number": school[0]})

        schools = schools[27:]
        schools.insert(0, {"year": year, "level": exam_type})

        schools_data = {
            "exam_type": exam_type,
            "year_of_exam": year,
            "number_of_schools": len(schools),
            "description": f"a list of schools in {exam_type} year {year}",
            "schools": schools
        }
        print(schools_data)
        return schools_data
    else:
        raise Exception(
            f"failed to access {url}. \n Error Code: {data.status_code}")


def schoolSummary(year, examp_type, school_number):
    url = f"https://onlinesys.necta.go.tz/results/{year}/{examp_type}/results/{school_number}.htm"

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    if data.status_code != 200:
        raise Exception("failed to connect to server")
    else:
        summary = {}
        rows = []

        tables = soup.find_all('table')
        for tr in tables[0].find_all('tr'):
            r = []
            for td in tr.find_all('td'):
                r.append(td.text.strip('\n'))
            rows.append(r)

        for i in range(1, 6):
            div = {
                rows[0][i]: {
                    "F": rows[1][i],
                    "M": rows[2][i],
                    "T": rows[3][i],
                }
            }
            summary.update(div)
            print(summary)
        return summary


def splitAfter(text):
    subjects = {}
    values = []
    temp = ""
    for i in range(0, len(text)-1):
        temp += text[i]
        if text[i] == '\'' and text[i+1] == ' ':
            values.append(temp)
            temp = ""

    for v in values:
        q = v.split('-')
        subject = q[0].strip()
        grade = q[1].strip().strip('\'')
        subjects.update({subject: grade})

    return subjects


def student(year, exam_type, school_number, student_number):
    url = f"https://onlinesys.necta.go.tz/results/{year}/{exam_type}/results/{school_number}.htm"

    print(url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    rows = []

    if data.status_code != 200:
        raise Exception(f"Failed to connect to server")
    else:
        index = 0
        if int(year) < 2019:
            index = 0
        elif int(year) == 2019 and exam_type == 'acsee':
            index = 0
        else:
            index = 2

        students_table = soup.find_all("table")

        for _table in students_table[index].find_all("tr"):
            row = []

            for _data in _table.find_all("td"):
                row.append(_data.text.strip('\n'))
            rows.append(row)
        complete_number = f"{school_number.upper()}/{student_number}"
        student_details = {}

        found = False

        for r in rows:
            if r[0] == complete_number:
                subjects = r[4:]
                student_details["number"] = complete_number
                student_details["gender"] = r[1]
                student_details["division"] = r[3]
                student_details["points"] = r[2]
                student_details["subjects"] = splitAfter(subjects[0])

                found = True

        if not found:
            raise Exception(f"Wrong Examination Number {complete_number}")
        else:
            print(student_details)
            return student_details


if __name__ == '__main__':
    # schools('2020', 'csee')
    # schoolSummary('2020', 'csee', 'p0217')
    student('2020', 'csee', 's1319', '0014')
