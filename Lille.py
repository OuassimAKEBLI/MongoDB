import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=" \
          "libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


v_lille = get_vlille()


v_lille_to_insert = [
    {
        'name': elem.get('fields', {}).get('nom', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
        'source': {
            'dataset': 'Lille',
            'id_ext': elem.get('fields', {}).get('libelle')
        },
        'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE'
    }
    for elem in v_lille
]


atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
                    'ty')

db = atlas.lille_bicycle

# db.stations.insert_many(vlilles_to_insert)

for ve_lille in v_lille_to_insert:
    db.stations.insert_one(ve_lille)