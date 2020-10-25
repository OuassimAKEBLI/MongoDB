from Second_Q_City import Lille_up as Lille
from pymongo import MongoClient
from pprint import pprint
from math import sin, cos, sqrt, atan2, radians
import folium


# get the user data
def log_lat_me():
    # normally i would add a try catch to verify if it is a float/int or a string but i focused of the main
    # functionality of the software
    lat = float(input("latitude : "))
    log = float(input("longitude : "))
    how_many_station = int(input('how many stations do you want to show :'))
    return [lat, log, how_many_station]


# get the user data businnes program
def log_lat():
    # normally i would add a try catch to verify if it is a float/int or a string but i focused of the main
    # functionality of the software
    lat = float(input("latitude : "))
    log = float(input("longitude : "))
    return [lat, log]


def update():
    Lille.execute()


# get all stations long and lat data
def stations_cord_data():
    atlas = MongoClient(
        'mongodb+srv://main:19631963@gettingstarted.nhut8.gcp.mongodb.net/vlille?retryWrites=true&w=majori'
        'ty')

    db = atlas.lille_bicycle
    my_collection = db['datas']
    cursor = my_collection.find({})

    data_col = []

    for document in cursor:
        data_col.append(document)

    return data_col


def calculate_distance(uu_lat, uu_log, s_lat, s_log):
    r = 6373.0

    u__lat = radians(uu_lat)
    u__log = radians(uu_log)
    s_lat = radians(s_lat)
    s_log = radians(s_log)

    d_lon = u__log - s_log
    d_lat = u__lat - s_lat
    a = sin(d_lat / 2) ** 2 + cos(s_lat) * cos(u__lat) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c

    return distance


def trace_map(u_l_lat, u_l_log, nb_station, station_name, s_lat, s_log):

    m = folium.Map(location=[u_l_lat, u_l_log], zoom_start=16)

    # add user position to map
    folium.Marker([u_l_lat, u_l_log], popup='<strong>User Position</strong>',
                  icon=folium.Icon(color='red', icon='cloud')).add_to(m)

    # add all the stations that the user asked for
    for pos in range(nb_station):
        folium.Marker([s_lat[pos], s_log[pos]], popup='<strong>' + str(station_name[pos]) + '</strong>',
                      icon=folium.Icon(color='green')).add_to(m)

    # save results
    m.save('Near_Stations.html')


# this function is going to be used in the fourth program
def execute(nb_h_m_s):
    print("done update")

    # get the coordination of the user & how many stations he want to show

    cord = log_lat()
    u_lat = cord[0]
    u_log = cord[1]
    nb_stations = nb_h_m_s

    # get data from datastore
    info = stations_cord_data()

    # stock the needed data you need to show in a new list
    stock_info_user = [
        {
            'name': ind.get('name'),
            'available_bike': ind.get('bike_availbale'),
            'stand_available': ind.get('stand_availbale'),
            'Cord': ind.get('Cord').get('coordinates'),
            'distance': calculate_distance(u_lat, u_log, ind.get('Cord').get('coordinates')[1],
                                           ind.get('Cord').get('coordinates')[0])
        }
        for ind in info
    ]

    # sort by distance
    result = sorted(stock_info_user, key=lambda x: float(x['distance']))

    # show results depends on the user choice
    # pprint(list(result[i] for i in range(nb_stations)))

    # or more clearer & pretty
    for i in range(nb_stations):
        print("\n-------------------------\n")
        print("name : ", result[i].get('name'), "\nbike available : ", result[i].get('available_bike'))
        print("stand available : ", result[i].get('stand_available'), "\ndistance : ", result[i].get('distance'))
    print("\n-------------------------\n")

    # and even more amazing and pretty check the project files and open Near_Stations.html
    lat_t = []
    log_g = []
    na_me = []

    for elem in result:
        cord_lat = float(elem.get('Cord')[1])
        cord_log = float(elem.get('Cord')[0])
        name = str(elem.get('name'))
        lat_t.append(cord_lat)
        log_g.append(cord_log)
        na_me.append(name)

    trace_map(u_lat, u_log, nb_stations, na_me, lat_t, log_g)

    return result


def execute_me():
    # update the datastore
    update()
    print("done update")

    # get the coordination of the user & how many stations he want to show

    cord = log_lat_me()
    u_lat = cord[0]
    u_log = cord[1]
    nb_stations = cord[2]

    # get data from datastore
    info = stations_cord_data()

    # stock the needed data you need to show in a new list
    stock_info_user = [
        {
            'name': ind.get('name'),
            'available_bike': ind.get('bike_availbale'),
            'stand_available': ind.get('stand_availbale'),
            'Cord': ind.get('Cord').get('coordinates'),
            'distance': calculate_distance(u_lat, u_log, ind.get('Cord').get('coordinates')[1],
                                           ind.get('Cord').get('coordinates')[0])
        }
        for ind in info
    ]

    # sort by distance
    result = sorted(stock_info_user, key=lambda x: float(x['distance']))

    # show results depends on the user choice
    # pprint(list(result[i] for i in range(nb_stations)))

    # or more clearer & pretty
    for i in range(nb_stations):
        print("\n-------------------------\n")
        print("name : ", result[i].get('name'), "\nbike available : ", result[i].get('available_bike'))
        print("stand available : ", result[i].get('stand_available'), "\ndistance : ", result[i].get('distance'))
    print("\n-------------------------\n")

    # and even more amazing and pretty check the project files and open Near_Stations.html
    lat_t = []
    log_g = []
    na_me = []

    for elem in result:
        cord_lat = float(elem.get('Cord')[1])
        cord_log = float(elem.get('Cord')[0])
        name = str(elem.get('name'))
        lat_t.append(cord_lat)
        log_g.append(cord_log)
        na_me.append(name)

    trace_map(u_lat, u_log, nb_stations, na_me, lat_t, log_g)


if __name__ == '__main__':
    execute_me()
