import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def tourist_attractions_per_city():
  conn = sqlite3.connect('not_sin_city.db')
  cur = conn.cursor()
  cur.execute("SELECT cities.city, COUNT(*) as num_pois FROM pois INNER JOIN cities ON pois.city_id=cities.city_id GROUP BY cities.city")
  data = cur.fetchall()
  cities = [row[0] for row in data]
  pois = [row[1] for row in data]
  avg_pois = sum(pois) / len(pois)

  fig, ax = plt.subplots(figsize=(12,9))
  ax.bar(cities, pois)
  ax.axhline(y=avg_pois, color='r', linestyle='--', label='Average')
  ax.set_xlabel('City')
  ax.set_ylabel('Number of POIs')
  ax.set_title('Tourist Attractions per City')
  ax.legend()

  plt.subplots_adjust(bottom=0.2)
  # Rotate x-axis labels by 45 degrees
  plt.xticks(rotation=45)

  plt.show()
  
  
  

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
      city_avg_distance = np.mean([distance(coords[i], coords[j]).km for i in range(len(coords)) for j in range(i+1, len(coords))])
      if city_avg_distance > 0:
          city_distances[city] = city_avg_distance

  # Plot the results
  plt.subplots(figsize=(12,9))
  plt.bar(city_distances.keys(), city_distances.values())
  plt.xticks(rotation=90)
  plt.xlabel('City')
  plt.ylabel('Average distance (km)')
  plt.title('Average distance between tourist attractions per city')
  plt.subplots_adjust(bottom=0.2)
  plt.xticks(rotation=45)
  plt.show()