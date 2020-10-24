import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser


atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majority')


db = atlas.lyon_bicycle

db.datas.create_index([('station_id', 1),('date', -1)], unique=True)


def get_vlyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=250&facet" \
          "=name&facet=commune&facet=bonus&facet=status&facet=available&facet=availabl_1&facet=availabili&facet=" \
          "availabi_1&facet=last_upd_1"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_station_id(id_ext):
    tps = db.stations.find_one({ 'source.id_ext': id_ext }, { '_id': 1 })
    return tps['_id']


while True:
    print('update')
    vlyon = get_vlyon()
    datas = [
        {
            "bike_availbale": elem.get('fields', {}).get('available'),
            "stand_availbale": elem.get('fields', {}).get('availabl_1'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('last_upd_1')),
            "station_id": get_station_id(elem.get('fields', {}).get('gid'))
        }
        for elem in vlyon
    ]

    try:
        db.datas.insert_many(datas, ordered=False)
    except:
        pass

    time.sleep(10)

