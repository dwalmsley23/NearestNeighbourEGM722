
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

df = pd.read_csv('data_files/bus.csv') # read the csv data

# create a new geodataframe
stations = gpd.GeoDataFrame(df[['CommonName']], # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), # set the geometry using points_from_xy
                            crs='epsg:4326') # set the CRS using a text representation of the EPSG code for WGS84 lat/lon

stations.head() # show the new geodataframe
