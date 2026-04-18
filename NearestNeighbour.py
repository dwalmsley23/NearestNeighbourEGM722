
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points
import math

df = pd.read_csv('bus2.csv') # read the csv data

# create a new geodataframe
stations = gpd.GeoDataFrame(df[['CommonName']],
                            geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon
#add new column to table
stations.insert(0,'ID', value=None)
#assign index value to the new column
for index,row in stations.iterrows():
    stations.loc[index,'ID'] = index

#reproject to allow distance calculation- converted to Irish Tranverse Mercator
stations = stations.to_crs(epsg=2157)

#add new column to place the nearest neighbour point
stations.insert(3, 'NearestNeighbour', None)

print(stations.head())

for index,row in stations.iterrows():
    point = row.geometry
    multipoint = stations.drop(index, axis=0).geometry.union_all()
    queried_geom, nearest_geo = nearest_points(point, multipoint)
    stations.loc[index, 'NearestNeighbour'] = nearest_geo



#add new column to table
stations.insert(4,'Distance', value=None)


#calculate the distance between each bus station and its nearest neighbour and add into Distance column
for index,row in stations.iterrows():
    row['Distance'] = row['geometry'].distance(row['NearestNeighbour'])/1000
    stations.loc[index,'Distance'] = row['Distance']

#calculate average distance between each bus station and nearest neighbour
average_distance = (stations['Distance'].sum())/stations['Distance'].count()

print(average_distance)

#calculate nearest neighbour value using NI area value

NRvalue = 2*average_distance*math.sqrt(stations['ID'].count()/14330)

#printing the value of NN
print(f"The nearest neighbour value is {NRvalue:.3f}")

#using value to assign a type of distribution
if NRvalue < 1:
    print("Bus stations in Northern Ireland have a  significantly clustered distribution")
elif NRvalue == 1:
    print("Bus stations in Northern Ireland have a significantly random distribution")
else:
    print("Bus stations in Northern Ireland have a significantly regular distribution")

