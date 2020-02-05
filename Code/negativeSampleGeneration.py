import pandas
import os, sys
import random
import time
from datetime import datetime
import feather
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
    """
    This is our main function for getting negative samples from an accident dataset
    :param calldata: The cut form of the accidents
    :param compare: An unaltered version of the accidents, used for comparison and duplicate finding later in code
    :return:
    General guidelines for commenting our code segments:
        Depending on what format of negative sample generation you want to do, you will need to comment out certain
        parts of the code. By default, the code is written to create Total Shift negatives (random negatives), and it
        changes Grid_Num, Date, and Hour
        If you want to do Grid Fixed negatives, you will need to comment out any code that has to do with altering
        the grid_num variable
        If you want to do Spatial Shift negatives, you will need to comment out any code that has to do with altering
        temporal variables (date and hour)
    """
    # Blank csv file for formatting purposes and easily saving negative samples
    negative_samples = pandas.read_csv(
        "../Excel & CSV Sheets/Hex_Grid/Negative Sampling/Negative Sample Template.csv", sep=",")

    # The center points for our grid blocks for the current grid layout we are using
    # center_points = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/Hex_GridInfo.csv", sep=",")

    # This contains the information of each grid block, such as road count, lat/long, grid id, etc.
    grid_info = pandas.read_csv("../Excel & CSV Sheets/Hex_Grid/HexGridInfo.csv")

    # Select the range of grid numbers to use for getting new grid blocks
    # Depending on what version of the city layout you are using, there may be more or less grid values to go through
    block_number = range(1, 695)

    # The following files are used as an easy way to access the dates in certain years
    # They are separated due to the nature of negative samples by date
    # day_holder2017 = pandas.read_excel(
    #     "../Excel & CSV Sheets/Hex_Grid/Negative Sampling/Day Holder 2017.xlsx")
    # day_holder2018 = pandas.read_excel(
    #     "../Excel & CSV Sheets/Hex_Grid/Negative Sampling/Day Holder 2018.xlsx")
    # day_holder2019 = pandas.read_excel(
    #     "../Excel & CSV Sheets/Hex_Grid/Negative Sampling/Day Holder 2019.xlsx")

    # A negative sample location
    neg_loc = 0  # Used for positioning

    # Cast these columns as strings for easy manipulation and comparison
    calldata.Date = calldata.Date.astype(str)
    # day_holder2017.Date = day_holder2017.Date.astype(str)
    # day_holder2018.Date = day_holder2018.Date.astype(str)
    # day_holder2019.Date = day_holder2019.Date.astype(str)
    calldata.Unix = calldata.Unix.astype(int)

    # Lists to hold the values for each type of changed variable that shouldn't be chosen again
    # Ex: The block_list holds the block numbers that have been selected in the current loop so we don't
    # choose the same grid block again
    block_list = []
    # date_list_2017 = []
    # date_list_2018 = []
    # date_list_2019 = []
    # hour_list = []

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
        # If you want to do grid_fixed or temporal negatives, then have these two lines commented out,
        # as well as the other lines in this file that have to do with altering grid num data
        current_grid = calldata.Grid_Num.values[j]
        block_list.append(current_grid)

        # Append the current date (the first date for the main loop) to the list of dates that shouldn't be chosen
        # for finding negative samples
        # Based on the year of the accident's record, we will use the according file
        # This is because when we find a new date for a negative sample, we can only choose new dates from the same year
        # as the original positive sample
        # If you are running this code on data that has accidents for an incomplete year, then you will need to alter
        # the code to not go past the last date in the current year you are creating negatives for
        # Ex: if you try to get negatives for data that goes up to 1/16/20, you can't create a negative sample that
        # has the date 10/2/20, since there is no corresponding positive sample for that date
        # original_accident_year = int(calldata.Date.values[j].split("-")[0])
        # if original_accident_year == 2019:
        #     doa = calldata.Date.values[j]
        #     date_list_2019.append(doa)
        # elif original_accident_year == 2018:
        #     doa = calldata.Date.values[j]
        #     date_list_2019.append(doa)
        # elif original_accident_year == 2017:
        #     doa = calldata.Date.values[j]
        #     date_list_2019.append(doa)

        # Append the current hour (the first hour for the main loop) to the list of hours that shouldn't be chosen
        # for finding negative samples
        # current_hour = calldata.Hour.values[j]
        # hour_list.append(current_hour)

        # This is the g-loop, where the process of finding a negative sample for our current accident record is repeated
        # This is repeated 9 times so we have a split of roughly %10 positive samples, and %90 negative samples
        for g in range(0, 9):
            # Grid Block Changer #
            # list of random grid numbers that aren't in our block_number list
            # If you want to do grid_fixed or temporal negative sampling, then have these commented out
            r_grid = [x for x in block_number if x not in block_list]
            new_block = random.choice(r_grid)
            copy_calldata.Grid_Num.values[0] = new_block
            block_list.append(new_block)

            # Date Changer #
            # accident_year = int(copy_calldata.Date.values[0].split("-")[0])
            # if accident_year == 2019:
            #     days = day_holder2019.Date.values
            #     r_date = [y for y in days if y not in date_list_2019]
            #     copy_calldata.Date.values[0] = random.choice(r_date)
            #     date_list_2019.append(copy_calldata.Date.values[0])
            # elif accident_year == 2018:
            #     days = day_holder2018.Date.values
            #     r_date = [y for y in days if y not in date_list_2018]
            #     copy_calldata.Date.values[0] = random.choice(r_date)
            #     date_list_2018.append(copy_calldata.Date.values[0])
            # elif accident_year == 2017:
            #     days = day_holder2017.Date.values
            #     r_date = [y for y in days if y not in date_list_2017]
            #     copy_calldata.Date.values[0] = random.choice(r_date)
            #     date_list_2017.append(copy_calldata.Date.values[0])

            # Hour Changer #
            # hours = range(0, 24)
            # r = [x for x in hours if x not in hour_list]  # A list of numbers without n
            # new_hour = random.choice(r)
            # hour_list.append(new_hour)
            # copy_calldata.Hour.values[0] = new_hour

            # Set a boolean value for finding matches
            # If a match is found, the value is set to false and the for loop below is broken
            # This helps us save time for searching for matches, since if we have a single match we move onto the next
            # negative sampling
            no_matches = True
            for n, checks in enumerate(compare.values):
                # Because the copy_calldata row we are working with is an altered form of the compare dataset's
                # corresponding row, we can skip over that corresponding row since we know the two rows will
                # be different
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
                unixTime = time.mktime(datetime.strptime(timestamp, "%Y-%m-%d %H").timetuple())
                negative_samples.at[neg_loc, "Unix"] = unixTime
                # Create the day of the week variable, 0 = Monday, 6 = Sunday
                thisDate = datetime.strptime(timestamp, "%Y-%m-%d %H")
                negative_samples.at[neg_loc, "DayOfWeek"] = thisDate.weekday()
                # for each grid block
                negative_samples.at[neg_loc, "Grid_Num"] = copy_calldata.Grid_Num.values[0]
                # Get the row number to use in grid info based on the grid number of the negative sample
                # The basic idea here is to match row numbers based on grid number numbers
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
        # date_list_2019 = []
        # date_list_2018 = []
        # date_list_2017 = []
        # hour_list = []
    # Some final variable additions before saving, these are saved for the end since they can have lambda statements
    # that apply to the whole column (ideally, this saves time)
    negative_samples['hourbefore'] = negative_samples['Unix'] - 60 * 60
    negative_samples.WeekDay = negative_samples.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    negative_samples.DayFrame = negative_samples.Hour.apply(lambda x: 1 if 0 <= x <= 4 or 19 <= x <= 23
                        else(2 if 5 <= x <= 9 else(3 if 10 <= x <= 13 else 4)))

    negative_samples.to_csv("../", index=False)


