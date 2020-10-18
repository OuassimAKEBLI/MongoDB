import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser


atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retry'
                    'Writes=true&w=majority')


db = atlas.rennes_bicycle

db.datas.create_index([('station_id', 1),('date', -1)], unique=True)


def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps" \
          "-reel&q=&rows=251&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles" \
          "&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_station_id(id_ext):
    tps = db.stations.find_one({ 'source.id_ext': id_ext }, { '_id': 1 })
    return tps['_id']


pprint(get_vrennes())


while True:
    print('update')
    vrennes = get_vrennes()
    datas = [
        {
            "bike_availbale": elem.get('fields', {}).get('nombrevelosdisponibles', '999'),
            "stand_availbale": elem.get('fields', {}).get('nombreemplacementsdisponibles', '999'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('lastupdate', '999')),
            "station_id": get_station_id(elem.get('fields', {}).get('idstation', '999'))
        }
        for elem in vrennes
    ]

    try:
        db.datas.insert_many(datas, ordered=False)
    except:
        pass

    time.sleep(10)
