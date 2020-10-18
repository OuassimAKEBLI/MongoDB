import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps" \
          "-reel&q=&rows=251&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles" \
          "&facet=nombrevelosdisponibles"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


v_rennes = get_vrennes()


v_rennes_to_insert = [
    {
        'name': elem.get('fields', {}).get('nom', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
        'source': {
            'dataset': 'Rennes',
            'id_ext': elem.get('fields', {}).get('idstation')
        },
        'tpe': elem.get('fields', {}).get('etat', '') == 'En fonctionnement' # pas de TPE je vais le remplacer par l'état
    }
    for elem in v_rennes
]

atlas = MongoClient('mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
                    'ty')

db = atlas.rennes_bicycle


for ve_rennes in v_rennes_to_insert:
    db.stations.insert_one(ve_rennes)