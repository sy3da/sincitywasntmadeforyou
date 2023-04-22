from yelpapi import YelpAPI
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import shutil



import tomtom 
import calc_visualizations


def main():
    
    #tomtom.tomtom_data()
    calc_visualizations.tourist_attractions_per_city()
    calc_visualizations.average_distance_between_tourist_locations_per_city()
    
    cur, conn = calc_visualizations.open_database('YelpData.db')

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