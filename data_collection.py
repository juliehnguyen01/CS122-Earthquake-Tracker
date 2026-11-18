
import requests
import csv
from datetime import datetime, timezone
from pathlib import Path


def get_earthquakes(start_date, end_date, magnitude, region):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    parameters = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": magnitude,
        "limit": 100
    }

    regions = {
        "California": (32, 42, -125, -114),
        "Japan": (24, 46, 123, 146),
        "Indonesia": (-11, 6, 95, 141),
        "Alaska": (51, 72, -170, -130)
    }

    if region in regions:
        bounds = regions[region]
        parameters["minlatitude"] = bounds[0]
        parameters["maxlatitude"] = bounds[1]
        parameters["minlongitude"] = bounds[2]
        parameters["maxlongitude"] = bounds[3]

    response = requests.get(url, params=parameters, timeout=30)
    response.raise_for_status()

    data = response.json()
    earthquakes = data["features"]

    data_folder = Path(__file__).parent / "data"
    data_folder.mkdir(exist_ok=True)
    file_name = data_folder / "earthquakes.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Date", "Location", "Magnitude",
            "Depth", "Latitude", "Longitude"
        ])

        for earthquake in earthquakes:
            properties = earthquake["properties"]
            coordinates = earthquake["geometry"]["coordinates"]

            timestamp = properties["time"] / 1000
            date = datetime.fromtimestamp(
                timestamp, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")

            location = properties["place"]
            magnitude = properties["mag"]

            longitude = coordinates[0]
            latitude = coordinates[1]
            depth = coordinates[2]

            writer.writerow([
                date, location, magnitude,
                depth, latitude, longitude
            ])

    return len(earthquakes)
