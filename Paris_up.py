import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser


atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majority')


db = atlas.paris_bicycle

db.datas.create_index([('station_id', 1),('date', -1)], unique=True)


def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows" \
          "=251&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_station_id(id_ext):

    tps = db.stations.find_one({'source.id_ext': id_ext}, {'_id': 1})
    print(list(tps))
    return tps['_id']


pprint(get_vparis())

while True:
    print('update')
    vparis = get_vparis()
    datas = [
        {
            "bike_availbale": elem.get('fields', {}).get('numbikesavailable'),
            "stand_availbale": elem.get('fields', {}).get('numdocksavailable'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('duedate')),
            "station_id": get_station_id(elem.get('fields', {}).get('stationcode'))
        }
        for elem in vparis
    ]

    try:
        db.datas.insert_many(datas, ordered=False)
    except:
        pass

    time.sleep(10)
