import json

from metrics.metricsByYear import getMetricsYears
from dbConnection.saveData import saveMultiData
from dbConnection.getData import getData

url=""
with open('./keys/key.json') as json_file:
    config = json.load(json_file)
    url=config['urldb']

#saveMultiData(getMetricsYears('./config.json'),url,'trinskapp','metrics')

print(getData({},url,'trinskapp','metrics'))