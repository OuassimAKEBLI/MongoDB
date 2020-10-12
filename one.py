import pymongo
import pprint


client = pymongo.MongoClient("mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majority")
db = client.get_database('vlille')

# get records
collection = db.myData

# get test
result1 = collection.find({'records.fields.commune': {'$eq': 'LILLE'}},
                          {'records.fields.commune':1, 'records.geo': 1, 'records.fields.nom': 1,
                           'records.fields.type': 1, 'records.fieldsetat': 1})


pprint.pprint(list(result1))


# get bicycle stations Lille, Lyon, Paris, Rennes
