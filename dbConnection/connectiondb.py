import pymongo

def generateConnection(url,database,collection):
    client = pymongo.MongoClient(url)
    db=client[database]
    return db[collection]
