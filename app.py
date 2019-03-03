from flask import Flask, jsonify,request,session
from sklearn.externals import joblib
import pandas as pd
import json

import numpy as np
import os.path


app = Flask(__name__)

@app.route('/predict_ml', methods=['POST'])
def predict_ml():
     if request.method=='POST':
         data = request.data
         dataDict = json.loads(data)
         sex=dataDict["sex_name"]
         age=dataDict["age_name"]
         prediction = predict(sex,age)
         return jsonify({'prediction': prediction})

def predict(sex,age):
    # Load Model
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "model_risk.pkl")

    model_loaded = joblib.load(path)

    # Static Variables
    sex_female_flag=0
    sex_male_flag=1
    final_prediction = "SAFE"

    # Data Engineering
    if sex=="Female":
        sex_female_flag=1

    if sex=="Male":
        sex_male_flag=1

    df = pd.DataFrame({'AGE':age,'SEX_Female':sex_female_flag,'SEX_Male':sex_male_flag}, index=[0])
    query = pd.get_dummies(df)

    # Predict
    prediction = int(model_loaded.predict(query))

    # Labeling
    if prediction == 0:
        final_prediction == "RISKY"

    return final_prediction


if __name__ == '__main__':
     app.run(port=8080)
