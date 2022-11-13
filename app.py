from flask import Flask, request, render_template
from flask_cors import cross_origin
from summary import summary
from schools import schools
from student import student
from students import students

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results', methods=['GET', 'POST'])
@cross_origin()
def results():
    if request.method == 'POST':
        search_type = request.form['search']
        year = request.form['School_Year']
        exam_type = request.form['Exam_Type']
        school_number = request.form['School_Number']
        student_number = request.form['Student_Number']

    if search_type == 'Summary':
        out_results = summary(year, exam_type, school_number)
    elif search_type == 'Schools':
        out_results = schools(year, exam_type)
    elif search_type == 'Student':
        out_results = student(year, exam_type, school_number, student_number)
    elif search_type == 'Students':
        out_results = students(year, exam_type, school_number)

    return render_template('home.html', res=out_results)


if __name__ == '__main__':
    app.run()
