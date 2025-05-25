#Author: D. W. Yeheni Kaveesha Dodanwela
#Date: 23.12.2024
#Student ID: 20241486 (IIT Number) | w2121364 (UoW Number)

import csv

# Task A: Input Validation

def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    # check if the given year is a leap year
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    # keep asking for the day until a valid one is entered
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format DD: "))
            if 1 <= day <= 31:  # check range for days
                break
            else:
                print("Out of range - Days must be in the range 1 to 31.")
        except ValueError:
            print("Integer required")

    # keep asking for the month until a valid one is entered
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12: # check range for months

                # checking if the entered day fits within entered month
                if month in {1, 3, 5, 7, 8, 10, 12} and 1 <= day <= 31:
                    break
                elif month in {4, 6, 9, 11} and 1 <= day <= 30:
                    break
                elif month == 2:
                    if 1 <= day <= 29:
                        break
                    else:
                        print(f"Entered month can not have {day} days")
                else:
                    print(f"Entered month can not have {day} days")
            else:
                print("Out of range - Months must be in the range 1 to 12.")
        except ValueError:
            print("Integer required")

    # keep asking for the year until a valid one is entered
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:# check range of years

                # additional validation for february in leap years
                if is_leap_year(year):
                    if month == 2:
                        if 1 <= day <= 29:
                            break
                    else:
                        break
                else:
                    if month == 2:
                        if 1 <= day <= 28:
                            break
                        else:
                            print("February can have 29 days only in a leap year - Check the entered year again.")
                    else:
                        break
            else:
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required")

    # format the valid date as DD MM YYYY and return it
    date = f"{day:02d}{month:02d}{year}"
    return date

