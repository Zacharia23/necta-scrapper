from unicodedata import name
from flask import render_template, redirect, url_for
from app import app
import datetime

@app.route("/<name>")
def home(name):
    year = getYear()
    return render_template('index.html', year = year)

def getYear():
    current_date = datetime.datetime.now()
    date = current_date.date()
    return date.strftime("%Y")