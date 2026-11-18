
from tkinter import messagebox
from datetime import datetime
from data_collection import get_earthquakes
from analysis_page import open_analysis_page
import tkinter as tk
import requests

navy = "#101C30"
light_navy = "#1D304A"
blue = "#3177D4"
white = "#FFFFFF"
light_text = "#D5E2F2"

window = tk.Tk()
window.title("Global Earthquake Tracker & Analyzer")
window.geometry("800x700")
window.configure(bg=navy)

title = tk.Label(
    window,
    text="Global Earthquake Tracker & Analyzer",
    font=("Arial", 22, "bold"),
    bg=navy,
    fg=white
)
title.pack(pady=(30, 10))

description = tk.Label(
    window,
    text="Explore earthquake activity around the world!",
    font=("Arial", 13),
    bg=navy,
    fg=light_text
)
description.pack(pady=(0, 20))

filter_frame = tk.Frame(
    window,
    bg=light_navy,
    padx=40,
    pady=20
)
filter_frame.pack(pady=10)

heading = tk.Label(
    filter_frame,
    text="Earthquake Search Filters",
    font=("Arial", 16, "bold"),
    bg=light_navy,
    fg=white
)
heading.pack(pady=(0, 15))

magnitude_label = tk.Label(
    filter_frame,
    text="Minimum Magnitude:",
    bg=light_navy,
    fg=light_text,
    font=("Arial", 11)
)
magnitude_label.pack()

magnitude_entry = tk.Entry(
    filter_frame,
    width=25,
    font=("Arial", 12),
    bg="#304762",
    fg=white,
    insertbackground=white,
    relief="flat"
)
magnitude_entry.insert(0, "4.0")
magnitude_entry.pack(pady=(5, 12), ipady=5)

start_label = tk.Label(
    filter_frame,
    text="Start Date (YYYY-MM-DD):",
    bg=light_navy,
    fg=light_text,
    font=("Arial", 11)
)
start_label.pack()

start_entry = tk.Entry(
    filter_frame,
    width=25,
    font=("Arial", 12),
    bg="#304762",
    fg=white,
    insertbackground=white,
    relief="flat"
)
start_entry.insert(0, "2026-11-01")
start_entry.pack(pady=(5, 12), ipady=5)

end_label = tk.Label(
    filter_frame,
    text="End Date (YYYY-MM-DD):",
    bg=light_navy,
    fg=light_text,
    font=("Arial", 11)
)
end_label.pack()

end_entry = tk.Entry(
    filter_frame,
    width=25,
    font=("Arial", 12),
    bg="#304762",
    fg=white,
    insertbackground=white,
    relief="flat"
)
end_entry.insert(0, "2026-11-07")
end_entry.pack(pady=(5, 12), ipady=5)

region_label = tk.Label(
    filter_frame,
    text="Select Region:",
    bg=light_navy,
    fg=light_text,
    font=("Arial", 11)
)
region_label.pack()

regions = ["Worldwide", "California", "Japan", "Indonesia", "Alaska"]
region_variable = tk.StringVar(value="Worldwide")

region_menu = tk.OptionMenu(
    filter_frame,
    region_variable,
    *regions
)
region_menu.config(
    width=20,
    font=("Arial", 11),
    bg="#304762",
    fg=white,
    activebackground=blue,
    activeforeground=white,
    highlightthickness=0,
    relief="flat"
)
region_menu["menu"].config(
    bg=light_navy,
    fg=white
)
region_menu.pack(pady=(5, 10))


def reset_filters():
    magnitude_entry.delete(0, tk.END)
    magnitude_entry.insert(0, "4.0")

    start_entry.delete(0, tk.END)
    start_entry.insert(0, "2026-11-01")

    end_entry.delete(0, tk.END)
    end_entry.insert(0, "2026-11-07")

    region_variable.set("Worldwide")


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
    width=25,
    font=("Arial", 11, "bold"),
    bg=blue,
    fg=navy,
    activebackground="#245CA8",
    activeforeground=navy,
    relief="flat",
    command=search_earthquakes
)
search_button.pack(pady=(15, 5), ipady=6)

reset_button = tk.Button(
    window,
    text="Reset Filters",
    width=25,
    font=("Arial", 11),
    bg="#304762",
    fg=navy,
    activebackground="#405C7D",
    activeforeground=navy,
    relief="flat",
    command=reset_filters
)
reset_button.pack(pady=5, ipady=6)

analysis_button = tk.Button(
    window,
    text="View Earthquake Analysis",
    width=25,
    font=("Arial", 11, "bold"),
    bg="#245CA8",
    fg=navy,
    activebackground=blue,
    activeforeground=navy,
    relief="flat",
    command=lambda: open_analysis_page(window)
)
analysis_button.pack(pady=5, ipady=6)
