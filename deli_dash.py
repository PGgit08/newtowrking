import requests
import pprint
import sqlite3


class Map_API:
    def __init__(self, key):
        self.key = "&key=" + key
        self.nearby_places_info = {}

    def get_user_loc(self, address):
        # get user's latitude and longitude based on their address
        baseurl_for_getting_location = "https://maps.googleapis.com/maps/api/geocode/json"
        addr = "?address=" + address
        print(baseurl_for_getting_location + addr + self.key)
        loc_response = requests.get(baseurl_for_getting_location + addr + self.key).json()
        pprint.pprint(loc_response['results'][0]['geometry']['location'])
        return loc_response['results'][0]['geometry']['location']

    def get_nearby_places(self, user_location, mile_radius):
        # get radius
        meter_radius = mile_radius * 1609.34
        meter_radius = int(meter_radius)

        # location parameters
        location = "?location=" + str(user_location['lat']) + "," + str(user_location['lng'])
        radius = "&radius=" + str(meter_radius)

        # find nearby places using api
        baseurl_for_getting_nearby_places = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        nearby_places_url = baseurl_for_getting_nearby_places + location + radius + "&opennow" + self.key
        server_response = requests.get(nearby_places_url).json()['results']
        print(len(server_response))
        return server_response

    def sort_nearby_places_info(self, nearby_places_list):
        for place in nearby_places_list:
            self.nearby_places_info[place['place_id']] = {place['name']}


class Sql_Manager:
    def __init__(self, file_name):
        self.places_db = sqlite3.connect(file_name)
        self.places_cursor = self.places_db.cursor()
        self.places_cursor.execute("CREATE TABLE IF NOT EXISTS places(place_id, item, cost)")

    def add_new_row(self, col1, col2, col3):
        self.places_cursor.execute("INSERT INTO places(place_id, item, cost) VALUES(?, ?, ?)", (col1, col2, col3))
        self.places_db.commit()

    def read_table(self):
        self.places_cursor.execute("SELECT * FROM places")
        places_data = self.places_cursor.fetchall()
        return places_data

    def close_connections(self):
        self.places_cursor.close()
        self.places_db.close()


# API key for access
api_key = "AIzaSyDGb61LgcVHDtga1yeKrcPOvnVInCtr3ms"
map = Map_API(key=api_key)
# create database connection
db = Sql_Manager('places.db')
print(db.read_table())

# get user location based on their location
user_loc = map.get_user_loc(address="+155+North+Country+Club+Road, +Brevard, +NC")
nearby_places = map.get_nearby_places(user_loc, 1.5)
map.sort_nearby_places_info(nearby_places_list=nearby_places)
pprint.pprint(map.nearby_places_info)

# id_thing = input("id: ")
# db.add_new_row(col1=id_thing, col2="skittles", col3=1.25)
