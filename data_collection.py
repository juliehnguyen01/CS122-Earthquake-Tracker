
# CS 122 Final Project
# Global Earthquake Tracker & Analyzer
# Author #1: Julie Nguyen
# Data Collection and Storage

import requests
import csv
from datetime import datetime
from pathlib import Path

# USGS Earthquake API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Search for earthquakes
parameters = {
    "format": "geojson",
    "starttime": "2026-11-01",
    "endtime": "2026-11-07",
    "minmagnitude": 4.0,
    "limit": 100
}

# Request earthquake data
response = requests.get(url, params=parameters, timeout=30)
response.raise_for_status()

# Convert response to a Python dictionary
data = response.json()

# Get earthquake records
earthquakes = data["features"]

# Save CSV inside the project's data folder
data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)
file_name = data_folder / "earthquakes.csv"

# Open CSV file
with open(file_name, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Column names
    writer.writerow([
        "Date", "Location", "Magnitude",
        "Depth", "Latitude", "Longitude"
    ])

    # Save each earthquake
    for earthquake in earthquakes:
        properties = earthquake["properties"]
        coordinates = earthquake["geometry"]["coordinates"]

        # Convert earthquake time to readable date
        timestamp = properties["time"] / 1000
        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        location = properties["place"]
        magnitude = properties["mag"]

        longitude = coordinates[0]
        latitude = coordinates[1]
        depth = coordinates[2]

        writer.writerow([
            date, location, magnitude,
            depth, latitude, longitude
        ])

# Display results
print("Global Earthquake Tracker")
print("-------------------------")
print("Total earthquakes retrieved:", len(earthquakes))
print("Earthquake data saved to:", file_name)

