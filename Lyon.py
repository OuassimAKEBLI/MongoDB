import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_vlyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=250&facet" \
          "=name&facet=commune&facet=bonus&facet=status&facet=available&facet=availabl_1&facet=availabili&facet=" \
          "availabi_1&facet=last_upd_1"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


v_lyon = get_vlyon()


v_lyon_to_insert = [
    {
        'name': elem.get('fields', {}).get('name', '').title(),
        'geometry': elem.get('fields', {}).get('geo_shape'),
        'size': elem.get('fields', {}).get('bike_stand'),
        'source': {
            'dataset': 'Lyon',
            'id_ext': elem.get('fields', {}).get('gid')
        },
        'tpe': elem.get('fields', {}).get('banking', '') == 't'
    }
    for elem in v_lyon
]


atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
                    'ty')

db = atlas.lyon_bicycle

# db.stations.insert_many(vlilles_to_insert)

for ve_lyon in v_lyon_to_insert:
    db.stations.insert_one(ve_lyon)