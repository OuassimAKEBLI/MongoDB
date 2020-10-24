import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows" \
          "=251&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


v_paris = get_vparis()

v_paris_to_insert = [
    {
        'name': elem.get('fields', {}).get('name', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('capacity'),
        'source': {
            'dataset': 'Paris',
            'id_ext': elem.get('fields', {}).get('stationcode')
        },
        'tpe': elem.get('fields', {}).get('is_renting', '') == 'OUI'
    }
    for elem in v_paris
]

atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
                    'ty')

db = atlas.paris_bicycle


for ve_paris in v_paris_to_insert:
    db.stations.insert_one(ve_paris)