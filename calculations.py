

import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('notsincity.db')
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
ax.set_title('POIs per City')
ax.legend()

plt.subplots_adjust(bottom=0.2)
# Rotate x-axis labels by 45 degrees
plt.xticks(rotation=45)

plt.show()