from flask import Flask, render_template, url_for, request

app = Flask(__name__)

from ML_models import *

@app.route('/')
def home():
    user =  {'username': 'Zakaria'}
    return render_template('index.html', title='home', user=user)


@app.route('/predict', methods=['POST'])
def predict():
        
    #New predict value from models.py
    if request.method == 'POST':
        tweet = [request.form['message']]
        new_prediction = run_model(tweet)
    return render_template('result.html', prediction=new_prediction, message=tweet[0])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
