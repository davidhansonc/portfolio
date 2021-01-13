# -*- coding: utf-8 -*-
# @Author: davidhansonc
# @Date:   2021-01-12 14:41:13
# @Last Modified by:   davidhansonc
# @Last Modified time: 2021-01-13 11:02:19
from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/<string:page_name>')
def show_page(page_name=None):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thank_you.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong, try again.'

def write_to_file(new_data): 
    with open('database.txt', 'a') as database:
        email = new_data['email']
        subject = new_data['subject']
        message = new_data['message']
        file = database.write(f'{email},{subject},{message}\n')
    return file

def write_to_csv(new_data):
    with open('database.csv', 'a', newline='') as database:
        email = new_data['email']
        subject = new_data['subject']
        message = new_data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', \
                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])
    return csv_writer
