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
#select data from table to make the highest rated hotel per city list
def highestratedhotel(cur,conn):
    info = cur.execute("select hotel_name, city, rating from YelpData order by city")
    cs = info.fetchall() #fetchall converts our data into a list
    highestRated = {}

    # Loop through the list of hotels and update the dictionary if we find a higher rated hotel for a given city
    for hotel in cs:
        name, city, rating = hotel
        if city not in highestRated or rating > highestRated[city][1]:
            highestRated[city] = (name, rating, city)

    # Convert the dictionary to a list of tuples and return it
    highestratedhotelLst = list(highestRated.values())

    #writing the list to a file
    with open('highest_rated_hotels.txt', 'w') as f:
        f.write("Hotel Name, Rating, City\n")
        for hotel in highestratedhotelLst:
            f.write("{}, {}, {}\n".format(hotel[0], hotel[1], hotel[2]))
    return highestratedhotelLst

#using the highest rated hotel list to create a bar graph 
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
    
    fig = plt.figure(figsize=(10, 5))
    
    # creating the bar plot
    plt.bar(city, values, color ='maroon',
            width = 0.4)
    
    plt.xlabel("City")
    plt.ylabel("Rating")
    plt.title("Highest Rated Hotel for each City")
    plt.show()


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
    plt.xticks(rotation=90)
    # To show the plot
    plt.show()
 
def main():
    #Establishing Database connection
    cur, conn = open_database('YelpData.db')

    #Calling function to calculate highest rated hotel per city and outputs it to text file
    high_rated = highestratedhotel(cur,conn)
    #print(high_rated)
    
    #calling function to create bargraph of highest rated hotel per city
    bargraphHotel(high_rated)

    scatterplot(high_rated)

main()