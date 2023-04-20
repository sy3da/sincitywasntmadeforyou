
import requests
import sqlite3
import json
import time
import matplotlib.pyplot as plt

'''
todo

make table for just las vegas results, or just for restaurants
make the two tables have shared integer keys for a join
make second plot comparing average las vegas tourist attractions compared to total average of all other cities
'''




# set up database connection
conn = sqlite3.connect('tourist_attractions.db')
c = conn.cursor()

# create table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS tourist_attractions
             (name text, category text, address text, lat real, lon real, city text, UNIQUE(name, address))''')

# set up API request parameters
api_key = "cx2F39RYHouQTgQi2sV4tuBXMyrJQJ6t"
radius = 20000  # 10 km radius around each city  
cities = {
          "Henderson": (36.0397, -114.9817),
          "North Las Vegas": (36.1989, -115.1175), 
          "Reno": (39.5296, -119.8138), 
          "Sparks": (39.5348, -119.7527), 
          "Carson City": (39.1638, -119.7674),
          "Fernley": (39.6080, -119.2518),
          "Mesquite": (36.8055,-114.0672),
          "Elko": (40.8324,-115.7631),
          "Boulder City": (35.9782,-114.8345),
          "Fallon": (39.4749,-118.7770),
          "Winnemucca": (40.9730,-117.7357),
          "West Wendover": (40.7391,-114.0733),
          "Ely": (39.2533,-114.8742),
          "Yerington": (38.9858,-119.1629),
          "Carlin": (40.7138,-116.1040),
          "Lovelock": (40.1794,-118.4735),
          "Wells": (41.1116,-114.9645),
          "Caliente": (37.6150,-114.5119),
          }
    
    
# loop over each city and make API requests

for city, (lat, lon) in cities.items():
    print(f"Requesting tourist attractions in {city}...")
    url = f"https://api.tomtom.com/search/2/categorySearch/important%20tourist%20attraction.json?key={api_key}&lat={lat}&lon={lon}&radius={radius}"
    response = requests.get(url)
    data = json.loads(response.text)
    results = [[r["poi"]["name"], r["poi"]["categories"][0], r["address"]["freeformAddress"], r["position"]["lat"], r["position"]["lon"], city] for r in data["results"]]
    
    # insert results into database, ignoring duplicates
    
    for r in results:
      ok = r[2].split(',')
      if (r[1] == "important tourist attraction" and ok[1].strip() != "Las Vegas" and ok[0].strip() != "Las Vegas"):
        try:
          c.execute("INSERT INTO tourist_attractions VALUES (?, ?, ?, ?, ?, ?)", r)
        except sqlite3.IntegrityError:
          pass

    # commit changes to database
    conn.commit()

# calcul
# 
# 
# 
# 
# 
# 
# 
# 
# 
# ate average number of tourist attractions around each city
averages = {}
category = "important tourist attraction"
for city in cities.keys():
    c.execute(f"SELECT COUNT(*) FROM tourist_attractions WHERE city='{city}' AND category='{category}'")
    count = c.fetchone()[0]
    averages[city] = count

# plot averages using Matplotlib
plt.bar(range(len(averages)), list(averages.values()), align='center')
plt.xticks(range(len(averages)), list(averages.keys()))
plt.title("Average Number of Tourist Attractions within 10km Radius")
plt.xlabel("City")
plt.ylabel("Number of Tourist Attractions")
plt.show()
plt.savefig('average_tourist_attractions.png')

# close database connection
conn.close()