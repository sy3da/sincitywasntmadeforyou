import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from geopy.distance import distance
from geopy.distance import geodesic

from yelpapi import YelpAPI
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#calculation
def highestratedhotel(cur,conn):
    info = cur.execute("select hotel_name, city, rating, cost from YelpData order by city")
    cs = info.fetchall()
    highestRated = {}

    # Loop through the list of hotels and update the dictionary if we find a higher rated hotel for a given city
    for hotel in cs:
        name, city, rating, cost = hotel
        if city not in highestRated or rating > highestRated[city][1]:
            highestRated[city] = (name, rating, city, cost)

    # Convert the dictionary to a list of tuples
    highestratedhotelLst = list(highestRated.values())

    with open('calculations.txt', 'a') as f:
        f.write("\n Hotel Name, Rating, City\n")
        for hotel in highestratedhotelLst:
            f.write("{}, {}, {}\n".format(hotel[0], hotel[1], hotel[2]))
        f.write("\n")
    return highestratedhotelLst

#using the highest rated hotel list  
def bargraphHotel(hotelList):
    # Create empty lists for each category
    hotel_names = []
    ratings = []
    cities = []

    # Loop through each tuple in the original list and extract the data
    for hotel in hotelList:
        hotel_names.append(hotel[0])
        ratings.append(hotel[1])
        cities.append(hotel[2])

    city = cities
    values = ratings
    
    fig = plt.figure(figsize=(15, 8))
    
    # creating the bar plot
    plt.bar(city, values, color ='maroon', width = 0.5)
    
    plt.xlabel("City")
    plt.ylabel("Rating")
    plt.title("Highest Rated Hotel for each City")
    
    # rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    plt.savefig('Highest Rated Hotel for each City')

def scatterplot(hotelList):
    hotel_names = []
    ratings = []
    cities = []

    # Loop through each tuple in the original list and extract the data
    for hotel in hotelList:
        hotel_names.append(hotel[0])
        ratings.append(hotel[1])
        cities.append(hotel[2])

    city = cities
    values = ratings
    plt.scatter(city, values, c ="blue")
    plt.xlabel("City")
    plt.ylabel("Hotel Ratings")
    plt.title("Hotel Ratings by City")
    # rotate x-axis labels for better visibility
    plt.xticks(rotation=45)
  
    plt.savefig('Hotel Ratings by City.png')
    
    
    
def tourist_attractions_per_city():
  conn = sqlite3.connect('not_sin_city.db')
  cur = conn.cursor()
  cur.execute("SELECT cities.city, COUNT(*) as num_pois FROM pois INNER JOIN cities ON pois.city_id=cities.city_id GROUP BY cities.city")
  data = cur.fetchall()
  cities = [row[0] for row in data]
  pois = [row[1] for row in data]
  avg_pois = sum(pois) / len(pois)

  fig, ax = plt.subplots(figsize=(15,10))
  ax.bar(cities, pois)
  ax.axhline(y=avg_pois, color='r', linestyle='--', label='Average')
  ax.set_xlabel('City', fontsize=16)
  ax.set_ylabel('Number of POIs', fontsize=16)
  ax.set_title('Tourist Attractions per City', fontsize=16)
  ax.legend()

  plt.subplots_adjust(bottom=0.2)
  # Rotate x-axis labels by 45 degrees
  plt.xticks(rotation=45, fontsize=16)


  with open('calculations.txt', 'a') as f:
    f.write('\nCity\tNumber of Tourist Attractions\n')
    for i in range(len(cities)):
        f.write(f'{cities[i]}\t{pois[i]}\n')
    f.write(f'Average\t{avg_pois}\n\n')
  fig.savefig('tourist_attractions_per_city.png')
  
  
  

def average_distance_between_tourist_locations_per_city():
    # Connect to the database
    conn = sqlite3.connect('not_sin_city.db')

    # Execute the join query
    query = '''
        SELECT p.poi_id, p.name, c.city, pos.lat, pos.lon
        FROM pois p
        JOIN cities c ON p.city_id = c.city_id
        JOIN positions pos ON p.poi_id = pos.poi_id
    '''
    result = conn.execute(query).fetchall()

    # Group the result by city
    city_data = {}
    for poi_id, name, city, lat, lon in result:
        if city not in city_data:
            city_data[city] = []
        city_data[city].append((lat, lon))

    # Compute the average distances for each city
    city_distances = {}
    for city, coords in city_data.items():
      if len(coords) > 1:
        city_avg_distance = np.mean([geodesic(coords[i], coords[j]).km for i in range(len(coords)) for j in range(i+1, len(coords))])
        if city_avg_distance > 0:
            city_distances[city] = city_avg_distance

    with open('calculations.txt', 'a') as f:
        f.write('\nCity\tAverage Distance between Tourist Locations\n')
        for city, distance in city_distances.items():
            f.write(f'{city}: {distance:.2f} km\n')
        f.write('\n')
        
    # Plot the results
    plt.subplots(figsize=(15,10))
    plt.bar(city_distances.keys(), city_distances.values())
    plt.xticks(rotation=45, fontsize=16)
    plt.xlabel('City', fontsize=16)
    plt.ylabel('Average distance (km)', fontsize=16)
    plt.title('Average distance between tourist attractions per city', fontsize=16)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('average_distance_between_tourist_attractions_per_city.png')


def city_pop_proportions():
    conn = sqlite3.connect('not_sin_city.db')
    cur = conn.cursor()
    cur.execute('SELECT city, population FROM populations')
    result = cur.fetchall()

    cities = []
    pops = []
    for item in result:
        cities.append(item[0])
        pops.append(item[1])

   

    # add some dummy cities with zero population
    for i in range(126 - len(cities)):
        cities.append(f"Dummy{i}")
        pops.append(0)

    plt.subplots()
    plt.pie(pops, labels=cities, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Cities by Population in Nebraska', fontsize=16)
    plt.savefig('cities_by_pop_NE.png')
