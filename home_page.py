
from tkinter import messagebox
from datetime import datetime
from data_collection import get_earthquakes
from analysis_page import open_analysis_page
import tkinter as tk
import requests

window = tk.Tk()
window.title("Global Earthquake Tracker & Analyzer")
window.geometry("800x650")

title = tk.Label(
    window,
    text="Global Earthquake Tracker & Analyzer",
    font=("Arial", 22, "bold")
)
title.pack(pady=30)

description = tk.Label(
    window,
    text="Explore earthquake activity around the world!",
    font=("Arial", 14)
)
description.pack(pady=10)

heading = tk.Label(
    window,
    text="Earthquake Search Filters",
    font=("Arial", 16, "bold")
)
heading.pack(pady=20)

magnitude_label = tk.Label(window, text="Minimum Magnitude:")
magnitude_label.pack()

magnitude_entry = tk.Entry(window)
magnitude_entry.insert(0, "4.0")
magnitude_entry.pack(pady=5)

start_label = tk.Label(window, text="Start Date (YYYY-MM-DD):")
start_label.pack()

start_entry = tk.Entry(window)
start_entry.insert(0, "2026-11-01")
start_entry.pack(pady=5)

end_label = tk.Label(window, text="End Date (YYYY-MM-DD):")
end_label.pack()

end_entry = tk.Entry(window)
end_entry.insert(0, "2026-11-07")
end_entry.pack(pady=5)

region_label = tk.Label(window, text="Select Region:")
region_label.pack()

regions = ["Worldwide", "California", "Japan", "Indonesia", "Alaska"]
region_variable = tk.StringVar(value="Worldwide")

region_menu = tk.OptionMenu(window, region_variable, *regions)
region_menu.pack(pady=5)


def search_earthquakes():
    start_date = start_entry.get()
    end_date = end_entry.get()
    magnitude = magnitude_entry.get()
    region = region_variable.get()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        magnitude = float(magnitude)

        if start > end:
            messagebox.showerror(
                "Invalid Dates",
                "Start date must be before the end date."
            )
            return

        if magnitude < 0 or magnitude > 10:
            messagebox.showerror(
                "Invalid Magnitude",
                "Enter a magnitude between 0 and 10."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid dates and magnitude."
        )
        return

    try:
        total = get_earthquakes(
            start_date,
            end_date,
            magnitude,
            region
        )

        messagebox.showinfo(
            "Search Complete",
            f"Found {total} earthquakes!\nData saved successfully."
        )

    except requests.exceptions.RequestException as error:
        messagebox.showerror(
            "Search Error",
            f"Could not retrieve earthquake data.\n{error}"
        )


search_button = tk.Button(
    window,
    text="Search Earthquakes",
    width=20,
    command=search_earthquakes
)


search_button.pack(pady=20)

analysis_button = tk.Button(
    window,
    text="View Earthquake Analysis",
    width=25,
    command=lambda: open_analysis_page(window)
)
analysis_button.pack(pady=5)


