import pandas
import os, sys
import random
import time
from datetime import datetime
import feather
path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def find_cred(service):
    file = "../Ignore/logins.csv"
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

def get_negatives_master_random(calldata, compare, name):
    # Blank csv file for formatting purposes and easily saving negative samples
    negative_samples = pandas.read_csv(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/Negative Sample Template.csv", sep=",")
    # The center points for our grid blocks for the current grid layout we are using
    # center_points = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/Hex_GridInfo.csv", sep=",")
    # This contains the information of each grid block, such as road count and grid column number
    grid_info = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Hex_Grid/HexGridInfo.csv")

    # Select the range of grid blocks to use for getting new grid blocks
    # This is based on the column length of the center point's grid_num column, which is the block ID number
    block_number = range(1, 695)

    # The following file(s) are used as an easy way to access the dates in certain years
    # They are separated due to the nature of negative samples by date
    day_holder2017 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2017.xlsx")
    day_holder2018 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2018.xlsx")
    day_holder2019 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2019.xlsx")

    # A negative sample location
    neg_loc = 0  # Used for positioning

    # Cast these columns as strings for easy manipulation and comparison
    calldata.Date = calldata.Date.astype(str)
    day_holder2017.Date = day_holder2017.Date.astype(str)
    day_holder2018.Date = day_holder2018.Date.astype(str)
    day_holder2019.Date = day_holder2019.Date.astype(str)

    # day_holder2017.Unix = day_holder2017.Unix.astype(int)
    # day_holder2018.Unix = day_holder2018.Unix.astype(int)
    # day_holder2019.Unix = day_holder2019.Unix.astype(int)
    calldata.Unix = calldata.Unix.astype(int)


    # Lists to hold the values for each type of changed variable that shouldn't be chosen again
    # Ex: The block_list holds the block numbers that have been selected in the current g-loop so we don't
    # choose the same grid block again
    block_list = []
    date_list_2017 = []
    date_list_2018 = []
    date_list_2019 = []
    hour_list = []
    # unix_list_2017 = []
    # unix_list_2018 = []
    # unix_list_2019 = []

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
        current_block = calldata.Grid_Num.values[j]
        block_list.append(current_block)

        # Append the current date (the first date for the main loop) to the list of dates that shouldn't be chosen
        # for finding negative samples
        # Based on the year of the accident's record, we will use the according file
        # This is because when we find a new date for a negative sample, we can only choose new dates from the same year
        # as the original positive sample
        original_accident_year = int(calldata.Date.values[j].split("-")[0])
        if original_accident_year == 2019:
            doa = calldata.Date.values[j]
            # row_num = day_holder2019.loc[day_holder2019['Date'] == doa]
            # dateValue = row_num.Date.value[0]
            date_list_2019.append(doa)
            # uoa = calldata.Unix.values[j]
            # row_num = day_holder2019.loc[day_holder2019["Unix"] == uoa].index[0]
            # unix_list_2019.append(row_num)
        elif original_accident_year == 2018:
            doa = calldata.Date.values[j]
            # row_num = day_holder2019.loc[day_holder2019['Date'] == doa]
            # dateValue = row_num.Date.value[0]
            date_list_2019.append(doa)
            # uoa = calldata.Unix.values[j]
            # row_num = day_holder2018.loc[day_holder2019["Unix"] == uoa].index[0]
            # unix_list_2018.append(row_num)
        elif original_accident_year == 2017:
            doa = calldata.Date.values[j]
            # row_num = day_holder2019.loc[day_holder2019['Date'] == doa]
            # dateValue = row_num.Date.value[0]
            date_list_2019.append(doa)

        # Append the current hour (the first hour for the main loop) to the list of hours that shouldn't be chosen
        # for finding negative samples
        current_hour = calldata.Hour.values[j]
        hour_list.append(current_hour)

        # This is the g-loop, where the process of finding a negative sample for our current accident record is repeated
        # This is repeated 9 times so we have a split of roughly %10 positive samples, and %90 negative samples
        for g in range(0, 9):
            # Grid Block Changer #
            # list of random grid numbers that aren't in our block_number list
            r_grid = [x for x in block_number if x not in block_list]
            # rand_num = random.choice(r_grid)
            # new_block = center_points.Grid_Num.values[rand_num]
            new_block = random.choice(r_grid)
            copy_calldata.Grid_Num.values[0] = new_block
            block_list.append(new_block)

            # Unix Changer #
            # accident_year = int(copy_calldata.Date.values[0].split("-")[0])
            # if accident_year == 2019:
            #     unix_times = range(0, len(day_holder2019.Unix))
            #
            #     r_unix = [y for y in unix_times if y not in unix_list_2019]
            #     copy_calldata.Unix.values[0] = day_holder2019.Unix.values[random.choice(r_unix)]
            #     row_num = day_holder2019.loc[day_holder2019['Unix'] == copy_calldata.Unix.values[0]].index[0]
            #     unix_list_2019.append(row_num)
            #     copy_calldata.Date.values[0] = day_holder2019.Date.values[row_num]
            #     copy_calldata.Hour.values[0] = day_holder2019.Hour.values[row_num]
            # elif accident_year == 2018:
            #     unix_times = range(0, len(day_holder2018.Unix))
            #
            #     r_unix = [y for y in unix_times if y not in unix_list_2018]
            #     copy_calldata.Unix.values[0] = day_holder2018.Unix.values[random.choice(r_unix)]
            #     row_num = day_holder2018.loc[day_holder2018['Unix'] == copy_calldata.Unix.values[0]].index[0]
            #     unix_list_2018.append(row_num)
            #     copy_calldata.Date.values[0] = day_holder2018.Date.values[row_num]
            #     copy_calldata.Hour.values[0] = day_holder2018.Hour.values[row_num]

            # Date Changer #
            accident_year = int(copy_calldata.Date.values[0].split("-")[0])
            if accident_year == 2019:
                # days = range(0, len(day_holder2019.Date))
                days = day_holder2019.Date.values

                r_date = [y for y in days if y not in date_list_2019]
                copy_calldata.Date.values[0] = random.choice(r_date)
                # row_num = day_holder2019.loc[day_holder2019['Date'] == copy_calldata.Date.values[0]].index[0]
                # date_list_2019.append(row_num)
                date_list_2019.append(copy_calldata.Date.values[0])
            elif accident_year == 2018:
                # days = range(0, len(day_holder2018.Date))
                days = day_holder2018.Date.values

                r_date = [y for y in days if y not in date_list_2018]
                copy_calldata.Date.values[0] = random.choice(r_date)
                # row_num = day_holder2018.loc[day_holder2018['Date'] == copy_calldata.Date.values[0]].index[0]
                # date_list_2018.append(row_num)
                date_list_2018.append(copy_calldata.Date.values[0])
            elif accident_year == 2017:
                # days = range(0, len(day_holder2017.Date))
                days = day_holder2017.Date.values

                r_date = [y for y in days if y not in date_list_2017]
                copy_calldata.Date.values[0] = random.choice(r_date)
                # row_num = day_holder2017.loc[day_holder2017['Date'] == copy_calldata.Date.values[0]].index[0]
                # date_list_2017.append(row_num)
                date_list_2017.append(copy_calldata.Date.values[0])

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
                            and copy_calldata.Grid_Num.values[0] is compare.Grid_Num.values[n]:
                    # if copy_calldata.Grid_Num.values[0] == compare.Grid_Num.values[n] and \
                    #         copy_calldata.Unix.values[0] is compare.Unix.values[n]:
                        no_matches = False
                        break
            # If the boolean value for matches is true, then we save the appropriate data to our negative samples
            # data frame
            if no_matches is True:
                # These values stay the same between copy_calldata and the negative samples
                negative_samples.at[neg_loc, "Accident"] = 0
                negative_samples.at[neg_loc, "Hour"] = copy_calldata.Hour.values[0]
                negative_samples.at[neg_loc, "Date"] = copy_calldata.Date.values[0]
                # Update the unix timestamp
                # Ensure date is formatted as such: yyyy-mm-d
                timestamp = str(copy_calldata.Date.values[0]) + " " + str(copy_calldata.Hour.values[0])
                negative_samples.at[neg_loc, "Unix"] = time.mktime(datetime.strptime(timestamp, "%Y-%m-%d %H").timetuple())
                # for each grid block
                negative_samples.at[neg_loc, "Grid_Num"] = copy_calldata.Grid_Num.values[0]
                # Get the row number to use in grid info based on the grid block of the negative sample
                # The basic idea here is to match row numbers based on grid block numbers
                info_row_num = grid_info.loc[grid_info["Grid_Num"] == copy_calldata.Grid_Num.values[0]].index[0]
                negative_samples.at[neg_loc, "Latitude"] = grid_info.Center_Lat.values[info_row_num]
                negative_samples.at[neg_loc, "Longitude"] = grid_info.Center_Long.values[info_row_num]
                negative_samples.at[neg_loc, "Join_Count"] = grid_info.Join_Count.values[info_row_num]
                negative_samples.at[neg_loc, "NBR_LANES"] = grid_info.NBR_LANES.values[info_row_num]
                negative_samples.at[neg_loc, "TY_TERRAIN"] = grid_info.TY_TERRAIN.values[info_row_num]
                negative_samples.at[neg_loc, "FUNC_CLASS"] = grid_info.FUNC_CLASS.values[info_row_num]
                negative_samples.at[neg_loc, "GRID_ID"] = grid_info.GRID_ID.values[info_row_num]

                neg_loc = neg_loc + 1
        # Delete the copies made earlier to save memory space
        del copy_calldata
        del line_copy
        # Reset the do-not-use lists for the new accident record we'll be using
        block_list = []
        date_list_2019 = []
        date_list_2018 = []
        date_list_2017 = []
        hour_list = []
        # if j % 500 == 0:
        #     negative_samples.to_csv("../Excel & CSV Sheets/Hex_Grid/Negative Sampling/NS 2017 P1 Done CP.csv")

    negative_samples.to_csv(name, index=False)


##Finding the 'true' negatives from a larger set. 
def cut_negatives(negatives, accidents):
    neg_loc=0
    negative_samples = pandas.DataFrame(columns=negatives.columns.values)
    for i, info in enumerate(negatives.values):
        print(i)
        no_matches=True
        for j, stuff in enumerate(accidents.values):
            if (negatives.DayFrame.values[i] == accidents.DayFrame.values[j]) and (negatives.WeekDay.values[i] == accidents.WeekDay.values[j]) and \
                (negatives.Grid_Num.values[i] == accidents.Grid_Num.values[j]):
                no_matches = False
                break
        if no_matches is True:
            negative_samples.loc[neg_loc] = negatives.values[i]
            neg_loc += 1
        if i % 500 == 0:
            negative_samples.to_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/NegativeSampling/NS True Master List 1.csv", index=False)
    print("True Negatives found :", neg_loc+1)
    negative_samples.to_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/NS True Master List 1.csv", index=False)

def get_negatives_master_gridfix(calldata, compare, name):
    # Blank csv file for formatting purposes and easily saving negative samples
    negative_samples = pandas.read_csv(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/Negative Sample Template.csv", sep=",")
    # The center points for our grid blocks for the current grid layout we are using
    # center_points = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/Hex_GridInfo.csv", sep=",")
    # This contains the information of each grid block, such as road count and grid column number
    grid_info = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Hex_Grid/HexGridInfo.csv")

    # Select the range of grid blocks to use for getting new grid blocks
    # This is based on the column length of the center point's grid_num column, which is the block ID number
    # block_number = range(1, 695)

    # The following file(s) are used as an easy way to access the dates in certain years
    # They are separated due to the nature of negative samples by date
    day_holder2017 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2017.xlsx")
    day_holder2018 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2018.xlsx")
    day_holder2019 = pandas.read_excel(
        "Excel & CSV Sheets/Hamilton County Accident System Hex/Day Holder 2019.xlsx")

    # A negative sample location
    neg_loc = 0  # Used for positioning

    # Cast these columns as strings for easy manipulation and comparison
    calldata.Date = calldata.Date.astype(str)
    day_holder2017.Date = day_holder2017.Date.astype(str)
    day_holder2018.Date = day_holder2018.Date.astype(str)
    day_holder2019.Date = day_holder2019.Date.astype(str)
    calldata.Unix = calldata.Unix.astype(int)


    # Lists to hold the values for each type of changed variable that shouldn't be chosen again
    # Ex: The block_list holds the block numbers that have been selected in the current g-loop so we don't
    # choose the same grid block again
    # block_list = []
    date_list_2017 = []
    date_list_2018 = []
    date_list_2019 = []
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
        # Based on what type of negative sampling you want to do, you would have these lines commented out
        # If you want to do grid_fixed negatives, then have these two lines commented out, as well as the other lines
        # in this file that have to do with altering grid num data
        # current_block = calldata.Grid_Num.values[j]
        # block_list.append(current_block)

        # Append the current date (the first date for the main loop) to the list of dates that shouldn't be chosen
        # for finding negative samples
        # Based on the year of the accident's record, we will use the according file
        # This is because when we find a new date for a negative sample, we can only choose new dates from the same year
        # as the original positive sample
        original_accident_year = int(calldata.Date.values[j].split("-")[0])
        if original_accident_year == 2019:
            doa = calldata.Date.values[j]
            date_list_2019.append(doa)
        elif original_accident_year == 2018:
            doa = calldata.Date.values[j]
            date_list_2018.append(doa)
        elif original_accident_year == 2017:
            doa = calldata.Date.values[j]
            date_list_2017.append(doa)

        # Append the current hour (the first hour for the main loop) to the list of hours that shouldn't be chosen
        # for finding negative samples
        current_hour = calldata.Hour.values[j]
        hour_list.append(current_hour)

        # This is the g-loop, where the process of finding a negative sample for our current accident record is repeated
        # This is repeated 9 times so we have a split of roughly %10 positive samples, and %90 negative samples
        for g in range(0, 9):
            # Grid Block Changer #
            # list of random grid numbers that aren't in our block_number list
            # If you want to do ns grid_fixed, then have these commented out
            # r_grid = [x for x in block_number if x not in block_list]
            # new_block = random.choice(r_grid)
            # copy_calldata.Grid_Num.values[0] = new_block
            # block_list.append(new_block)

            # Date Changer #
            accident_year = int(copy_calldata.Date.values[0].split("-")[0])
            if accident_year == 2019:
                days = day_holder2019.Date.values
                r_date = [y for y in days if y not in date_list_2019]
                copy_calldata.Date.values[0] = random.choice(r_date)
                date_list_2019.append(copy_calldata.Date.values[0])
            elif accident_year == 2018:
                days = day_holder2018.Date.values
                r_date = [y for y in days if y not in date_list_2018]
                copy_calldata.Date.values[0] = random.choice(r_date)
                date_list_2018.append(copy_calldata.Date.values[0])
            elif accident_year == 2017:
                days = day_holder2017.Date.values
                r_date = [y for y in days if y not in date_list_2017]
                copy_calldata.Date.values[0] = random.choice(r_date)
                date_list_2017.append(copy_calldata.Date.values[0])

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
                            and copy_calldata.Grid_Num.values[0] is compare.Grid_Num.values[n]:
                        no_matches = False
                        break
            # If the boolean value for matches is true, then we save the appropriate data to our negative samples
            # data frame
            if no_matches is True:
                # These values stay the same between copy_calldata and the negative samples
                negative_samples.at[neg_loc, "Accident"] = 0
                negative_samples.at[neg_loc, "Hour"] = copy_calldata.Hour.values[0]
                negative_samples.at[neg_loc, "Date"] = copy_calldata.Date.values[0]
                # Update the unix timestamp
                # Ensure date is formatted as such: yyyy-mm-d
                timestamp = str(copy_calldata.Date.values[0]) + " " + str(copy_calldata.Hour.values[0])
                negative_samples.at[neg_loc, "Unix"] = time.mktime(datetime.strptime(timestamp, "%Y-%m-%d %H").timetuple())
                # for each grid block
                negative_samples.at[neg_loc, "Grid_Num"] = copy_calldata.Grid_Num.values[0]
                # Get the row number to use in grid info based on the grid block of the negative sample
                # The basic idea here is to match row numbers based on grid block numbers
                info_row_num = grid_info.loc[grid_info["Grid_Num"] == copy_calldata.Grid_Num.values[0]].index[0]
                negative_samples.at[neg_loc, "Latitude"] = grid_info.Center_Lat.values[info_row_num]
                negative_samples.at[neg_loc, "Longitude"] = grid_info.Center_Long.values[info_row_num]
                negative_samples.at[neg_loc, "Join_Count"] = grid_info.Join_Count.values[info_row_num]
                negative_samples.at[neg_loc, "NBR_LANES"] = grid_info.NBR_LANES.values[info_row_num]
                negative_samples.at[neg_loc, "TY_TERRAIN"] = grid_info.TY_TERRAIN.values[info_row_num]
                negative_samples.at[neg_loc, "FUNC_CLASS"] = grid_info.FUNC_CLASS.values[info_row_num]
                negative_samples.at[neg_loc, "GRID_ID"] = grid_info.GRID_ID.values[info_row_num]

                neg_loc = neg_loc + 1
        # Delete the copies made earlier to save memory space
        del copy_calldata
        del line_copy
        # Reset the do-not-use lists for the new accident record we'll be using
        # block_list = []
        date_list_2019 = []
        date_list_2018 = []
        date_list_2017 = []
        hour_list = []
        # if j % 500 == 0:
        #     negative_samples.to_csv("../Excel & CSV Sheets/Hex_Grid/Negative Sampling/NS 2017 P1 Done CP.csv")

    negative_samples.to_csv(name, index=False)



##Accident percent is the percent of accidents you want! For example, 75/25 split would be 25 percent accidents. 
def dividing_data(accidents, negatives, accident_percent):
    num_accidents = len(accidents)
    currentNeg = len(negatives)

    wantNeg = round((((num_accidents*100)/accident_percent)-num_accidents))
    divisionInt = round((currentNeg/wantNeg))

    cutNegatives = negatives.iloc[::divisionInt, :]
    data = cutNegatives.append(accidents)
    data = data.sort_values(["Unix", "Grid_Num"])
    return data


# The main lines and files for getting the totally random negative samples
accidents = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/NS 2018 P1.csv")
compare = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/Accident2018 NoHighway.csv")
name = "Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/Grid Fix/NS Fix 2018 P1 Done.csv"
get_negatives_master_gridfix(accidents, compare, name)