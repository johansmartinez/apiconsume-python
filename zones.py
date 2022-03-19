import json
from geopy.distance import geodesic


DEFAULT_DISTANCE=0.002646001349619869

data=[]
with open('./2014.geojson') as json_file:
    file = json.load(json_file)
    data= file['features']

#sacar la longitud y latitud determinar las zonas
def determinateZones():
    temp=data
    zones=[]
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
        print('VOY en el ',data.index(current)," quedán ", len(data))
        #------
        with open("pintar.json","a") as archivo:
            json.dump(parseZone(zone_current),archivo)
        #-----
        temp.remove(current)
        zones.append(zone_current)
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

zone1=[]
with open('./test.json') as json_file:
    file = json.load(json_file)
    zone1= file

def calculateCentroid(zone):
    length = len(zone)
    sumLat=0
    sumLon=0
    for point in zone:
        sumLat+= point['lat']
        sumLon+= point['lon']
    return  {'lon':sumLon/length , 'lat':sumLat/length}

def calculateRadius(centroid, zone):
    maxDistance=0
    centroidCordinate=(centroid['lon'], centroid['lat'])
    for x in zone:
        xCordinate=((x['lon'], x['lat']))
        distance = geodesic(xCordinate, centroidCordinate).miles
        if distance> maxDistance:
            maxDistance=distance
    return (DEFAULT_DISTANCE,maxDistance) [maxDistance==0]

def parseZone(zone):
    centroid= calculateCentroid(zone)
    radius= calculateRadius(centroid, zone)
    riskTotal=calculateRisk(zone)
    return {'centroid':centroid, 'radius': radius, 'riskTotal':riskTotal, 'numberPoints': len(zone)}

#print(parseZone(zone1))
determinateZones()