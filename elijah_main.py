from tomtom import tomtom_data
from elijah_calculations import tourist_attractions_per_city
from elijah_calculations import average_distance_between_tourist_locations_per_city


def main():
    tomtom_data()
    tourist_attractions_per_city()
    average_distance_between_tourist_locations_per_city()

if __name__ == "__main__":
    main()