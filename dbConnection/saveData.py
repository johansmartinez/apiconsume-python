import json
from .connectiondb import generateConnection

def saveMultiData(data , url, db, collection):
    db=generateConnection(url,db,collection)
    db.insert_many(json.loads(str(json.dumps(data, ensure_ascii=False))))

def saveOneData(data , url, db, collection):
    db=generateConnection(url,db,collection)
    db.insert_one(json.loads(str(json.dumps(data, ensure_ascii=False))))