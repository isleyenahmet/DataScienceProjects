from flask import Flask, render_template, request
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Veri setini yükle ve modeli oluştur
data = pd.read_csv('tips_data.csv')
features = ['total_bill', 'sex', 'smoker', 'time', 'size', 'day_Sat', 'day_Sun', 'day_Thur']
target = 'tip'

X = data[features]
y = data[target]

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total_bill = float(request.form['total_bill'])
        sex = int(request.form['sex'])
        smoker = int(request.form['smoker'])
        time = int(request.form['time'])
        size = int(request.form['size'])
        day = request.form['day']
        
        day_Sat = 1 if day == 'Cumartesi' else 0
        day_Sun = 1 if day == 'Pazar' else 0
        day_Thur = 1 if day == 'Perşembe' else 0
        
        tahmin = model.predict([[total_bill, sex, smoker, time, size, day_Sat, day_Sun, day_Thur]])[0]
        tahmin = round(tahmin, 2)
        yuzde = round((tahmin / total_bill) * 100, 2)
        
        return render_template('index.html', tahmin=tahmin, yuzde=yuzde, total_bill=total_bill)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)