##Finding the 'true' negatives from a larger set. 
def cut_negatives(negatives, accidents):
    """
    This cuts our negative samples down to what we call "true" negatives. The idea behind this is using the DayFrame
        variable to find any duplicate values, instead of using the hour variable
    :param negatives:
    :param accidents:
    :return:
    """
    neg_loc = 0  # the line position in the negative samples dataframe
    negative_samples = pandas.DataFrame(columns=negatives.columns.values)
    for i, info in enumerate(negatives.values):
        print(i)
        no_matches = True
        for j, stuff in enumerate(accidents.values):
            if (negatives.DayFrame.values[i] == accidents.DayFrame.values[j]) and \
                    (negatives.WeekDay.values[i] == accidents.WeekDay.values[j]) and \
                    (negatives.Grid_Num.values[i] == accidents.Grid_Num.values[j]):
                no_matches = False
                break
        if no_matches is True:
            negative_samples.loc[neg_loc] = negatives.values[i]
            neg_loc += 1
        # if i % 500 == 0:
        #     negative_samples.to_csv("../", index=False)
    print("True Negatives found :", neg_loc+1)
    negative_samples.to_csv("../", index=False)


def dividing_data(accidents, negatives, accident_percent):
    """
    Method for splitting our negative samples into different percentage splits for testing
    :param accidents:
    :param negatives:
    :param accident_percent: The percent of accidents to non-accidents you want. Ex: for a 75/25 split, the data would
        consist of 25% accidents,a nd 75% non-accidents (or negatives)
    :return:
    """
    num_accidents = len(accidents)
    currentNeg = len(negatives)

    wantNeg = round((((num_accidents*100)/accident_percent)-num_accidents))
    divisionInt = round((currentNeg/wantNeg))

    cutNegatives = negatives.iloc[::divisionInt, :]
    data = cutNegatives.append(accidents)
    data = data.sort_values(["Unix", "Grid_Num"])
    return data


