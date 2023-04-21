import requests
import sqlite3
import json
import time




# set up database connection

def tomtom_data():
  conn = sqlite3.connect('not_sin_city.db')

  conn.execute('''CREATE TABLE IF NOT EXISTS cities
              (city_id INTEGER PRIMARY KEY AUTOINCREMENT, city text UNIQUE)''')
  conn.execute('''CREATE TABLE IF NOT EXISTS pois
              (poi_id INTEGER PRIMARY KEY AUTOINCREMENT, name text, city_id INT, FOREIGN KEY (city_id) REFERENCES cities(city_id))''')
  conn.execute('''CREATE TABLE IF NOT EXISTS positions
              (poi_id INT, lat real, lon real, FOREIGN KEY (poi_id) REFERENCES pois(poi_id))''')
  # set up API request parameters
  api_key = "cx2F39RYHouQTgQi2sV4tuBXMyrJQJ6t"
  radius = 20000  # 10 km radius around each city  
  cities = {
            "Henderson": (36.0397, -114.9817),
            "Reno": (39.5296, -119.8138), 
            "North Las Vegas": (36.1989, -115.1175), 
            "Sparks": (39.5348, -119.7527), 
            "Carson City": (39.1638, -119.7674),
            "Sun Valley": (39.5963, -119.7760),
            "Elko": (40.8324,-115.7631),
            "Dayton": (39.2408, -119.5787),
            "Boulder City": (35.9782,-114.8345),
            "Gardnerville Ranchos": (38.8975, -119.7516),
            "Cold Springs": (39.6967, -119.9319), 
            "Incline Village": (39.2503, -119.9656),
            "Fallon": (39.4749,-118.7770),
            "Laughlin": (35.1678, -114.5730),
            "Silver Springs": (39.3884, -119.2219),
            "West Wendover": (40.7391,-114.0733),
            "Ely": (39.2533,-114.8742), 
            "Carlin": (40.7138,-116.1040),
            }
  cur = conn.cursor()


  # Loop over each city and make API requests
  total_count = 0
  poi_count = 0
  position_count = 0

  cur.execute("SELECT COUNT(*) FROM cities")
  row_count = cur.fetchone()[0]
  city_number = 0
  for city, (lat, lon) in cities.items():
    if total_count >= 50:
      break
    if row_count != 0 and row_count > city_number:
      city_number += 1
      continue 
    url = f"https://api.tomtom.com/search/2/categorySearch/tourist.json?key={api_key}&lat={lat}&lon={lon}&radius={radius}&limit=100"
    response = requests.get(url)
    data = json.loads(response.text)
    the_next_city = city
    # Iterate over the results and insert into tables
    for result in data['results']:
      poi_name = result['poi']['name']
      city_name = result['address']['localName']
      if city_name == 'Las Vegas':
        continue
    
      # Insert into the cities table
      try:
        conn.execute("INSERT INTO cities (city) VALUES (?)", (city_name,))
      except sqlite3.IntegrityError:
        pass
      
      # Get the city_id of the current city
      cur.execute("SELECT city_id FROM cities WHERE city=?", (city_name,))
      city_id = cur.fetchone()[0]
      
      # Insert into the pois table with the current city_id
      try:
        if poi_count >= 25:
          break
        conn.execute("INSERT INTO pois (name, city_id) VALUES (?, ?)", (poi_name, city_id))
        poi_count += 1
        total_count += 1
      except sqlite3.IntegrityError:
        pass
      
      # Get the poi_id of the current poi
      cur.execute("SELECT poi_id FROM pois WHERE name=?", (poi_name,))
      poi_id = cur.fetchone()[0]
      
      # Insert into the positions table with the current poi_id
      position_result = result['position']
      try:
        if position_count >= 25:
          break
        conn.execute("INSERT INTO positions (poi_id, lat, lon) VALUES (?, ?, ?)", (poi_id, position_result['lat'], position_result['lon']))
        position_count += 1
        total_count += 1
      except sqlite3.IntegrityError:
        pass

    
      # commit changes to database
  conn.commit()


