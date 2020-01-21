import pandas as pd
import geopandas as gpd
import requests
import zipfile
from os import getcwd
import io
import matplotlib.pyplot as plt

# Download data on wildfires globally in the last 7 days from FIRMS
# print('Downloading shapefiles...')
#
# firms_activefires_url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/shapes/zips/MODIS_C6_Global_7d.zip'
# local_path = getcwd() + '/'
# r = requests.get(firms_activefires_url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
#
# z.extractall(path=local_path) # extract to folder

# filenames = [y for y in sorted(z.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
# print(filenames)

# dbf, prj, shp, shx = [filename for filename in filenames]
# fires = gpd.read_file(local_path + shp)

fires = gpd.read_file('MODIS_C6_Global_7d.shp')

fires.columns = [x.lower() for x in fires.columns]
# fires.index

print("Shape of the fires dataframe: {}".format(fires.shape))
print("Projection of fires dataframe: {}".format(fires.crs))

# Download world country borders
# world_map_url = 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip'
# r = requests.get(world_map_url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
#
#
# z.extractall(path=local_path) # extract to folder

# filenames = [y for y in sorted(z.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
# print(filenames)

# dbf, prj, shp, shx = [filename for filename in filenames]
# world = gpd.read_file(local_path + shp)

world = gpd.read_file('ne_10m_admin_0_countries.shp')

world.columns = [x.lower() for x in world.columns]

print("Shape of the countries dataframe: {}".format(world.shape))
print("Projection of countries dataframe: {}".format(world.crs))

# print("Done")


# Data preparation
fires = gpd.GeoDataFrame(geometry=fires['geometry'], index=fires.index)
# fires.shape
# world.columns
world = world[['sovereignt', 'name', 'abbrev', 'postal', 'formal_en', 'pop_est', 'pop_rank', 'gdp_md_est', 'pop_year', 'lastcensus',
       'gdp_year', 'economy', 'income_grp', 'continent', 'region_un', 'subregion', 'geometry']]

fires_proj = fires.to_crs("+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs") # convert to Eckert IV equal-area projection
world_proj = world.to_crs("+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs") # convert to Eckert IV equal-area projection

fig, ax = plt.subplots(figsize=(18,16))
world_proj.plot(ax=ax)
fires_proj.plot(ax=ax, markersize=0.5, color='red')

world_proj['area'] = pd.to_numeric(world_proj['geometry'].area)/10**6

# Calculate number of fires by country
type(world_proj)
type(fires_proj)

pts = fires_proj.copy()
polygons = world_proj.copy()

# List of how many points are found per polygon
pts_in_polys = []

# Loop over polygons with index i
for i, poly in polygons.iterrows():
    # List of points in this poly
    pts_in_this_poly = []
    # Now loop over all points with index j.
    for j, pt in pts.iterrows():
        if poly.geometry.contains(pt.geometry):
            # Then it's a hit! Add it to the list,
            # and drop it so we have less hunting.
            pts_in_this_poly.append(pt.geometry)
            pts = pts.drop([j])
    # Append number of points per polygon
    pts_in_polys.append(len(pts_in_this_poly))

# Add the number of points for each poly to the dataframe.
polygons['number_of_fires'] = gpd.GeoSeries(pts_in_polys)
