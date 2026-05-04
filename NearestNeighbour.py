import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points
import math
import folium


#input the bus station data downloaded in a csv file
df = pd.read_csv('bus.csv') # read the csv data

# create a new geodataframe using the latitude and longitude values from the csv file
stations = gpd.GeoDataFrame(df[['CommonName']],
                            geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

#creates map to show bus stops outside NI
m = stations.explore()
m.save("map1.html")

ni_boundary = gpd.read_file('datasets/OSNI_Open_Data_-_50K_Boundaries_-_NI_Outline.shp') #NI boundary shapefile
ni_boundary = ni_boundary.to_crs(epsg=4326) #reprojected to lat/long

stations = gpd.clip(stations, ni_boundary) #removal of stations not in NI

#add new blank column to table called ID
stations.insert(0,'ID', value=None)

#assign index value to the ID column for use in identifying rows
for index,row in stations.iterrows():
    stations.loc[index,'ID'] = index

#reproject the geodataframe to allow distance calculation- converted to Irish Tranverse Mercator
stations = stations.to_crs(epsg=2157)

#add new column to pgeodataframe into which will be placed the nearest neighbour point
stations.insert(3, 'NearestNeighbour', None)

#iterative process to find the nearest bus station for each of the bus stations in the geodataframe
for index,row in stations.iterrows():
    point = row.geometry #finds the location of each bus station
    multipoint = stations.drop(index, axis=0).geometry.union_all() #creates a list of all other bus station locations except the bus station being considered
    queried_geom, nearest_geo = nearest_points(point, multipoint) #uses nearest_points to find the closest bus station in list
    stations.loc[index, 'NearestNeighbour'] = nearest_geo #adds the location of nearest bus tation to the nearest neighbour column

#calculate the distance between each bus station and its nearest neighbour and add into Distance column
for index,row in stations.iterrows():
    row['Distance'] = row['geometry'].distance(row['NearestNeighbour'])/1000 #calculates distance in new column and divides by 1000 to get the distance in kilometres
    stations.loc[index,'Distance'] = row['Distance']

def NNA(stations):
    """
        Nearest Neighbour Analysis calculates and prints the nearest neighbour value and distribution type.
        Parameters
        ----------
        stations: GeoDataFrame
            the geodataframe containing the bus stations to be analysed

        Returns
        -------
        Nothing, it prints out the resulting distribution type.
        """
    #calculate average distance between each bus station and nearest neighbour
    average_distance = (stations['Distance'].sum())/stations['Distance'].count()

    #calculate the area of the study using the convexhull function
    Area_boundary = stations.geometry.union_all().convex_hull
    area_study = Area_boundary.area/1000000


    #calculate nearest neighbour value using NI area value
    NRvalue = 2*average_distance*math.sqrt(stations['ID'].count()/area_study)

    number = stations['ID'].count()
    print(f"There are {number} bus stations.")

    #printing the value of NN
    print(f"The nearest neighbour value is {NRvalue:.3f}")

    #using value to assign a type of distribution
    if NRvalue < 1:
        print("Bus stations have a significantly clustered distribution")
    elif NRvalue == 1:
        print("Bus stations have a significantly random distribution")
    else:
        print("Bus stations have a significantly regular distribution")

print("NORTHERN IRELAND")
NNA(stations)

#import the county outlines file and reproject
counties = gpd.read_file('datasets/osni_counties_largescale.shp')
counties = counties.to_crs(epsg=2157)

#creates list of the 6 counties
unique_counties = sorted(counties['NAME'].unique())

#iterates over each of the 6 counties
for county in unique_counties:
    county_geom = counties[counties['NAME'] == county].geometry #identifies polygon for county
    stations_clipped = gpd.clip(stations, county_geom) #clips stations geodataframe to the county
    print(str(county))
    NNA(stations_clipped)

print("--------------------------------------")

#input the post code data downloaded in a csv file
dg = pd.read_csv('postcodes.csv')

#create a geodataframe for postcode using the latitude and longitude values from the csv file
postcodes = gpd.GeoDataFrame(dg[['pcds']],
                            geometry=gpd.points_from_xy(dg['long'], dg['lat']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

postcodes = postcodes.to_crs(epsg=2157) #convert to same projection as bus stations geodataframe


#create new geodatabase with closest station assigned to each postcode from original post code geodataframe
nearest_station = postcodes.sjoin_nearest(stations, distance_col='Distance to nearest station') #sjoin_nearest built in function which includes a calculation of distance between the bus station and postcode

#creates function to find name of closest station and distance of that station from the postcode
def nearest(inputPostcode):
    """
    Find the name of the closest bus station and it's distance from the given postcode.
    Parameters
    ----------
    inputPostcode: string
        the postcode to find the closest bus station

    Returns
    -------
    name: string
        the name of the closest bus station
    distance: float
        the distance to the nearest bus station
    """
    rowID = nearest_station.loc[nearest_station['pcds'] == inputPostcode].index #finds the row of the geodataframe with a postcode matching the input postcode
    name = nearest_station['CommonName'][rowID].values[0] #finds the value in the bus station name columm of the row
    distance = nearest_station['Distance to nearest station'][rowID].values[0] #finds the value in the distance column of the row
    return  [name,distance]

#interactive text which includes option for exiting the program
print("NEAREST BUS STOP FINDER")
print("Please type exit to exit this program.")
print("--------------------------------------")
print("Provide a postcode to find the closest bus station:")
postcode = str(input()).upper() #will capitalise letters of the postcode if entered in lower case

while postcode != 'EXIT':
    while postcode not in postcodes['pcds'].values: #if postcode not found in geodataframe then ask for another postcode
        print("Please provide a valid postcode - it should be in the form BT* *** eg BT34 6HE") #reminder of correct format to enter postcode so it matches the geodataframe
        postcode = str(input()).upper()
    print(f"The nearest bus stop is: {nearest(postcode)[0]}.")
    print(f"This bus stop is approximately {nearest(postcode)[1]:.0f} metres away from this postcode.")
    print("--------------------------------------")
    print("Provide another postcode to find the closest bus station")
    postcode = str(input()).upper() #allows for multiple attempts at postcode bus station finder