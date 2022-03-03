import json
import metricsByYear
import json

D14=metricsByYear(2014, 'https://opendata.arcgis.com/datasets/505e89d2ade143a684d51b60236ba285_0.geojson')

f = open("{}.json".format(2014), "w")
f.write(json.dumps(D14, ensure_ascii=False))
f.close()