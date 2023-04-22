import requests
from bs4 import BeautifulSoup
import os
import sqlite3

def open_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

def make_pop_table(cur, conn):
    # create a table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS populations (id INTEGER PRIMARY KEY, city TEXT UNIQUE, population INTEGER)''')

    # BeautifulSoup Scraping
    url = 'https://www.nevada-demographics.com/cities_by_population'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table') # Get table of cities and populations
    rows = table.find_all('tr')[1:]  

    # Loop through the rows and insert the data into the database
    count = 0
    for row in rows:
        columns = row.find_all('td')
        name = columns[1].text.strip()
        population = int(columns[2].text.replace(',', ''))
        try:
            cur.execute('INSERT INTO populations (city, population) VALUES (?, ?)', (name, population))
            count += 1
        except sqlite3.IntegrityError: # Ignores duplicate city names
            pass
        if count == 25 or name == 'Hiko':  # Limit to 25 cities per run
            break

    # Commit the changes and close the connection
    conn.commit()

def main():
    cur, conn = open_database('not_sin_city.db') # Connect to the database
    make_pop_table(cur, conn)

main()