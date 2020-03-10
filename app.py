# importing libraries
# env FLASK_APP=app.py flask run
import numpy as np
import pandas as pd
import flask
import joblib
from flask import Flask, render_template, request

# creating instance of the class
app = Flask(__name__)


# to tell flask what url should trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", template="main.html")
    # return flask.render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        user_input = request.form.to_dict()
        prediction = predict_value(user_input).astype(int)

        df = pd.read_csv('data/tln_clean_data.csv', na_values='-')

        district_mean = round(df[df['district'] == user_input['district']]['price'].mean())
        district_median = round(df[df['district'] == user_input['district']]['price'].median())
        tln_mean = round(df['price'].mean())
        tln_median = round(df['price'].median())

        content = {
            'prediction': prediction,
            'district': user_input['district'],
            'district_mean': district_mean,
            'district_median': district_median,
            'tln_mean': tln_mean,
            'tln_median': tln_median
        }

        return render_template("index.html", template="result.html", content=content)


def predict_value(user_input):
    X_columns = ['district', 'rooms', 'area', 'material',
                 'condition', 'year_built', 'total_floors']
    d = pd.DataFrame(0, index=[0], columns=X_columns)

    d['area'] = user_input['area']
    d['rooms'] = user_input['rooms']
    d['year_built'] = user_input['year_built']
    d['district'] = user_input['district']
    d['material'] = user_input['material']
    d['condition'] = user_input['condition']
    d['total_floors'] = user_input['total_floors']

    model = joblib.load("tln_house_model.pkl")
    prediction = model.predict(d)

    return prediction[0]
