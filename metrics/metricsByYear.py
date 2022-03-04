import requests
import json

def getMetricsByYear(year,url):

    response=requests.get(url)
    a=response.json()

    data={
        'year':year,
        'url': url,
        'total':len(a['features']),
        'tipos_accidente':{},
        'meses':{},
        'barrios':{},
        'dias':{},
        'riesgo':{}
    }

    def generateTotal(type,element):
        name=element
        dict=data[type]
        try:
            dict[name]+=1
        except:
            a_dict = {}
            for variable in ["name"]:
                a_dict[eval(variable)] = 0
            data[type] = {**dict, **a_dict}
            

    for element in a['features']:
        generateTotal('tipos_accidente',element['properties']['CLASE'])
        generateTotal('meses',element['properties']['MES'])
        generateTotal('barrios',element['properties']['BARRIO'])
        generateTotal('dias',element['properties']['DIA_NOMBRE'])
        generateTotal('riesgo',element['properties']['GRAVEDAD'])

    return data


def getMetricsYears(urlfile):
    dataset=[]
    with open(urlfile) as json_file:
        config = json.load(json_file)
        for element in config:
            data=getMetricsByYear(element['year'], element['url'])
            dataset.append(data)
    return dataset