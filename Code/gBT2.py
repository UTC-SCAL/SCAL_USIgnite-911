import pandas
import os, sys
import random
path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


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


def get_negatives_master(calldata, compare):
    # Blank csv file for formatting purposes and easily saving negative samples
    negative_samples = pandas.read_csv(
        "../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/Blank Negative Samples Form.csv", sep=",")
    # The center points for our grid blocks for the current grid layout we are using
    center_points = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/CenterPoints Ori Layout.csv", sep=",")
    # This contains the information of each grid block, such as road count and grid column number
    grid_info = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Info.csv")

    # Select the range of grid blocks to use for getting new grid blocks
    # This is based on the column length of the center point's ORIG_FID column, which is the block ID number
    block_number = range(0, len(center_points.ORIG_FID))

    # Two files to hold the days in years 2017 and 2018
    # They are separated due to the nature of negative samples by date
    day_holder2017 = pandas.read_excel(
        "../Excel & CSV Sheets/New Data Files/Day Holder 2017.xlsx")
    day_holder2018 = pandas.read_excel(
        "../Excel & CSV Sheets/New Data Files/Day Holder 2018.xlsx")

    # A negative sample location
    neg_loc = 0  # Used for positioning

    # Cast these columns as strings for easy manipulation and comparison
    calldata.Date = calldata.Date.astype(str)
    day_holder2017.Date = day_holder2017.Date.astype(str)
    day_holder2018.Date = day_holder2018.Date.astype(str)

    # Lists to hold the values for each type of changed variable that shouldn't be chosen again
    # Ex: The block_list holds the block numbers that have been selected in the current g-loop so we don't
    # choose the same grid block again
    block_list = []
    date_list_2017 = []
    date_list_2018 = []
    hour_list = []

    # Our main for loop: iterates through our accidents
    for j, values in enumerate(calldata.values):
        print(j)
        # Make a copy of the current calldata row for manipulation
        # This copy helps us avoid having to make changes to the original data
        # Make a basic copy of the row we are on, then save it as a single row dataframe
        line_copy = calldata.values[j].copy()
        line_copy = list(line_copy)
        copy_calldata = pandas.DataFrame([line_copy], columns=calldata.columns.values)

        # Append the current block (the first block for the main loop) to the list of blocks that shouldn't be chosen
        # for finding negative samples
        current_block = calldata.Grid_Block.values[j]
        block_list.append(current_block)

        # Append the current date (the first date for the main loop) to the list of dates that shouldn't be chosen
        # for finding negative samples
        # Based on the year of the accident's record, we will use the according file
        # This is because when we find a new date for a negative sample, we can only choose new dates from the same year
        # as the original positive sample
        original_accident_year = int(calldata.Date.values[j].split("-")[0])
        if original_accident_year == 2017:
            doa = calldata.Date.values[j]
            row_num = day_holder2017.loc[day_holder2017['Date'] == doa].index[0]
            date_list_2017.append(row_num)
        elif original_accident_year == 2018:
            doa = calldata.Date.values[j]
            row_num = day_holder2018.loc[day_holder2018['Date'] == doa].index[0]
            date_list_2018.append(row_num)

        # Append the current hour (the first hour for the main loop) to the list of dates that shouldn't be chosen
        # for finding negative samples
        current_hour = calldata.Hour.values[j]
        hour_list.append(current_hour)

        # This is the g-loop, where the process of finding a negative sample for our current accident record is repeated
        # This is repeated 9 times so we have a split of roughly %10 positive samples, and %90 negative samples
        for g in range(0, 9):
            # Grid Block Changer #
            r_grid = [x for x in block_number if x not in block_list]
            rand_num = random.choice(r_grid)
            new_block = center_points.ORIG_FID.values[rand_num]
            copy_calldata.Grid_Block.values[0] = new_block
            block_list.append(new_block)

            # Date Changer #
            accident_year = int(copy_calldata.Date.values[0].split("-")[0])
            if accident_year == 2017:
                days = range(0, len(day_holder2017.Date))

                r_date = [y for y in days if y not in date_list_2017]
                copy_calldata.Date.values[0] = day_holder2017.Date.values[random.choice(r_date)]
                row_num = day_holder2017.loc[day_holder2017['Date'] == copy_calldata.Date.values[0]].index[0]
                date_list_2017.append(row_num)
            elif accident_year == 2018:
                days = range(0, len(day_holder2018.Date))

                r_date = [y for y in days if y not in date_list_2018]
                copy_calldata.Date.values[0] = day_holder2018.Date.values[random.choice(r_date)]
                row_num = day_holder2018.loc[day_holder2018['Date'] == copy_calldata.Date.values[0]].index[0]
                date_list_2018.append(row_num)

            # Hour Changer #
            hours = range(0, 24)
            r = [x for x in hours if x not in hour_list]  # A list of numbers without n
            new_hour = random.choice(r)
            hour_list.append(new_hour)
            copy_calldata.Hour.values[0] = new_hour

            # Set a boolean value for finding matches
            # If a match is found, the value is set to false and the for loop below is broken
            # This helps us save time for searching for matches, since if we have a single match we move onto the next
            # negative sampling
            no_matches = True
            for n, checks in enumerate(compare.values):  # Iterates through copy_calldata checking for a match with i
                if n == j:
                    pass
                else:
                    if copy_calldata.Hour.values[0] == compare.Hour.values[n] and \
                                copy_calldata.Date.values[0] is compare.Date.values[n]\
                            and copy_calldata.Grid_Block.values[0] is compare.Grid_Block.values[n]:
                        no_matches = False
                        break
            # If the boolean value for matches is true, then we save the appropriate data to our negative samples
            # data frame
            if no_matches is True:
                # These values stay the same between copy_calldata and the negative samples
                negative_samples.loc[neg_loc, "Grid_Block"] = copy_calldata.Grid_Block.values[0]
                negative_samples.loc[neg_loc, "Accident"] = 0
                negative_samples.loc[neg_loc, "Date"] = copy_calldata.Date.values[0]
                negative_samples.loc[neg_loc, "Hour"] = copy_calldata.Hour.values[0]
                negative_samples.loc[neg_loc, "Time"] = copy_calldata.Time.values[0]
                negative_samples.loc[neg_loc, "Weekday"] = copy_calldata.Weekday.values[0]
                # Get the row number to use in the centerpoint file based on the grid block of the negative sample
                # The basic idea here is to match row numbers based on grid block numbers
                center_row_num = center_points.loc[center_points['ORIG_FID'] == copy_calldata.Grid_Block.values[0]].index[0]
                negative_samples.loc[neg_loc, "Center_Lat"] = center_points.Center_Lat.values[center_row_num]
                negative_samples.loc[neg_loc, "Center_Long"] = center_points.Center_Long.values[center_row_num]
                # Get the row number to use in grid info based on the grid block of the negative sample
                # The basic idea here is to match row numbers based on grid block numbers
                info_row_num = grid_info.loc[grid_info["ORIG_FID"] == copy_calldata.Grid_Block.values[0]].index[0]
                negative_samples.loc[neg_loc, "Grid_Col"] = grid_info.loc[info_row_num, "Col_Num"]
                negative_samples.loc[neg_loc, "Grid_Row"] = grid_info.loc[info_row_num, "Row_Num"]
                negative_samples.loc[neg_loc, "Highway"] = grid_info.loc[info_row_num, "Highway"]
                negative_samples.loc[neg_loc, "Land_Use_Mode"] = grid_info.loc[info_row_num, "Land_Use_Mode"]
                negative_samples.loc[neg_loc, "Road_Count"] = grid_info.loc[info_row_num, "Road_Count"]
                neg_loc = neg_loc + 1
        # Delete the copies made earlier to save memory space
        del copy_calldata
        del line_copy
        # Reset the do-not-use lists for the new accident record we'll be using
        block_list = []
        date_list_2017 = []
        date_list_2018 = []
        hour_list = []
        if j % 1000 == 0:
            negative_samples.to_csv\
                ("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS Master List 2.csv")

    negative_samples.to_csv\
        ("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS Master List 2.csv")


accidents = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GOD Section 2.csv")
compare_data = pandas.read_csv\
    ("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GOD 2017+2018 Accidents.csv")
get_negatives_master(accidents, compare_data)
