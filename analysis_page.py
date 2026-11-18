import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_analysis import (
    calculate_statistics,
    create_analysis_figure,
    load_earthquakes
)


def open_analysis_page(parent):
    """Open a window showing earthquake statistics and plots."""
    try:
        data = load_earthquakes()
        statistics = calculate_statistics(data)
        figure = create_analysis_figure(data)
    except (FileNotFoundError, ValueError) as error:
        messagebox.showerror(
            "Analysis Error",
            str(error),
            parent=parent
        )
        return

    page = tk.Toplevel(parent)
    page.title("Earthquake Analysis")
    page.geometry("1200x700")

    heading = tk.Label(
        page,
        text="Earthquake Data Analysis",
        font=("Arial", 22, "bold")
    )
    heading.pack(pady=15)

    statistics_text = (
        f"Total Earthquakes: {statistics['count']}    "
        f"Average Magnitude: {statistics['average_magnitude']}    "
        f"Maximum Magnitude: {statistics['maximum_magnitude']}    "
        f"Average Depth: {statistics['average_depth']} km"
    )

    statistics_label = tk.Label(
        page,
        text=statistics_text,
        font=("Arial", 12),
        wraplength=1100
    )
    statistics_label.pack(pady=10)

    canvas = FigureCanvasTkAgg(
        figure,
        master=page
    )
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    def close_page():
        plt.close(figure)
        page.destroy()

    close_button = tk.Button(
        page,
        text="Close Analysis",
        width=18,
        command=close_page
    )
    close_button.pack(pady=10)

    page.protocol(
        "WM_DELETE_WINDOW",
        close_page
    )