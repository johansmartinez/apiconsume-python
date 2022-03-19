import json
from geopy.distance import geodesic
from dbConnection.saveData import saveMultiData

DEFAULT_DISTANCE=0.310686 # 500m

data=[]
with open('./2014.geojson') as json_file:
    file = json.load(json_file)
    data= file['features']

f = open("demofile.json", "w")
f.write(json.dumps(data, ensure_ascii=False))
f.close()


#sacar la longitud y latitud determinar las zonas
def determinateZones():
    temp=data
    zones=[]
    cont=0
    for current in data :
        zone_current=[]
        for x in data:
            coordinates=(x['properties']['LONGITUD'], x['properties']['LATITUD'])
            coordinates_current_position=(current['properties']['LONGITUD'], current['properties']['LATITUD'])
            distance = geodesic(coordinates, coordinates_current_position).miles
            if((distance < DEFAULT_DISTANCE ) and (current!=x)):
                zone_current.append({'lon':x['properties']['LONGITUD'],'lat': x['properties']['LATITUD'], 'riesgo':x['properties']['GRAVEDAD']})
                temp.remove(x)
        zone_current.append({'lon':current['properties']['LONGITUD'],'lat': current['properties']['LATITUD'], 'riesgo':current['properties']['GRAVEDAD']})
        print('VOY en el ',cont," quedán ", len(data))
        cont+=1
        temp.remove(current)
        result=parseZone(zone_current)
        if result!=None:
            zones.append(result)
    return zones

def scoreRisk(x):
    if(x['riesgo'] == "SOLO DAÑOS"):
        return 1
    elif(x['riesgo'] == "HERIDO"):
        return 3
    elif(x['riesgo'] == "MUERTO"):   
        return 5

def calculateRisk(zone):
    total= 0
    for x in zone:
        total+=scoreRisk(x)
    return total


def calculateCentroid(zone):
    length = len(zone)
    sumLat=0
    sumLon=0
    for point in zone:
        try:
            sumLat+= point['lat']
            sumLon+= point['lon']
        except:
            return None
    return  {'lon':sumLon/length , 'lat':sumLat/length}


def calculateRadius(centroid, zone):
    maxDistance=0
    centroidCordinate=(centroid['lon'], centroid['lat'])
    for x in zone:
        xCordinate=((x['lon'], x['lat']))
        distance = geodesic(xCordinate, centroidCordinate).miles
        if distance> maxDistance:
            maxDistance=distance
    if (maxDistance == 0):
        return DEFAULT_DISTANCE
    else:
        return maxDistance

def parseZone(zone):
    centroid= calculateCentroid(zone)
    if centroid!=None:
        radius= calculateRadius(centroid, zone)
        riskTotal=calculateRisk(zone)
        return {'centroid':centroid, 'radius': radius, 'riskTotal':riskTotal, 'numberPoints': len(zone)}
    else: 
        return None

#print(parseZone(zone1))

url=""
with open('./keys/key.json') as json_file:
    config = json.load(json_file)
    url=config['urldb']

saveMultiData(determinateZones(),url,'trinskapp','zones')