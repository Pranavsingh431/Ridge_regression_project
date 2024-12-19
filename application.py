import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler
import pickle

application = Flask(__name__)
app = application

ridge = pickle.load(open('models/ridge.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))
model = ridge['model']
r2_score_model = ridge['r2']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == "POST":
        Temperature = float(request.form.get("Temperature"))
        RH = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        DC = float(request.form.get('DC'))
        ISI = float(request.form.get('ISI'))
        BUI = float(request.form.get('BUI'))       
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))
        
        scaled_data = scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,DC,ISI,BUI,Classes,Region]])
        result = model.predict(scaled_data)[0]
        
        return render_template('predict.html', result = f"{result}, Accuracy: {r2_score_model*100}")
    else:
        return render_template('predict.html')

 
if __name__ == '__main__':
    app.run(debug=True)