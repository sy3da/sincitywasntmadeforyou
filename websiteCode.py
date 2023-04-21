import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# URL of the page to scrape
url = "https://www.nevada-demographics.com/cities_by_population"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page using Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table element containing the city population data
table = soup.find("table")

# Extract the city names and populations from the table rows
cities = []
populations = []
count = 0
for row in table.find_all("tr")[1:]:
    if count > 125:
        break
    cols = row.find_all("td")
    count +=1
    city = cols[1].text.strip()
    population = int(cols[2].text.strip().replace(",", ""))
    cities.append(city)
    populations.append(population)

# Create a horizontal bar chart of the city populations using Matplotlib
plt.barh(cities, populations)
plt.xlabel("Population")
plt.ylabel("City")
plt.title("Nevada City Populations")
plt.show()