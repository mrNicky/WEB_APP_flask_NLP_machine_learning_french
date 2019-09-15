from flask import Flask, render_template, url_for, request
import os
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000)) #To deploy in Heroku
from ML_models import *
import sqlite3 as sql

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

@app.route('/add', methods=['POST', 'GET'])
def add():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * from tweets_list")
    rows = cur.fetchall();
    return render_template("add.html", rows=rows)

@app.route('/added', methods=['POST', 'GET'])
def added():
    if request.method == 'POST':
        try:
            label = request.form['label']
            tweet = request.form['tweet']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tweets_list (label, tweet) \
                VALUES (?,?)",(label, tweet))
                con.commit()
                msg = "Nous venons d'ajouter vos données"
        except:
            con.rollback()
            msg = "Une erreur est survenue"
        finally:
             print("ajout ok")
             return render_template("index.html", msg=msg)
             con.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
