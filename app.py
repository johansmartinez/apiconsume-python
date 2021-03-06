import json
from flask import Flask,jsonify
from flask_cors import CORS

from dbConnection.getData import getDataShow, getData

app=Flask(__name__)
CORS(app)

url=""
with open('./keys/key.json') as json_file:
    config = json.load(json_file)
    url=config['urldb']

@app.route('/')
def index():
    return "welcome"

@app.route('/metrics',methods=['GET'])
def getMetrics():
    return jsonify(getDataShow({}, {'_id': False},url,'trinskapp','metrics'))

@app.route('/zones',methods=['GET'])
def getMZones():
    return jsonify(getData({},url,'trinskapp','zones'))

if __name__=="__main__":
    app.run(debug=True)