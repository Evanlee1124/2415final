import matplotlib.pyplot as plt
import geopandas as gpd
import requests
import zipfile
import io
import os
import pandas as pd

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

# Load restaurant data (replace with your file path)
restaurants_data = pd.read_csv('/Users/lishuangyi/Downloads/Top_5_Cities_Fast_Food_Restaurants_PA.csv')
restaurant_locations = restaurants_data[['name', 'categories', 'latitude', 'longitude']]
restaurant_locations.dropna(subset=['latitude', 'longitude'], inplace=True)

# Create the map
plt.figure(figsize=(15, 12), dpi=300)

# Plot Pennsylvania state outline
ax = pa_state.plot(color='lightblue', edgecolor='black', linewidth=1)

# Plot county boundaries
pa_counties.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=0.5, alpha=0.5)

# Plot restaurants
for _, row in restaurant_locations.iterrows():
    plt.plot(row['longitude'], row['latitude'], 'g^', markersize=6)  # Green triangle for restaurants

# Add map title and annotations
plt.title('Pennsylvania: Map with Counties and Fast Food Restaurants', fontsize=16)
plt.xlabel('Longitude', fontsize=10)
plt.ylabel('Latitude', fontsize=10)

# Add grid for latitude and longitude
plt.grid(True, linestyle='--', alpha=0.3)

# Adjust the plot to focus on Pennsylvania
plt.xlim(-80.5, -75)
plt.ylim(39.5, 42.5)

# Save the map
plt.tight_layout()
plt.savefig('./pennsylvania_restaurants_map.png', dpi=300, bbox_inches='tight')
plt.show()

print("Map with restaurants saved as 'pennsylvania_restaurants_map.png'.")