# Task E: Code loops to load and processes a new dataset 
def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset
    """
    # ask the user if they want to process another file and convert input to lowercase to handle both capital and simple letters
    continue_choice = input("Do you want to select another data file for a different date? Y/N: ").strip().lower()
    if continue_choice == 'y': # if the user enters "y", ask for a new date
        return True
    elif continue_choice == 'n': # if the user enters "n", end the program
        print("End of run")
        return False
    else:
        print("Invalid input. Please enter 'Y' or 'N'") # if the input is invalid, ask the user again
        return validate_continue_input()

# Task B: Processed Outcomes

def process_csv_data(file_name):
    """
    Processes the CSV data for the selected date and returns the results
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    try:
        with open(file_name, 'r') as file: # open and read the CSV file
            reader = csv.reader(file) # open, read and auto close the CSV file
            header = next(reader) # Skip the first row beacause it's the header

            try:
                # find the required column indexes by header name
                vehicle_type_index = header.index("VehicleType")
                electric_status_index = header.index("elctricHybrid")
                junction_name_index = header.index("JunctionName")
                travel_Direction_out_index = header.index("travel_Direction_out")
                travel_Direction_in_index = header.index("travel_Direction_in")
                time_of_day_index = header.index("timeOfDay")
                vehicle_speed_index = header.index("VehicleSpeed")
                speed_limit_index = header.index("JunctionSpeedLimit")
                weather_conditions_index = header.index("Weather_Conditions")

            except ValueError:  
                # if any of the required columns are not found, print an error
                print("Required columns not found.")
                return None

            # print the selected file name
            print(f"***************************\ndata file selected is {file_name}\n***************************")

            # Initialize counters to track different statistics
            line_count = 0
            truck_count = 0
            electric_vehicles_count = 0
            two_wheeled_vehicles_count = 0
            busses_count = 0
            vehicles_passing_straight_count = 0
            bicycles_count = 0
            hours_count = set() # stores unique hour values extracted from the CSV file to avoid duplicates
            over_speed_limit_count = 0
            total_vehicles_elmavenue_rabbitroad = 0
            total_vehicles_hanleyhighway_westway = 0
            scooters_elmavenue_rabbitroad = 0
            hanley_highway_hourly_count = {} # dictionary that tracks the number of vehicles passing through the junction
            # Key: hour of the day
            # Value: count of vehicles that passed during that hour
            rainy_hours_count = 0
            rainy_hours = set() # set saves rainy hour only once from the csv file

            # Process each row in the CSV file
            for row in reader:
                line_count += 1

                # Extract the values from each row
                vehicle_type = row[vehicle_type_index].strip()
                electric_status = row[electric_status_index].strip().lower()
                junction_name = row[junction_name_index].strip()
                travel_Direction_out = row[travel_Direction_out_index].strip()
                travel_Direction_in = row[travel_Direction_in_index].strip()
                time_of_day = row[time_of_day_index].strip()
                vehicle_speed = int(row[vehicle_speed_index].strip())
                speed_limit = int(row[speed_limit_index].strip())
                weather_conditions = row[weather_conditions_index].strip()

                # counting the number of trucks
                if ("Truck" in vehicle_type):
                    truck_count += 1
                
                # counting the number of electric vehicles
                if ("true" in electric_status):
                    electric_vehicles_count += 1

                # count the number of two wheeled vehicles
                if (any(vehicle in vehicle_type for vehicle in ["Bicycle", "Motorcycle", "Scooter"])):
                    two_wheeled_vehicles_count += 1

                # counting the number of buses going North at the elm avenue/rabbit road junction
                if ("Elm Avenue/Rabbit Road" in junction_name and "N" in travel_Direction_out and "Buss" in vehicle_type):
                    busses_count += 1

                # counting vehicles traveling straight
                if (travel_Direction_out == travel_Direction_in):
                    vehicles_passing_straight_count += 1

                # calculating the average number of bicycles per hour
                if ("Bicycle" in vehicle_type):
                    bicycles_count += 1
                hour = time_of_day.split(":")[0]
                hours_count.add(hour)
                if (hours_count):
                        avg_bicycles_per_hour = round(bicycles_count / len(hours_count))
                else:
                        avg_bicycles_per_hour = 0

                # Counting vehicles exceeding the speed limit
                if (vehicle_speed > speed_limit):
                    over_speed_limit_count += 1

                # calculating the number of scooters passing through the elm avenue/rabbit road junction
                if (junction_name == "Elm Avenue/Rabbit Road"):
                    total_vehicles_elmavenue_rabbitroad += 1
                    if ("Scooter" in vehicle_type):
                        scooters_elmavenue_rabbitroad += 1

                # calculating the number of vehicles passing through the hanley highway/westway junction and tracking peak hours
                if (junction_name == "Hanley Highway/Westway"):
                    hour = time_of_day.split(":")[0]
                    if (hour not in hanley_highway_hourly_count):
                        hanley_highway_hourly_count[hour] = 0
                    hanley_highway_hourly_count[hour] += 1
                    total_vehicles_hanleyhighway_westway += 1

                # Tracking rainy hours
                if (any(condition in weather_conditions for condition in ["Light Rain", "Heavy Rain"])):
                    hour = time_of_day.split(":")[0]
                    rainy_hours.add(hour)
                    rainy_hours_count = len(rainy_hours)

            # calculating the percentage of trucks in total vehicles
            if (line_count > 0):
                percentage_of_trucks = (truck_count / line_count) * 100
                percentage_of_trucks_rounded = round(percentage_of_trucks)

            # calculating the percentage of scooters at the elm avenue/rabbit road junction        
            if (total_vehicles_elmavenue_rabbitroad > 0):
                scooters_percentage_elmavenue_rabbitroad = (scooters_elmavenue_rabbitroad / total_vehicles_elmavenue_rabbitroad) * 100
                scooters_percentage_elmavenue_rabbitroad_rounded =  int (scooters_percentage_elmavenue_rabbitroad)
            else:
                scooters_percentage_elmavenue_rabbitroad_rounded = 0

            # calculating the number of vehicles passing through the hanley highway/westway junction and tracking peak hours
            if (hour not in hanley_highway_hourly_count):
                hanley_highway_hourly_count[hour] = 0
                hanley_highway_hourly_count[hour] += 1
                total_vehicles_hanleyhighway_westway += 1
            if (hanley_highway_hourly_count):
                peak_hour_count = max(hanley_highway_hourly_count.values())
            else:
                peak_hour_count = 0
            peak_hours = [hour for hour, count in hanley_highway_hourly_count.items() if count == peak_hour_count]
            if (peak_hours): 
                for hour in peak_hours:
                    next_hour = int(hour) + 1

            # results save as a list
            results = [
                f"The total number of vehicles recorded for this date is {line_count}",
                f"The total number of trucks recorded for this date is {truck_count}",
                f"The total number of electric vehicles for this date is {electric_vehicles_count}",
                f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles_count}",
                f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {busses_count}",
                f"The total number of Vehicles through both junctions not turning left or right is {vehicles_passing_straight_count}",
                f"The percentage of total vehicles recorded that are trucks for this date is {percentage_of_trucks_rounded}%",
                f"The average number of Bikes per hour for this date is {avg_bicycles_per_hour}",
                f"The total number of Vehicles recorded as over the speed limit for this date is {over_speed_limit_count}",
                f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {total_vehicles_elmavenue_rabbitroad}",
                f"The total number of vehicles recorded through Hanley Highway/Westway junction is {total_vehicles_hanleyhighway_westway}",
                f"{scooters_percentage_elmavenue_rabbitroad_rounded}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
                f"The highest number of vehicles in an hour on Hanley Highway/Westway is {peak_hour_count}",
                f"The most vehicles through Hanley Highway/Westway were recorded between {hour}:00 and {next_hour}:00",
                f"The number of hours of rain for this date is {rainy_hours_count}"
            ]

            return results, file_name # returns the results and file name as a tuple
        
    # Handle the case where the specified file is not found
    except FileNotFoundError:
        print(f"File {file_name} not found. Please try again.")
        return None

def display_outcomes(outcomes):
    """
    Function to display the calculated outcomes.
    """
    if outcomes:
        # print each result from the outcomes to the screen
        for result in outcomes[0]:  # results are the 0th element, file name is the first element
            print(result)

# Task C: Save Results to Text File

def save_results_to_file(outcomes):
    """
    Saves the processed results to a text file and append if needed.
    """
    if outcomes:
        results, file_name = outcomes
        with open("results.txt", "a") as results_file:
            results_file.write(f"data file selected is {file_name}\n")
            for result in results:
                results_file.write(result + "\n") # write each result outcome to the file
            results_file.write("\n***************************\n") # a separator to mark the end of the results

        print("\nResults have been saved to results.txt.\n") # notify the user that the results have been saved

    
if __name__ == "__main__":
    """
    Main program execution starts here
    """
    continue_program = True # boolean value to validate continue input
    
    while continue_program: 
        valid_date = validate_date_input() # get a valid date input from the user
        file_name = f"traffic_data{valid_date}.csv" # generate the CSV file name based on the valid date
        outcomes = process_csv_data(file_name) # process the CSV file and get the outcomes
        
        if outcomes:
            display_outcomes(outcomes)  # display the results to the user
            save_results_to_file(outcomes) # save the results to a file
        
        continue_program = validate_continue_input() # ask the user if they want to continue or exit the program (if validate_continue_input is false program will exit)

# if you have been contracted to do this assignment please do not remove this line
