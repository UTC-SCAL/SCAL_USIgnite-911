import pandas
import os, sys
from datetime import datetime
from darksky import forecast


def find_cred(service):
    file = "../Excel & CSV Sheets/login.csv"
    if os.path.exists(file):
        with open(file, "r") as file:
            lines = file.readlines()
            if service in lines[0]:
                cred = lines[0].split(",")[1]
                # print(cred)
            if service in lines[1]:
                cred = str(lines[1].split(",")[1]) + "," + str(lines[1].split(",")[2])
                # print(cred)
                    # logins[username] = password
    return cred


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# This code fetches the daily mins, maxes, and average temperatures for each grid block #
# These files hold the days for the years 2017 and 2018
dayHolder_2017 = pandas.read_excel("../Excel & CSV Sheets/New Data Files/Day Holder 2017.xlsx")
dayHolder_2018 = pandas.read_excel("../Excel & CSV Sheets/New Data Files/Day Holder 2018.xlsx")
# Our accidents
# calldata = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018.csv")
# Grid Block center point coordinates
grid_coords = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/CenterPoints OS Layout.csv")

# First, we'll need to find the daily temperature for every grid block we use
# Grid Blocks represents the files related to the standard grid layout we started with, while grid os blocks
# represents the files related to the oriented small version of the grid layout
# Grid Blocks 0 - 275
# Grid OS Blocks 0 - 456
# grid_section1 = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Daily Avg Temps.csv")
# # Grid Blocks 276 - 550
# # Grid OS Blocks 457 - 912
# # grid_section2 = pandas.read_csv("../")
# # Grid Blocks 551 - 825
# # Grid OS Blocks 913 - 1368
# # grid_section3 = pandas.read_csv("../")
# # Grid Blocks 826 - 1099
# # Grid OS Blocks 1369 - 1826
# # grid_section4 = pandas.read_csv("../")

# # Set the date column as a string for easy splitting
# # Change the number after the section in the name to correspond to the file you read in
# grid_section1.Date = grid_section1.Date.astype(str)

# # The key for using DarkSky API
# key = find_cred("darksky")
# # Set the range of column values you want to go over
# for i in range(440, 457):
#     print("Finding data for grid block ", i)
#     # Use the i value to make a string for the current column name in grid blocks section
#     col_name = "Block_" + str(i)
#     grid_section1[col_name] = grid_section1[col_name].astype(str)
#     for k, info in enumerate(grid_section1.values):
#         print(k)
#         # All variables are blank-of-accident, thus year is yoa.
#         doa = grid_section1.Date.values[k]
#         yoa = int(doa.split('/')[2])
#         moa = int(doa.split('/')[0])
#         dayoa = int(doa.split('/')[1])
#         lat = grid_coords.Center_Lat.values[i]  # Center latitude point for current grid block
#         long = grid_coords.Center_Long.values[i]  # Center longitude point for current grid block
#         # The following line needs to have this format:
#         # Since we're using the daily method of dark sky, the time doesn't matter,
#         # but it still needs to be formatted like this
#         t = datetime(yoa, moa, dayoa, 0, 0, 0).isoformat()
#         call = key, lat, long
#         forecastcall = forecast(*call, time=t)
#         # try:
#         # Daily data, which requires individual try/except statements, otherwise the code crashes for some reason
#         for j, value2 in enumerate(forecastcall.daily):
#             try:
#                 temp_max = value2.temperatureMax
#             except:
#                 temp_max = -1000
#             try:
#                 temp_min = value2.temperatureMin
#             except:
#                 temp_min = -1000
#             temp_avg = (temp_max + temp_min) / 2
#             # Save the numbers in this format so they can all stay in the same cell for easy data saving
#             # For later use, all you'd need to do is split by |
#             grid_section1[col_name].values[k] = str(temp_max) + "|" + str(temp_min) + "|" + str(temp_avg)
#     # Save each time a column finishes to avoid having to redo work if the code stops for some reason
#     grid_section1.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Daily Avg Temps2.csv")
# # A final save
# grid_section1.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Daily Avg Temps2.csv")

# The following code is getting the monthly averages for each grid block
# These files have the daily min, max, and average temperatures for each grid block
# Grid Blocks represents the files related to the standard grid layout we started with, while grid os blocks
# represents the files related to the oriented small version of the grid layout
# Grid Blocks 0 - 275
# Grid OS Blocks 0 - 456
# grid_section1 = pandas.read_csv("../")
# Grid Blocks 276 - 550
# Grid OS Blocks 457 - 912
# grid_section2 = pandas.read_csv("../")
# Grid Blocks 551 - 825
# Grid OS Blocks 913 - 1368
# grid_section3 = pandas.read_csv("../")
# Grid Blocks 826 - 1099
# Grid OS Blocks 1369 - 1826
# grid_section4 = pandas.read_csv("../")

# These will contain the monthly averages per grid block
# Grid Blocks 0 - 275
# Grid OS Blocks 0 - 456
grid_averages = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Monthly Avg Temps.csv")
grid_section = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Daily Avg Temps.csv")

# Grid Blocks 276 - 550
# Grid OS Blocks 457 - 912
# grid_averages = pandas.read_csv("../")
# Grid Blocks 551 - 825
# Grid OS Blocks 913 - 1368
# grid_averages = pandas.read_csv("../")
# Grid Blocks 826 - 1099
# Grid OS Blocks 1369 - 1826
# grid_averages = pandas.read_csv("../")

# Here, you will need to change the range values based on what file you are reading in
# You can find each file's respective grid block numbers above each file as a comment
# Remember to have the range values be (start, end + 1)
for i in range(456,457):
    # Use the i value to make a string for the current column name in grid blocks section
    col_name = "Block_" + str(i)
    print("Finding data for grid block ", i)
    for o, values in enumerate(grid_section.values):
        print(o)
        grid_averages[col_name] = grid_averages[col_name].astype(float)
        year = int(grid_section.Date.values[o].split('/')[2])
        month = int(grid_section.Date.values[o].split('/')[0])
        daily_avg = float(grid_section[col_name].values[o].split("|")[2])
        for j, avg_values in enumerate(grid_averages.values):
            if year == grid_averages.Year.values[j] and month == grid_averages.Month.values[j]:
                grid_averages[col_name].values[j] += daily_avg
    # You will need to change the name of the file based on what file you are reading in
    # Ex, if you are reading in file Grid Blocks S4 Monthly Averages, you will need to change the save name to that
    grid_averages.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Monthly Avg Temps.csv")
grid_averages.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Monthly Avg Temps.csv")




# This code reads in the previously made files and gets the average temp for each month
# This is just for simplicity, as going through doing this averaging for every single grid block would take forever
# Aint nobody got time for that
# Read in the monthly averages file you want to get the averages for, and change the values in the for in range below
# average_file = pandas.read_csv("../")
# # Set the range of column values you want to go over
# for i in range(,):
#     print("Averaging for block ", i)
#     # Use the i value to make a string for the current column name in grid blocks section
#     col_name = "Block_" + str(i)
#     for k, info in enumerate(average_file.values):
#         month = average_file.Month.values[k]
#         if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
#             average_file[col_name].values[k] = round(average_file[col_name].values[k]/31.00, 2)
#         elif month == 2:
#             average_file[col_name].values[k] = round(average_file[col_name].values[k]/28.00, 2)
#         else:
#             average_file[col_name].values[k] = round(average_file[col_name].values[k]/30.00, 2)
# average_file.to_csv("../")