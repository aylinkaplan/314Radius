from flask import Flask, request, make_response, render_template
import csv
import json
import io
import codecs
import random
from datetime import datetime


application = app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/form-list')
def form_list():
    return render_template('list_page.html')


@app.route('/form-csv')
def form():
    return render_template('csv_page.html')


@app.route('/form-json')
def form_json():
    return render_template('json_page.html')


@app.route('/list', methods=["POST"])
def update_list():
    params = request.data
    if params:
        params_list = json.loads(params)
    elif not params and request.form['params']:
        params = request.form['params']
        params_list = params.split(',')
    else:
        params_list = ""
    params_str = " | ".join(params_list)
    return params_str


@app.route('/csv', methods=["POST"])
def update_csv():
    flask_file = request.files['data_file']
    if not flask_file:
        return "Not available file"
    if flask_file.content_type != 'text/csv':
        return "File is not CSV format"

    result = [['number 1', 'number 2', 'answer']]
    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            values = row[0].split(';')
            multiply = 1
            for val in values:
                multiply *= int(val)
            values.append(str(multiply))
            result.append(values)

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerows(result)
    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    response.headers["Content-type"] = "text/csv"

    return response


def generate_password(user_info):
    password = ''
    user_list = []
    for info in user_info:
        info = info.replace(" ", "")
        user_list += info.split('-')

    while len(password) <= 6:
        password += random.choice(user_list)
    created_at = datetime.now()
    return password, created_at


@app.route('/json', methods=["POST"])
def update_json():
    json_data = request.get_json()
    if not json_data and request.form['params']:
        try:
            json_data = json.loads(request.form['params'])
        except:
            return "Wrong Parameter Type"
    if json_data:
        user_info = list(json_data.values())
        password, created_at = generate_password(user_info)
        json_data['password'] = password
        json_data['created_at'] = created_at
        return json_data
    else:
        return "ANY PARAMETERS"


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080, debug=True)
