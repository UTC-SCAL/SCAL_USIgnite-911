import pandas
import os, sys

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

grid_data = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018_DailyTemp.csv")
# First, we'll need to find the daily temperature for every grid block we use
# Grid Blocks 0 - 275
grid_section1 = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S1 Monthly Avg Temps2.csv")
# Grid Blocks 276 - 550
grid_section2 = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S2 Monthly Avg Temps2.csv")
# Grid Blocks 551 - 825
grid_section3 = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S3 Monthly Avg Temps2.csv")
# Grid Blocks 826 - 1099
grid_section4 = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Blocks S4 Monthly Avg Temps2.csv")

# These 4 casting lines are only needed for finding daily relative temperature
# grid_section1.Date = grid_section1.Date.astype(str)
# grid_section2.Date = grid_section2.Date.astype(str)
# grid_section3.Date = grid_section3.Date.astype(str)
# grid_section4.Date = grid_section4.Date.astype(str)
grid_data.Date = grid_data.Date.astype(str)
grid_data.Temperature = grid_data.Temperature.astype(float)

# # This for loop is for finding daily relative temperature
# for i, value in enumerate(grid_data.values):
#     print(i)
#     # Use the i value to make a string for the current column name in grid blocks section
#     # Based on what the current accident's grid block number is, the appropriate grid_section file will be used
#     if 0 <= grid_data.Grid_Block.values[i] <= 456:
#         # this is the column of the grid section file
#         col_name = "Block_" + str(grid_data.Grid_Block.values[i])
#         # Set the column as a string for easy splitting
#         grid_section1[col_name] = grid_section1[col_name].astype(str)
#         # this is the row of the grid section file
#         # this gets the row number based on the value passed to it, which is the date from the current accident
#         row_num = grid_section1.loc[grid_section1['Date'] == grid_data.Date.values[i]].index[0]
#         # get relative temp from the grid section file
#         # in the files, there are 3 values in each cell (temp max, temp min, relative temp), all separated by a |
#         # use the string split function to get the relative temperature
#         relative_temp = grid_data.Temperature.values[i] - float(grid_section1.loc[row_num, col_name].split('|')[2])
#         # save the relative temperature for the current accident
#         grid_data.Daily_Relative_Temp.values[i] = relative_temp
#     elif 457 <= grid_data.Grid_Block.values[i] <= 912:
#         col_name = "Block_" + str(grid_data.Grid_Block.values[i])

#         grid_section2[col_name] = grid_section2[col_name].astype(str)
#         row_num = grid_section2.loc[grid_section2['Date'] == grid_data.Date.values[i]].index[0]

#         relative_temp = grid_data.Temperature.values[i] - float(grid_section2.loc[row_num, col_name].split('|')[2])
#         grid_data.Daily_Relative_Temp.values[i] = relative_temp
#     elif 913 <= grid_data.Grid_Block.values[i] <= 1368:
#         col_name = "Block_" + str(grid_data.Grid_Block.values[i])

#         grid_section3[col_name] = grid_section3[col_name].astype(str)
#         row_num = grid_section3.loc[grid_section3['Date'] == grid_data.Date.values[i]].index[0]

#         relative_temp = grid_data.Temperature.values[i] - float(grid_section3.loc[row_num, col_name].split('|')[2])
#         grid_data.Daily_Relative_Temp.values[i] = relative_temp
#     elif 1369 <= grid_data.Grid_Block.values[i] <= 1825:
#         col_name = "Block_" + str(grid_data.Grid_Block.values[i])

#         grid_section4[col_name] = grid_section4[col_name].astype(str)
#         row_num = grid_section4.loc[grid_section4['Date'] == grid_data.Date.values[i]].index[0]

#         relative_temp = grid_data.Temperature.values[i] - float(grid_section4.loc[row_num, col_name].split('|')[2])
#         grid_data.Daily_Relative_Temp.values[i] = relative_temp

# grid_data.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018_DailyTemp.csv")
# exit()
# This for loop is for finding monthly relative temperature
for i, value in enumerate(grid_data.values):
    print(i)
    # Use the i value to make a string for the current column name in grid blocks section
    # Based on what the current accident's grid block number is, the appropriate grid_section file will be used
    if 0 <= grid_data.Grid_Block.values[i] <= 456:
        # This is the column name of we'll use to match the grid average file and the grid data file
        col_name = "Block_" + str(grid_data.Grid_Block.values[i])

        # Get the grid data's month and year for comparison purposes
        grid_year = int(grid_data.Date.values[i].split("/")[2])
        grid_month = int(grid_data.Date.values[i].split("/")[0])

        # Get the row number based on if the year and month match between the two files
        row_num = grid_section1.loc[(grid_section1['Year'] == grid_year) &
                                    (grid_section1['Month'] == grid_month)].index[0]

        # Get the relative temperature and save it to the current grid data entry
        relative_temp = grid_data.Temperature.values[i] - float(grid_section1.loc[row_num, col_name])
        grid_data.Monthly_Relative_Temp.values[i] = relative_temp
    elif 457 <= grid_data.Grid_Block.values[i] <= 912:
        col_name = "Block_" + str(grid_data.Grid_Block.values[i])

        grid_year = int(grid_data.Date.values[i].split("/")[2])
        grid_month = int(grid_data.Date.values[i].split("/")[0])

        row_num = grid_section2.loc[(grid_section2['Year'] == grid_year) &
                                    (grid_section2['Month'] == grid_month)].index[0]

        relative_temp = grid_data.Temperature.values[i] - float(grid_section2.loc[row_num, col_name])
        grid_data.Monthly_Relative_Temp.values[i] = relative_temp
    elif 913 <= grid_data.Grid_Block.values[i] <= 1368:
        col_name = "Block_" + str(grid_data.Grid_Block.values[i])

        grid_year = int(grid_data.Date.values[i].split("/")[2])
        grid_month = int(grid_data.Date.values[i].split("/")[0])

        row_num = grid_section3.loc[(grid_section3['Year'] == grid_year) &
                                    (grid_section3['Month'] == grid_month)].index[0]

        relative_temp = grid_data.Temperature.values[i] - float(grid_section3.loc[row_num, col_name])
        grid_data.Monthly_Relative_Temp.values[i] = relative_temp
    elif 1368 <= grid_data.Grid_Block.values[i] <= 1825:
        col_name = "Block_" + str(grid_data.Grid_Block.values[i])

        grid_year = int(grid_data.Date.values[i].split("/")[2])
        grid_month = int(grid_data.Date.values[i].split("/")[0])

        row_num = grid_section4.loc[(grid_section4['Year'] == grid_year) &
                                    (grid_section4['Month'] == grid_month)].index[0]

        relative_temp = grid_data.Temperature.values[i] - float(grid_section4.loc[row_num, col_name])
        grid_data.Monthly_Relative_Temp.values[i] = relative_temp
grid_data.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018_AllTemp.csv")