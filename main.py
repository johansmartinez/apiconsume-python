import json
import metricsByYear
import json


def writeFileData():
    with open('config.json') as json_file:
        config = json.load(json_file)
        for element in config:
            data=metricsByYear(element['year'], element['url'])
            f = open("dataset/{}.json".format(element['year']), "w")
            f.write(json.dumps(data, ensure_ascii=False))
            f.close()
            
writeFileData()