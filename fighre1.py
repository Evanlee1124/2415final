import matplotlib.pyplot as plt
import geopandas as gpd
import requests
import zipfile
import io
import os
import pandas as pd
import seaborn as sns

# URLs for shapefiles
states_url = "https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_state_500k.zip"
counties_url = "https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_county_500k.zip"

# Download directory
download_dir = "./geodata"
os.makedirs(download_dir, exist_ok=True)

# Download state shapefile
states_response = requests.get(states_url)
states_z = zipfile.ZipFile(io.BytesIO(states_response.content))
states_z.extractall(path=download_dir)

# Download county shapefile
counties_response = requests.get(counties_url)
counties_z = zipfile.ZipFile(io.BytesIO(counties_response.content))
counties_z.extractall(path=download_dir)

# Read the shapefiles
usa_states = gpd.read_file(os.path.join(download_dir, "cb_2021_us_state_500k.shp"))
usa_counties = gpd.read_file(os.path.join(download_dir, "cb_2021_us_county_500k.shp"))

# Filter for Pennsylvania (FIPS code for PA is 42)
pa_state = usa_states[usa_states['STATEFP'] == '42']
pa_counties = usa_counties[usa_counties['STATEFP'] == '42']

# Load complete restaurant data
restaurants_data = pd.read_csv('/Users/lishuangyi/Downloads/PA_Restaurants.csv')
restaurant_locations = restaurants_data[['name', 'categories', 'latitude', 'longitude', 'city']]
restaurant_locations.dropna(subset=['latitude', 'longitude'], inplace=True)

# Plot all fast food restaurant locations in Pennsylvania
plt.figure(figsize=(15, 12), dpi=300)

# Plot Pennsylvania state outline
ax = pa_state.plot(color='lightblue', edgecolor='black', linewidth=1)

# Plot county boundaries
pa_counties.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=0.5, alpha=0.5)

# Plot all restaurants
plt.scatter(restaurant_locations['longitude'], restaurant_locations['latitude'], 
            color='red', s=10, alpha=0.7, label='Fast Food Restaurants')

# Add title and legend
plt.title('All Fast Food Restaurants in Pennsylvania', fontsize=16, weight='bold')
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('./all_fast_food_restaurants_map.png')
plt.show()

print("Map of all fast food restaurants saved as 'all_fast_food_restaurants_map.png'.")
