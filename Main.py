# This program is designed to generate the best meeting place of a group of people matched to a specific
# city. It takes in names and returns the city closest to the ideal meeting spot with its coordinates.
# Imports necessary modules
import operator
from scipy import spatial
import pandas
from geopy.geocoders import Nominatim
from GeoCoordsTest import centroid
from GeoCoordsTest import geo_coords_dm as gc


# Class to create people's locations with their name
class Locations:
    # Init method to create classes containing people and their coordinates.
    def __init__(self, name, coords: tuple[int, int] | tuple[float, float] | tuple[str, str]):
        self.name = name
        if coords.__class__ == tuple[str, str]:
            new_coords = ()
            for coord in coords:
                new_coords += float(coord)
                coords = new_coords
        formatted_coords = ()
        for Num in coords:
            formatted_coords += format(Num, '.14f'),
        self.coords = formatted_coords


# Function to subtract tuples more easily
def subtract_tuples(tup1: tuple, tup2: tuple):
    if tup1.__class__ == tuple[float, float]:
        return (abs(gc(tup1[0], tup2[0], operator.sub))), (abs(gc(tup1[1], tup2[1], operator.sub)))
    else:
        return (abs(tup1[0] - tup2[0])), (abs(tup1[1] - tup2[1]))


# Class to create cities' locations with their name
class Cities:
    def __init__(self, name, coords):
        self.name = name
        formatted_coords = ()
        for Num in coords:
            formatted_coords += format(Num, '.14f'),
        self.coords = formatted_coords

    def check_dist(self, crds: tuple):
        return subtract_tuples(self.coords, crds)


# Function to find the best coordinates between people to meet.
def find_multiple(names_lst: list):
    temp_dict = {}

    for num_ in range(len(names_lst)):
        temp_dict['p{0}'.format(num_)] = names_lst[num_]

    x_lst = []
    y_lst = []
    for num_ in temp_dict:
        x_lst.append(float(temp_dict[f"{num_}"][0]))
        y_lst.append(float(temp_dict[f"{num_}"][1]))

    main_lst = []
    for n in range(len(x_lst)):
        main_lst.append((x_lst[n], y_lst[n]))

    # Calculates the centroid, this function is located in GeoCoordsTest.py
    fin_calc = centroid(main_lst)

    return fin_calc


# Reads the .csv file containing the German Cities with their data
Cities_Data = pandas.read_csv(r'csvs/GermanCities.csv')

# Temporary variables for use later
d = {}
num = 0

# Creates a temporary dictionary that includes the city name and its coordinates
for i in Cities_Data['city']:
    d['{0}'.format(i)] = Cities(i, (float(Cities_Data['lat'][num]), float(Cities_Data['lng'][num])))
    num += 1

# Switches the temporary dictionary to this permanent dictionary.
Cities_Lst = {}
for i in d:
    Cities_Lst[d[i].name] = d[i]

# Changes the coordinates in Cities_Lst to floats
for var in Cities_Lst:
    for i in Cities_Lst[var].coords:
        i = float(i)

# Reads the placements .csv
df = pandas.read_csv('csvs/CBYX_Placements.csv')


# Temporary variables
people = {}
num = 0

# Creates a dictionary called people to be used later
for i in df['Name']:
    if df['Placement'][num].__class__ != float:
        people['{0}'.format(i)] = df['Placement'][num]
    num += 1


# This starts the program
def initialize_program():
    num_ = 0
    # Prepares the geolocator module
    app = Nominatim(user_agent="tutorial")

    # Grabs names from input
    names = eval(input("Please put spaces between first/last name and underscores between full names"))
    names = names.split('_')
    people_lst_ip = []
    for i_ in names:

        try:
            temp = app.geocode(people[i_], timeout=100000).raw   # Returns geocode data
            people_lst_ip.append((temp['lat'], temp['lon']))

            num_ += 1
        except TimeoutError:  # If it times out for one reason or another, will retry without crashing.
            print(i_, 'timeout')
            continue

    # Prints final answer
    print(check_to_cities(people_lst_ip, Cities_Lst))
    while True:
        pass


# Checks each city to the average of all the coordinates of the people trying to meet.
def check_to_cities(name_lst, city_dict: dict):

    # Refers to the function that finds the best coordinates
    x = find_multiple(name_lst)

    temp = list(city_dict.values())
    main = [x.coords if x.__class__ == Cities else None for x in temp]

    qry = main[spatial.KDTree(main).query(x)[1]]

    # Returns city name and coords
    for city_name in list(city_dict.keys()):
        if city_dict[city_name].coords == qry:
            return city_dict[city_name].name, city_dict[city_name].coords


if __name__ == '__main__':

    initialize_program()


