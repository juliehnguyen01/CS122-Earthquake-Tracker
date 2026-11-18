from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_FILE = Path(__file__).parent / "data" / "earthquakes.csv"


def load_earthquakes():
    """Load and clean the earthquake CSV data."""
    data = pd.read_csv(DATA_FILE)

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Magnitude",
        "Depth",
        "Latitude",
        "Longitude"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(
        subset=[
            "Date",
            "Magnitude",
            "Depth",
            "Latitude",
            "Longitude"
        ]
    )

    return data


def calculate_statistics(data):
    """Calculate summary statistics for the earthquake data."""
    if data.empty:
        return {
            "count": 0,
            "average_magnitude": 0,
            "maximum_magnitude": 0,
            "average_depth": 0
        }

    return {
        "count": len(data),
        "average_magnitude": round(
            float(np.mean(data["Magnitude"])),
            2
        ),
        "maximum_magnitude": round(
            float(np.max(data["Magnitude"])),
            2
        ),
        "average_depth": round(
            float(np.mean(data["Depth"])),
            2
        )
    }


def create_analysis_figure(data):
    """Create earthquake visualizations."""
    if data.empty:
        raise ValueError(
            "There is no earthquake data to visualize."
        )

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(11, 5)
    )

    axes[0].hist(
        data["Magnitude"],
        bins=10,
        color="steelblue",
        edgecolor="black"
    )
    axes[0].set_title(
        "Earthquake Magnitude Distribution"
    )
    axes[0].set_xlabel("Magnitude")
    axes[0].set_ylabel("Number of Earthquakes")

    scatter = axes[1].scatter(
        data["Longitude"],
        data["Latitude"],
        c=data["Magnitude"],
        cmap="viridis",
        s=50,
        edgecolors="black"
    )
    axes[1].set_title("Earthquake Locations")
    axes[1].set_xlabel("Longitude")
    axes[1].set_ylabel("Latitude")

    figure.colorbar(
        scatter,
        ax=axes[1],
        label="Magnitude"
    )

    figure.tight_layout()

    return figure