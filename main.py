from flask_pymongo import PyMongo
import flask
from flask import Flask,jsonify,request
from flask_restful import Api,Resource
 

app=Flask(__name__)
api=Api(app)
 
def db_connection(app):
    mongodb_client = PyMongo(app, uri="mongodb://0.0.0.0:27017/capturedMetric")
    db = mongodb_client.db
 
    app.config["MONGO_URI"] = "mongodb://0.0.0.0:27017/capturedMetric"
    mongodb_client = PyMongo(app)
    db = mongodb_client.db
    return db
 
db=db_connection(app)
class capturedMetric(Resource):   # Use to Rececive Captured Data From Binge App
    def post(self):
         #db=db_connection(app)
         data=request.get_json()
         db.CapturedBecons.insert_one(data)
         return jsonify(
             {"Status Code":200})
    def get(self):
          return jsonify({"db_data":str(list(db.CapturedBecons.find()))})
 
class probeConfiguration(Resource): #Use to Send Probe Config Parameters to the Binge App
    def get(self):
        return jsonify(
            {
                "ServerURL": "ec2-52-204-122-132.compute-1.amazonaws.com",
                "frequencyOfCapturingInSeconds": 5,
                "timestamp": 1632297600,
                "frequencyOfTransmissionInSeconds": 15,
                "status":{
                "videoQuality":"on",
                "stallCount":"off"
                },
                "threshold":{
                "videoQuality":"10",
                "stallCount":"5"}
            }
            )

if __name__=="__main__":
    api.add_resource(probeConfiguration,"/probe")
    api.add_resource(capturedMetric,"/capture")
    app.run(host="0.0.0.0",port=8080,debug=True)
