
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points

df = pd.read_csv('bus.csv') # read the csv data

# create a new geodataframe
stations = gpd.GeoDataFrame(df[['CommonName']], # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon
#add new column to table
stations.insert(0,'ID', value=None)
#assign index value to the new column
for index,row in stations.iterrows():
    stations.loc[index,'ID'] = index

#add new column to place the nearest neighbour point
stations.insert(3, 'NearestNeighbour', None)

print(stations.head())

for index,row in stations.iterrows():
    point = row.geometry
    multipoint = stations.drop(index, axis=0).geometry.union_all()
    queried_geom, nearest_geo = nearest_points(point, multipoint)
    stations.loc[index, 'NearestNeighbour'] = nearest_geo


print(stations.head())


