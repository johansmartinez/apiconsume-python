from .connectiondb import generateConnection
from bson.json_util import dumps

def getData (filter,url,database,collection):
    db=generateConnection(url,database,collection)
    l = list(db.find(filter))
    return dumps(l)

def getDataShow(filter,show,url,database,collection):
    db=generateConnection(url,database,collection)
    l = list(db.find(filter,show))
    return dumps(l)