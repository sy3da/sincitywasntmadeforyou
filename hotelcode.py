from yelpapi import YelpAPI
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

#Getting API Data and storing into List
def getYelpAPIData():
    api_key = '84yyM6N4wVI_D4s419Jt40ZzW33AUxXvmR1hHUfR4j97ce2WibAUber4MGGirF_e7RjyF0PEd_tJV6F-NfZmBM0Xakb5x3yFR8o_Eh-a81v-hDkq3dm-u-4KWfkuZHYx'
    cities = ['Las Vegas', 'Henderson', 'Reno', 'North Las Vegas', 'Sparks', 'Carson City', 'Fernley', 'Mesquite', 'Elko', 'Boulder City', 'Fallon', 'Winnemucca']
    client = YelpAPI(api_key)

    hotel_list = []

    for city in cities:
        # Yelp API parameters
        params = {
            'term': 'hotel',
            'location': city,
            'limit': 2
        }
        response = client.search_query(**params)

        for business in response['businesses']:
            name = business['name']
            rating = business['rating']
            price = business.get('price', None)
            hotel_list.append((name, city, rating, price))
        if not response['businesses']:
            print(f"No new hotels found in {city}")

    return hotel_list

#Setting up DB connection/opening database
def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# def make_yelp_table(data, cur, conn):
#     cur.execute("CREATE TABLE IF NOT EXISTS YelpData (hotel_name TEXT, city TEXT, rating INTEGER, cost TEXT)")
#     for record in data:
#         cur.execute("INSERT OR IGNORE INTO YelpData (hotel_name, city, rating, cost) VALUES (?, ?, ?, ?)", record)
#     conn.commit()
def make_yelp_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS YelpData (hotel_name TEXT, city TEXT, rating INTEGER, cost TEXT, UNIQUE(hotel_name, city))")
    for record in data:
        try:
            cur.execute("INSERT INTO YelpData (hotel_name, city, rating, cost) VALUES (?, ?, ?, ?)", record)
        except sqlite3.IntegrityError:
            # Handle duplicate record
            pass
    conn.commit()


def main():
    finalList = []
    yelpData = getYelpAPIData()
    for hotel in yelpData:
        finalList.append(hotel)
   #print(finalList)
    cur, conn = open_database('YelpData.db')
    make_yelp_table(finalList, cur, conn)

main()
