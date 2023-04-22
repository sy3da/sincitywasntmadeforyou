from yelpapi import YelpAPI
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

#Getting API Data and storing into List
def getYelpAPIData(cur):
    api_key = '84yyM6N4wVI_D4s419Jt40ZzW33AUxXvmR1hHUfR4j97ce2WibAUber4MGGirF_e7RjyF0PEd_tJV6F-NfZmBM0Xakb5x3yFR8o_Eh-a81v-hDkq3dm-u-4KWfkuZHYx'
    cities = ['Henderson', 'Reno', 'Sparks', 'Carson City', 'Sun Valley', 'Elko', 'Boulder City', 'Fallon', 'Winnemucca']
    client = YelpAPI(api_key)

    hotel_list = []
    cur.execute("SELECT COUNT(*) FROM YelpData")
    row_count = cur.fetchone()[0]
    city_number = 0
    for city in cities:
        # Yelp API parameters
        params = {
            'term': 'hotel',
            'location': city,
            'limit': 15
        }
        if row_count != 0 and row_count > city_number:
            city_number += 1
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

def make_yelp_table(data, cur, conn):
    hotel_count = 0
    
    for record in data:
        if(hotel_count >= 25):
            break
        try:
            cur.execute("INSERT INTO YelpData (hotel_name, city, rating, cost) VALUES (?, ?, ?, ?)", record)
            hotel_count += 1
            
        except sqlite3.IntegrityError:
            # Handle duplicate record
            pass
    conn.commit()