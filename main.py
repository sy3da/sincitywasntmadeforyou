from yelpapi import YelpAPI
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import shutil



import tomtom 
import calc_visualizations
import websiteCode
import hotelcode



def main():
    
    tomtom.tomtom_data()
    cur, conn = websiteCode.open_database('not_sin_city.db') # Connect to the database
    calc_visualizations.tourist_attractions_per_city()
    calc_visualizations.average_distance_between_tourist_locations_per_city()
    websiteCode.make_pop_table(cur, conn)
    
    finalList = []
    cur, conn = hotelcode.open_database('not_sin_city.db')
    cur.execute("CREATE TABLE IF NOT EXISTS YelpData (hotel_name TEXT, city TEXT, rating INTEGER, cost TEXT, UNIQUE(hotel_name, city))")
    yelpData = hotelcode.getYelpAPIData(cur)
    for hotel in yelpData:
        finalList.append(hotel)
    
    hotelcode.make_yelp_table(finalList, cur, conn)
   
    cur, conn = calc_visualizations.open_database('not_sin_city.db')
    high_rated = calc_visualizations.highestratedhotel(cur,conn)
    

    calc_visualizations.bargraphHotel(high_rated)

    calc_visualizations.scatterplot(high_rated)
    
    subdir = 'visualizations'
    if not os.path.exists(subdir):
        os.mkdir(subdir)

# Iterate through files in the current directory
    for filename in os.listdir('.'):
    # Check if the file has the desired extension (PNG)
        if filename.endswith('.png'):
        # Move the file to the new subdirectory
            shutil.move(filename, os.path.join(subdir, filename))

if __name__ == "__main__":
    main()