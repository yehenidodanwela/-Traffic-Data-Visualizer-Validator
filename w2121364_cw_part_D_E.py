#Author: D. W. Yeheni Kaveesha Dodanwela
#Date: 23.12.2024
#Student ID: 20241486 (IIT Number) | w2121364 (UoW Number)

import tkinter as tk
import csv
from collections import defaultdict
import w2121364_cw_part_A_B_C

# Task D: Histogram Display

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        # store the input data and initialize the main application window
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None
        self.setup_window()
        self.draw_histogram()
        self.add_legend()

    def setup_window(self):
        """
        Sets up window and canvas for the histogram display.
        """
        self.root.title("Histogram")
        self.root.geometry("1500x500")  # set the dimensions of the window
        self.canvas = tk.Canvas(self.root, width=1500, height=500, bg="white")  # create a drawing canvas
        self.canvas.pack()  # add the canvas to the window

    def draw_histogram(self):
        """
        Draws the histogram representing vehicle frequencies per hour for two junctions.
        """
        # define layout parameters for the histogram
        margin = 50  # margin around the canvas
        canvas_width = 1450
        canvas_height = 500
        number_of_hours = len(self.traffic_data)  # number of hours in the traffic data
        available_width = canvas_width - 2 * margin  # calculate usable drawing area

        # calculate bar dimensions
        max_bar_width = 20  # maximum width of a bar
        hour_spacing = available_width / number_of_hours  # space allocated per hour on the x-axis
        bar_width = min(max_bar_width, (hour_spacing - 10) / 2)  # adjust bar width to fit the space and don't overlap
        bar_spacing = 0  # no gap between junction pairs
        max_height = canvas_height - 2 * margin -10  # maximum bar height

        max_value = max(max(values) for values in self.traffic_data.values())  # find the maximum traffuc count

        # draw the base x-axis line
        y_base = canvas_height - margin
        self.canvas.create_line(
        margin, y_base,  # start point
        canvas_width - margin, y_base,  # end point
        width=2,
        fill="black")

        # add title
        self.canvas.create_text(
            canvas_width / 2, margin / 2,
            text=f"Histogram of Vehicles Frequency per Hour ({self.date})",
            font=("Arial", 16), fill="black"
        )

        # add label for the x-axis
        self.canvas.create_text(
            canvas_width / 2, canvas_height - margin / 4,
            text="Hours 00:00 to 24:00", font=("Arial", 12), fill="black"
        )

        # draw bars for each hour and junction
        for i, (label, values) in enumerate(self.traffic_data.items()):
            x_start = margin + i * hour_spacing  # calculate the starting x-coordinate for the hour
            # calculate the x-coordinates for the first and second bars
            bar1_x1 = x_start + (hour_spacing - (2 * bar_width + bar_spacing)) / 2
            bar1_x2 = bar1_x1 + bar_width
            bar2_x1 = bar1_x2 + bar_spacing
            bar2_x2 = bar2_x1 + bar_width

            # calculate the height of the bars based on max height
            bar1_height = (values[0] / max_value) * max_height
            bar2_height = (values[1] / max_value) * max_height
            y_base = canvas_height - margin  # y-coordinate for the base of the bars

            # draw and label the first bar (for Elm Avenue/Rabbit Road)
            self.canvas.create_rectangle(
                bar1_x1, y_base - bar1_height,
                bar1_x2, y_base,
                fill="#42daf5" # light blue for first junction
            )
            self.canvas.create_text(
                bar1_x1 + bar_width / 2,
                y_base - bar1_height - 10,
                text=str(values[0]),
                fill="black"
            )

            # draw and label the second bar (for Hanley Highway/Westway)
            self.canvas.create_rectangle(
                bar2_x1, y_base - bar2_height,
                bar2_x2, y_base,
                fill="#90EE90" # light green for second junction
            )
            self.canvas.create_text(
                bar2_x1 + bar_width / 2,
                y_base - bar2_height - 10,
                text=str(values[1]),
                fill="black"
            )

            # add the hour label below the bars.
            self.canvas.create_text(
                (bar1_x1 + bar2_x2) / 2,
                y_base + 15,
                text=label,
                fill="black"
            )

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate the color coding for the two junctions.
        """
        legend_x = 1450 - 50 - 100  # position the legend on the right side of the canvas
        legend_y = 50  # position the legend near the top of the canvas
        legend_spacing = 40  # vertical spacing between legend items

        # create legend entry for Elm Avenue/Rabbit Road junction
        self.canvas.create_rectangle(
            legend_x, legend_y,
            legend_x + 20, legend_y + 20,
            fill="#42daf5"
        )
        self.canvas.create_text(
            legend_x + 30, legend_y + 10,
            text="Elm Avenue/Rabbit Road",
            anchor="w", fill="black"
        )

        # create legend entry for Hanley Highway/Westway junction
        self.canvas.create_rectangle(
            legend_x, legend_y + legend_spacing,
            legend_x + 20, legend_y + 20 + legend_spacing,
            fill="#90EE90"
        )
        self.canvas.create_text(
            legend_x + 30, legend_y + 10 + legend_spacing,
            text="Hanley Highway/Westway",
            anchor="w", fill="black"
        )

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram window.
        """
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files

class MultiCSVProcessor:

    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """

        # initialize storage for current session's data
        self.current_data = None  # stores the currently loaded traffic data
        self.selected_date = None # stores the date of the current dataset

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """

        data = defaultdict(lambda: [0, 0])  # initialize counts for both junctions
        selected_date = None # track the date of the dataset

        # read and process the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader: # Set the selected date from csv file
                # ensure we're processing data for the same date
                if row['Date'] == selected_date or selected_date is None:
                    selected_date = row['Date']

                time_of_day = row.get('timeOfDay', '')

                # extract hour from time string, skip invalid entries 
                if time_of_day:
                    try:
                        hour = time_of_day.split(":")[0]
                    except IndexError:
                        continue
                else:
                    continue

                # count vehicles for each junction
                junction = row['JunctionName']
                if junction == "Elm Avenue/Rabbit Road":
                    data[hour][0] += 1
                elif junction == "Hanley Highway/Westway":
                    data[hour][1] += 1

        # store processed data in instance variables
        self.current_data = data
        self.selected_date = selected_date

        return data, selected_date

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """

        self.current_data = None
        self.selected_date = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """

        # get valid date input from user
        valid_date = w2121364_cw_part_A_B_C.validate_date_input()
        file_name = f"traffic_data{valid_date}.csv"
        # process the CSV file and display results
        outcomes = w2121364_cw_part_A_B_C.process_csv_data(file_name)

        if outcomes:
            # display and save results, then create histogram
            w2121364_cw_part_A_B_C.display_outcomes(outcomes)
            w2121364_cw_part_A_B_C.save_results_to_file(outcomes)
            data, selected_date = self.load_csv_file(file_name)
            print (f"Histogram for {selected_date} will be created \nPlease close histogram window to continue")
            app = HistogramApp(data, selected_date)
            app.run()
            print ("Histogram closed successfully")

        return w2121364_cw_part_A_B_C.validate_continue_input()

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """

        while True:
            should_continue = self.handle_user_interaction()
            if not should_continue:
                break
            self.clear_previous_data()

if __name__ == "__main__":
    """
    Main program 
    """

    processor = MultiCSVProcessor()
    processor.process_files()