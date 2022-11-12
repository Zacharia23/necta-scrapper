from bs4 import BeautifulSoup
import requests


def schools(year, exam_type):
    url = ""
    skip = 0

    if exam_type.lower() == 'csee':
        if int(year) == 2021:
            url = f"https://onlinesys.necta.go.tz/results/2021/csee/csee.htm"
        elif int(year) == 2016:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/index.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/csee/csee.htm"

        if int(year) > 2014:
            skip = 28

    elif exam_type.lower() == 'acsee':
        if int(year) == 2022:
            url = f"https://matokeo.necta.go.tz/acsee2022/index.htm"
        elif int(year) > 2019:
            url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/index.htm"
        elif int(year) == 2014:
            url = f"https://onlinesys.necta.go.tz/results/2014/acsee/"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/acsee/acsee.htm"

        if int(year) > 2015:
            skip = 27

    else:
        raise Exception(f"Invalid Exam Type {exam_type}")

    data = requests.get(url)
    if data.status_code == 200:
        soup = BeautifulSoup(data.text, 'html.parser')

        schools = []

        for font in soup.find_all('font'):
            for a in font.find_all('a'):
                clean = a.text.strip('\n\r')
                school = clean.split(' ')

                school_name = ""
                for s in school[1:]:
                    school_name = f"{school_name} {s}"

                schools.append({"school_name": school_name, "school_number": school[0]})

        schools = schools[skip:]

        schools_data = {
            "exam_type": exam_type,
            "year_of_exam": year,
            "number_of_schools": len(schools),
            "description": f"list of schools and centers that participated in {exam_type} in {year}",
            "schools": schools
        }

        return schools_data
    else:
        raise Exception(f"Failed to access {url}\nResponse code: {data.status_code}")
