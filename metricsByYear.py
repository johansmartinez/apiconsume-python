import sys
import requests
import sys

def getMetricsByYear(year,url):

    response=requests.get(url)
    a=response.json()

    data={
        'year':year,
        'url': url,
        'total':len(a['features']),
        'tipos_accidente':{},
        'meses':{},
        'neighborhood':{},
        'days':{},
        'risks':{}
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
        generateTotal('neighborhood',element['properties']['BARRIO'])
        generateTotal('days',element['properties']['DIA_NOMBRE'])
        generateTotal('risks',element['properties']['GRAVEDAD'])

    return data

sys.modules[__name__]=getMetricsByYear