def splitData(mainFile):
    """
    This is a convenience tool for splitting our accident data into chunks for negative sampling.
    Typically, the longer the code runs the slower it will get, so we split the data into even chunks and run them in
        our bootleg parallel style
    :param mainFile: The file that contains the accidents
    :return:
    """
    print(len(mainFile))
    section1 = int(len(mainFile) / 4)
    section2 = int(len(mainFile) * (2 / 4))
    section3 = int(len(mainFile) * (3 / 4))

    p1 = mainFile.iloc[:section1]
    p2 = mainFile.iloc[section1:section2]
    p3 = mainFile.iloc[section2:section3]
    p4 = mainFile.iloc[section3:]

    print(len(p1))
    print(len(p2))
    print(len(p3))
    print(len(p4))
    lenCheck = len(p1) + len(p2) + len(p3) + len(p4)

    if lenCheck != len(mainFile):
        print("Error in splitting data, check the section values in code")
        print("Length of mainFile: ", len(mainFile))
        print("Length of sections summed: ", lenCheck)
    else:
        print("Splitting data worked, saving...")
        p1.to_csv("../", index=False)
        p2.to_csv("../", index=False)
        p3.to_csv("../", index=False)
        p4.to_csv("../", index=False)


def combine_negatives(p1, p2, p3, p4):
    """
    Method for combining the split chunks of the negative sample data
    This method assumes you only have 4 chunks, you may alter the amount as needed
    :return:
    """
    negComb = pandas.concat([p1, p2, p3, p4], axis=0, join='outer', ignore_index=False)
    beforeLen = len(negComb)
    # Drop duplicates if there are any
    negComb.drop_duplicates(keep="first", inplace=True)
    print("Dropped", beforeLen - len(negComb), "negatives")
    negComb.to_csv("../", index=False)

