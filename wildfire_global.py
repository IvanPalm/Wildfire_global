import pandas as pd
import geopandas as gpd
import requests
import zipfile
from os import getcwd
import io
import matplotlib.pyplot as plt

# Download data on wildfires globally in the last 7 days from FIRMS
firms_activefires_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/shapes/zips/MODIS_C6_Global_7d.zip'
local_path = getcwd() + '/'
print('Downloading shapefile...')
r = requests.get(firms_activefires_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
print("Done")

z.extractall(path=local_path) # extract to folder

filenames = [y for y in sorted(z.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
# print(filenames)

dbf, prj, shp, shx = [filename for filename in filenames]
fires = gpd.read_file(local_path + shp)

print("Shape of the dataframe: {}".format(fires.shape))
print("Projection of dataframe: {}".format(fires.crs))

# Download world country borders
world_map_url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip'
print('Downloading shapefile...')
r = requests.get(world_map_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
print("Done")

z.extractall(path=local_path) # extract to folder

filenames = [y for y in sorted(z.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
# print(filenames)

dbf, prj, shp, shx = [filename for filename in filenames]
world = gpd.read_file(local_path + shp)

print("Shape of the dataframe: {}".format(world.shape))
print("Projection of dataframe: {}".format(world.crs))

# Add column with area of each country
world.index
