from flask import Flask, request
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './app')
from ML_models import *
import json


app = Flask(__name__)
api = Api(app)

class sentiment(Resource):
    def get(self, prediction):
        
       # p = run_model(prediction)       
       # return {p: "ss"}
       prediction = [request.form['data']]
       return run_model(prediction)
api.add_resource(sentiment, '/<string:prediction>')

if __name__ == '__main__':
    app.run(debug=True)


