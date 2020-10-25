from pymongo import MongoClient
from pprint import pprint
import sys
from Second_Q_City import Lille_up as Lille
from Third_Q_City import lille_stations_location as Results
import datetime


# present a menu to the user
def menu():
    print("1) Find station\n2) Update station\n3) Delete station\n"
          "4) Deactivate station\n5) Give all stations with ratio bike\n6) Update\n7) Quit")
    print("\n----------------------------------")
    us_choice = int(input("chose from the menu : "))
    print("\n----------------------------------")
    return us_choice


# ask for the station name
def sub_menu():
    return str(input("Name of the station : "))


# ask the user to make a choice
def choice(user_choice, name):
    if user_choice == 1:
        find_station(name)
    elif user_choice == 2:
        update_station(name)
    elif user_choice == 3:
        delete_station(name)
    elif user_choice == 4:
        deactivate_station()
    elif user_choice == 5:
        ratio()
    elif user_choice == 6:
        update()
    elif user_choice == 7:
        return sys.exit(0)


# get information from the user about the update
def get_info():
    print("-----------------------------------------------------------------")
    print("\nplease select a new values to update the data\n")
    na_station = str(input("Name of the station : ")).upper()
    bi_available = int(input("Bike available : "))
    st_available = int(input("Stand available : "))
    latitude = float(input("latitude : "))
    longitude = float(input("longitude : "))
    date = str(input("date : "))
    print("-----------------------------------------------------------------\n")
    return [na_station, bi_available, st_available, latitude, longitude, date]


# update a station informations
def update_station(name):
    get_station = find_station(name=name)
    if get_station is None:
        print("------------------------------------------")
        print("\nvalue not found\n")
        print("------------------------------------------")
    else:
        info = get_info()
        atlas = MongoClient(
            'mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
            'ty')

        db = atlas.lille_bicycle
        my_collection = db['datas']

        my_collection.update_one({
            '_id': get_station.get('_id')
        }, {
            '$set': {
                "name": info[0],
                "bike_availbale": info[1],
                "stand_availbale": info[2],
                "Cord": {'coordinates': [info[4], info[3]], 'type': 'Point'},
                "date": info[5]
            }
        })


# delete a station from the collection
def delete_station(name):
    get_station = find_station(name=name)
    if get_station is None:
        print("------------------------------------------")
        print("\nvalue not found\n")
        print("------------------------------------------")
    else:
        atlas = MongoClient(
            'mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
            'ty')

        db = atlas.lille_bicycle
        my_collection = db['datas']
        my_collection.delete_one({'_id': get_station.get('_id')})


# deactivate the number of stations close to lat and log that we chose
def deactivate_station():
    nb_deactivate = int(input("how many station to deactivate : "))
    res = Results.execute(nb_h_m_s=nb_deactivate)
    test_name = ""
    for i in range(nb_deactivate):
        test_name = res[i].get('name')
        delete_station(res[i].get('name'))

    # test if the last element was delete or not
    find_station(test_name)


# find a station using name
def find_station(name):
    atlas = MongoClient(
        'mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
        'ty')

    db = atlas.lille_bicycle
    my_collection = db['datas']
    cursor = my_collection.find_one({'name': {"$regex": ".*"+str(name).upper()+".*"}})
    print("\n---------------- results ------------------")
    pprint(cursor)
    print("\n---------------- results ------------------")
    return cursor


# update the collection to get the new values / delete old collection and replace it with up to date new collection
def update():
    Lille.execute()


# get the documents that their ratio under 20% between 18/19 and between Monday/Friday
def ratio():
    test_day = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
    results = []
    atlas = MongoClient(
        'mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
        'ty')

    db = atlas.lille_bicycle
    my_collection = db['datas']
    save = my_collection.find({})
    for elem in save:
        d_ate = (elem.get('date')).strftime("%A")
        hour_test = (elem.get('date')).hour
        ratio = 0
        if elem.get('stand_availbale') == 0:
            ratio = 100
        else:
            ratio = (elem.get('bike_availbale') / elem.get('stand_availbale'))*100
        if d_ate.upper() in test_day:
            if 18 <= hour_test <= 19:
                if ratio < 20:
                    results.append(elem)

    pprint(results)
    return results


# ou main function
if __name__ == '__main__':
    while True:
        use_choice = menu()
        name_station = sub_menu()
        choice(user_choice=use_choice, name=name_station)
