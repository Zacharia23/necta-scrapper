import requests
from bs4 import BeautifulSoup


def summary(year, exam_type, school_number):
    url = ""
    exam_type = exam_type.lower()
    school_number = school_number.lower()

    if exam_type == 'acsee':
        if int(year) == 2022:
            url = f"https://matokeo.necta.go.tz/acsee{year}/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/{exam_type}/results/{school_number}.htm"
    elif exam_type == 'csee':
        if int(year) == 2021:
            url = f"https://onlinesys.necta.go.tz/results/2021/csee/results/{school_number}.htm"
        elif int(year) > 2014:
            url = f"https://onlinesys.necta.go.tz/results/{year}/{exam_type}/results/{school_number}.htm"
        else:
            url = f"https://onlinesys.necta.go.tz/results/{year}/{exam_type}/{school_number}.htm"

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    summary = {
        "school_name": "*",
        "school_number": school_number,
        "exam_type": exam_type,
        "year_of_exam": year,
        "school_category": "*",
        "number_of_students": "*",
        "school_region": "*",
        "male_students": "*",
        "female_students": "*",
        "absentees": "*",
        "division_one": "*",
        "division_two": "*",
        "division_three": "*",
        "division_four": "*",
        "division_zero": "*",
        "national_position": "*",
        "regional_position": "*",
        "total_national_schools": "*",
        "total_regional_schools": "*",
        "gpa": "*"
    }

    if data.status_code == 200:
        name = ""
        for n in soup.find_all('h3')[0].text.split(' ')[1:]:
            if '\n' in n:
                n = n.split('\r')[0]
                n = n.split('\n')[0]
                name = f"{name} {n}"
                break
            name = f"{name} {n}"

        summary['school_name'] = name.strip()
        summary = set_zero(summary)

        if school_number.startswith("p"):
            summary = handle_center(summary, soup)
        else:
            summary = handle_school(summary, soup)
    else:
        raise Exception(f"Failed to access {url}\nResponse Code {data.status_code}")

    return summary


def set_zero(summary):
    summary["division_one"] = 0
    summary["division_two"] = 0
    summary["division_three"] = 0
    summary["division_four"] = 0
    summary["division_zero"] = 0

    summary["female_students"] = 0
    summary["male_students"] = 0
    summary["number_of_students"] = 0
    return summary


def handle_center(summary, soup):
    year = int(summary['year_of_exam'])
    exam_type = summary['exam_type'].lower()

    if exam_type == 'acsee':
        if year > 2019:
            summary = manual_scrap(soup, summary, 2)
            summary = set_zero(summary)
            summary = top_scrap(soup, summary)
        else:
            summary = manual_scrap(soup, summary, 0)

    elif exam_type == 'csee':
        if year > 2018:
            summary = manual_scrap(soup, summary, 2)
            summary = set_zero(summary)
            summary = top_scrap(soup, summary)

        else:
            summary = manual_scrap(soup, summary, 0)

    else:
        raise Exception(f'Invalid exam type {exam_type}')

    summary["number_of_students"] = summary["female_students"] + summary["male_students"]
    return summary


def handle_school(summary, soup):
    year = int(summary["year_of_exam"])
    exam_type = summary["exam_type"].lower()

    if exam_type == "acsee":
        if year > 2019:
            summary = manual_scrap(soup, summary, 2)
            summary = set_zero(summary)
            summary = top_scrap(soup, summary)
            summary = bottom_scrap(soup, summary, 4)
        else:
            summary = manual_scrap(soup, summary, 0)
            summary = bottom_scrap(soup, summary, 2)

    elif exam_type == "csee":
        if year > 2018:
            summary = manual_scrap(soup, summary, 2)
            summary = set_zero(summary)
            summary = top_scrap(soup, summary)
            summary = bottom_scrap(soup, summary, 4)
        else:
            summary = manual_scrap(soup, summary, 0)
            summary = bottom_scrap(soup, summary, 2)

    else:
        raise Exception(f"Invalid Exam Type {exam_type}")

    return summary


def manual_scrap(soup, summary, index):
    tables = soup.find_all('table')
    for tr in tables[index].find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            row.append(td.text.strip('\n'))

        if row[1].lower() == "f":
            summary["female_students"] += 1
        else:
            summary["male_students"] += 1

        if row[3] == "I" or "DISTINCTION" in row[3]:
            summary["division_one"] += 1
        elif row[3] == "II" or "MERIT" in row[3]:
            summary["division_two"] += 1
        elif row[3] == "III" or "CREDIT" in row[3]:
            summary["division_three"] += 1
        elif row[3] == "IV" or "PASS" in row[3]:
            summary["division_four"] += 1
        elif row[3] == "0" or "FAIL" in row[3]:
            summary["division_zero"] += 1
        elif "ABS" in row[3]:
            summary["absentees"] += 1

    return summary


def top_scrap(soup, summary):
    tables = soup.find_all('table')
    rows = []

    for tr in tables[0].find_all('tr'):
        r = []
        for td in tr.find_all('td'):
            r.append(td.text.strip('\n'))
        rows.append(r)

    summary["division_one"] = int(rows[3][1].strip())
    summary["division_two"] = int(rows[3][2].strip())
    summary["division_three"] = int(rows[3][3].strip())
    summary["division_four"] = int(rows[3][4].strip())
    summary["division_zero"] = int(rows[3][5].strip())

    for i in range(1, 6):
        summary["female_students"] += int(rows[1][i])
        summary["male_students"] += int(rows[2][i])

    return summary


def bottom_scrap(soup, summary, index):
    tables = soup.find_all('table')
    tds = tables[index].find_all('td')
    for i in range(0, int(len(tds) / 2)):
        if "NATIONWIDE" in tds[2 * i].text or "NATIONWISE" in tds[2 * i].text:
            position = tds[2 * i + 1].text.strip().split('/')
            summary["national_position"] = position[0]
            summary["total_national_schools"] = position[1]
        elif "REGIONWIDE" in tds[2 * i].text or "REGIONWISE" in tds[2 * i].text:
            position = tds[2 * i + 1].text.strip().split('/')
            summary["regional_position"] = position[0]
            summary["total_regional_schools"] = position[1]
        elif "GPA" in tds[2 * i].text:
            summary["gpa"] = tds[2 * i + 1].text.strip()
        elif "CATEGORY" in tds[2 * i].text:
            summary["school_category"] = tds[2 * i + 1].text.strip()
        elif "TOTAL" in tds[2 * i].text:
            summary["number_of_students"] = tds[2 * i + 1].text.strip()
        elif "REGION" in tds[2 * i].text:
            summary["school_region"] = tds[2 * i + 1].text.strip()
    return summary
