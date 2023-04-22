import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to the database and create a table if it doesn't exist
conn = sqlite3.connect('cities.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS cities (id INTEGER PRIMARY KEY, city TEXT UNIQUE, population INTEGER)''')

# BeautifulSoup Scraping
url = 'https://www.nevada-demographics.com/cities_by_population'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Get table of cities and populations
table = soup.find('table')
rows = table.find_all('tr')[1:]  

# Loop through the rows and insert the data into the database
count = 0
for row in rows:
    columns = row.find_all('td')
    name = columns[1].text.strip()
    population = int(columns[2].text.replace(',', ''))
    try:
        c.execute('INSERT INTO cities (city, population) VALUES (?, ?)', (name, population))
        count += 1
    except sqlite3.IntegrityError: # Ignores duplicate city names
        pass
    if count == 25 or name == 'Hiko':  # Limit to 25 items per run
        break

# Commit the changes and close the connection
conn.commit()
conn.close()