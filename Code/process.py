import pandas
import xlrd
import xlsxwriter
from decimal import Decimal
from datetime import datetime, date
import numpy
import math
import time
# import xlutils.copy


# bringing info from the excel file in to work on. Remember if you move this file, change this location.
def import_excel_file(file_name, datetime_col_name):
    data_file_name = pandas.read_excel(file_name)
    # get data frame with the selected columns.
    data_file_name = split_datetime(data_file_name, datetime_col_name)
    print('Import complete')
    return data_file_name


# printing column names, if needed.
def get_col_names(data_file_name):
    print(data_file_name.columns)


# printing values for a given column, if needed.
def get_col_values(data_file_name, name_of_column):
    values = data_file_name['name_of_column'].values
    print(values)


# splitting 'Response_Date' into date and time columns.
def split_datetime(data_file_name, datetime_col_name):
    data_file_name['Date'] = data_file_name[datetime_col_name].dt.date
    data_file_name['Time'] = data_file_name[datetime_col_name].dt.time
    print('Time/Date Split complete.')
    return data_file_name


# Dropping calls with NaN entries
def drop_empties(data_file_name):
    data_file_name = data_file_name.dropna()
    print('Empties dispose Complete')
    return data_file_name


# this is the length of the dataframe, in case there are more entries added.
def get_length(data_file_name):
    length = len(data_file_name.index)


# for some reason the formatting in lat/lng isn't importing properly, so divide to get the correct locations
# and save the information to the Call_Information file.
def correct_LatLong(data_file_name, length):
    for index in data_file_name.ix[1:].iterrows():
        index[1]['Latitude'] = (int(index[1]['Latitude']) / 1000000)
        index[1]['Longitude'] = (int(index[1]['Longitude']) / 1000000)
        i = index[0]
        # If the loop reaches the end of the file, then save the information in the file.
        if i is length:
            save_excel_file('Call_Information.xlsx', 'Call Information', data_file_name)
    return data_file_name


# counting occurrence of each type of report. Sorts list in order of number of occurrences for each type
def count_occurrences(data_file_name, occurrence_list):
    count = pandas.Series({w: data_file_name['Problem'].str.contains(w, case=False).sum() for w in occurrence_list})
    count = count.sort_values(ascending=False)
    print(count)


def count_days(data_file_name, days_list):
    count = pandas.Series({w: data_file_name['Date'].str.contains(w, case=False).sum() for w in days_list})
    count = count.sort_values(ascending=False)
    print(count)


def find_Duplicates(data_file_name, occurrence_list):
    count_doubles = 0
    data_file_copy = data_file_name.copy()
    # this goes through the data and finds duplicates, based on a maximum of 4 minutes between calls,
    #  and a change in lat/long location of less than .000001.
    for id1, id2 in zip(data_file_copy.iterrows(), data_file_copy.loc[1:].iterrows()):
        # this duration takes the difference between two times and returns it
        duration = datetime.combine(date.min, id2[1]['Time']) - datetime.combine(date.min, (id1[1]['Time']))
        # this duration gathers the seconds from the duration above then the minutes line changes that number
        # to the absolute value of the actual number of minutes, ignoring
        duration = duration.total_seconds()
        minutes = math.fabs(duration / 60.0)
        # this section is testing whether the calls inside the 4 minute threshold are actually
        # close enough together to be regarding the same accident
        if minutes < 4:
            # if the calls are within 4 minutes of one another, are the lat and long in close proximity as well?
            # the division by 1 mil is required in each loop, since for some reason it refuses to save in the dataframe.
            correct_LatLong(data_file_copy, get_length(data_file_copy))
            # find the absolute value of the change in both lat and lng.
            latChange = math.fabs(id1[1]['Latitude'] - id2[1]['Latitude'])
            longChange = math.fabs(id1[1]['Longitude'] - id2[1]['Longitude'])
            # if the lat/long are in close proximity, print the information.
            if latChange < 0.0001 and longChange < 0.0001:
                # this increments the count of the doubles found.
                count_doubles += 1
                # deciding which entry will be recorded/deleted, based off problem level
                # this section deletes any blank space left at the beginning of the cell by the data enterer.
                problem1 = id1[1]['Problem'].lstrip()
                problem2 = id2[1]['Problem'].lstrip()
                # printing to be sure the levels are reporting properly.
                # print("Problem of first call: ", problem1, ". Level of first call:", occurrence_list.index(problem1))
                # print("Problem of second call: ", problem2, ". Level of second call:", occurrence_list.index(problem2))
                # if the level on the index of the first call is a higher concern than the second.
                if occurrence_list.index(problem1) >= occurrence_list.index(problem2):
                    print(id2[0])
                    data_file_name.drop(id2[0])
                # just delete the other call instead of making a variable here.
                # if the level on the second call is higher than the first
                else:
                    print(id1[0])
                    data_file_name.drop(id1[0])
    # more printing to make sure everything is working correctly.
    # print("Highest level problem:" ,problem)
    # print ('Duration: %.5f ' % minutes, 'Lat1:',id1[1]['Latitude'], 'Lat2:',id2[1]['Latitude'])
    # print( 'Change: %.6f ' %  latChange)
    # print ('Long1:',id1[1]['Longitude'], 'Long2:',id2[1]['Longitude'], 'Change: %.6f ' %  longChange)
    # Print the number of total duplicate calls.
    print("There were :", count_doubles, "occurrences of duplicate calls.")
    return data_file_name


# Saving this set to a new excel sheet, when you're done
def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def save_text_file(CSV_save_file_name, data_file_name):
    data_file_name.to_csv(CSV_save_file_name, sep=',', index=False)


def drop_duplicates(data_file_name, drop_name):
    # i = 0
    # while i < (len(drop_name)):
    for i in range(len(drop_name)):
        data_file_name.drop(data_file_name.index[drop_name[0][i]])
        print ('Dropping row at index {}'.format(drop_name[0][i]))
        # i += 1

    print (data_file_name.head())
    return data_file_name

def main():
    file_name = 'Accident Report - 4-29-2015 - 4-29-2018.xls'
    save_file_name = 'Call_Information.xls'
    sheet = 'Call Information'
    datetime_col_name = 'Response_Date'
    FORMAT = ['Latitude', 'Longitude', 'Date', 'Time', 'Problem']
    occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']
    days_list = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    data_file_name = import_excel_file(file_name, datetime_col_name)
    data_file_name = data_file_name[FORMAT]
    data_file_name = drop_empties(data_file_name)
    data_file_name = correct_LatLong(data_file_name, get_length(data_file_name))
    count_occurrences(data_file_name, occurrence_list)

    print(data_file_name.head())
    drop_name = pandas.read_csv('dup.txt', sep="\n", header=None)
    # print (drop_name.head())
    # i = 0
    # for i in range(0, 30):
    #     print(drop_name[0][i])
    drop_duplicates(data_file_name, drop_name)
    #print (data_file_name.head())

    #find_Duplicates(data_file_name, occurrence_list)
    print(data_file_name.head())
    save_excel_file(save_file_name, sheet, data_file_name)


if __name__ == "__main__":
    main()
