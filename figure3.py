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

# Load restaurant data (replace with your file path)
restaurants_data = pd.read_csv('/Users/lishuangyi/Downloads/Top_5_Cities_Fast_Food_Restaurants_PA.csv')
restaurant_locations = restaurants_data[['name', 'categories', 'latitude', 'longitude', 'city']]
restaurant_locations.dropna(subset=['latitude', 'longitude'], inplace=True)

# Define specific cities and their populations
cities_with_data = {
    'Philadelphia': {'population': 1603797},
    'Pittsburgh': {'population': 302971},
    'Erie': {'population': 94717},
    'Harrisburg': {'population': 49528},
    'Johnstown': {'population': 19241}
}

# Calculate the number of fast food restaurants in each city
restaurant_counts = restaurant_locations['city'].value_counts()
for city in cities_with_data.keys():
    cities_with_data[city]['restaurants'] = restaurant_counts.get(city, 0)

# Create a DataFrame for plotting
cities = list(cities_with_data.keys())
data = pd.DataFrame({
    'City': cities,
    'Population': [cities_with_data[city]['population'] for city in cities],
    'Fast Food Restaurants': [cities_with_data[city]['restaurants'] for city in cities]
})

# Plot population and fast food restaurants in the same chart
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot population
color = 'tab:blue'
ax1.set_xlabel('City', fontsize=12)
ax1.set_ylabel('Population', color=color, fontsize=12)
ax1.bar(cities, data['Population'], color=color, alpha=0.7, label='Population')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(range(len(cities)))
ax1.set_xticklabels(cities, rotation=45)

# Add secondary axis for fast food restaurants
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Fast Food Restaurants', color=color, fontsize=12)
ax2.plot(cities, data['Fast Food Restaurants'], color=color, marker='o', label='Fast Food Restaurants')
ax2.tick_params(axis='y', labelcolor=color)

# Add title and legend
plt.title('Population vs Fast Food Restaurants in Top Cities of Pennsylvania', fontsize=14, weight='bold')
fig.tight_layout()
plt.savefig('./population_vs_restaurants_combined.png')
plt.show()

print("Combined chart saved as 'population_vs_restaurants_combined.png'.")

