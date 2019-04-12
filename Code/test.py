import pandas
import xlrd
import xlsxwriter
from decimal import Decimal
from datetime import datetime, date
import numpy
import math
import csv
from collections import Counter
import re
import string


# bringing info from the excel file in to work on. Remember if you move this file, change this location.
def import_excel_file(file_name, datetime_col_name):
    data_file_name = pandas.read_excel(file_name)
    # get data frame with the selected columns.
    data_file_name = split_datetime(data_file_name, datetime_col_name)
    #data_file_name.drop(datetime_col_name)
    print('Import complete')
    return data_file_name

def easy_import_excel_file(file_name):
    data_file_name = pandas.read_excel(file_name)
    print('Import complete')
    return data_file_name

def import_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [r for r in reader]
    return data


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
    data_file_name['Hour'] = data_file_name[datetime_col_name].dt.hour
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
            save_text_file('Call_Information.csv', data_file_name)
    return data_file_name


# counting occurrence of each type of report. Sorts list in order of number of occurrences for each type
def count_occurrences(data_file_name, occurrence_list):
    problems = []
    problem_count = pandas.DataFrame(columns=['Problem', 'Count'])
    for i, value in enumerate(data_file_name['Problem'].values):
        value = value.lstrip()
        problems.append(value)
    for j, problemtype in enumerate(occurrence_list):
        problem_count.loc[j] = [problemtype, problems.count(problemtype)]
    print(problem_count)
    save_excel_file('Problem_Occurences2017.xlsx', 'Problem Count', problem_count)
    save_text_file('Problem_Occurences2017.csv', problem_count)


def count_days(data_file_name, days_list):
    days = []
    day_count = pandas.DataFrame(columns= ['Day', 'Count'])
    for i, value in enumerate(data_file_name['Date'].values):
        day = pandas.to_datetime(value).strftime('%A')
        days.append(day)
    for j, dayofweek in enumerate(days_list):
        day_count.loc[j] = [dayofweek, days.count(dayofweek)]
    print(day_count)
    #save_excel_file('Days of Week.xlsx', 'Daily Count', day_count)
    save_text_file('Days of Week.csv', day_count)


def split_by_day(data_file_name, dayofweek):
    day_count = pandas.DataFrame(columns = data_file_name.columns)
    for i, value in enumerate(data_file_name['Date'].values):
        day = pandas.to_datetime(value).strftime('%A')
        if (day == dayofweek):
            day_count.loc[i] = (data_file_name.iloc[i])
    #save_excel_file_with_format((dayofweek+'_Hours.xlsx'), (dayofweek +' Data'), day_count)
    save_text_file((dayofweek+'_Hours.csv'), day_count)
    print (dayofweek, "splitting complete")
    return day_count


def split_by_year(data_file_name, years):
    year_count = pandas.DataFrame(columns = data_file_name.columns)
    for i, value in enumerate(data_file_name['Date'].values):
        year = pandas.to_datetime(value).strftime('%Y')
        if (year == years):
            year_count.loc[i] = (data_file_name.iloc[i])
    save_excel_file_with_format((years+'_Data.xlsx'), (years +' Data'), year_count)
    #save_text_file((years+'_Data.csv'), year_count)
    print (years, "splitting complete")
    return year_count

def count_hours(data_file_name, hours_list, name):
    hours = []
    filename = (name  + '_Hourly_Count.csv')
    hour_count = pandas.DataFrame(columns=[ 'Count'])
    for i, value in enumerate(data_file_name['Hour'].values):
        hours.append(value)
    for j, hour in enumerate(hours_list):
        hour_count.loc[j] = [hours.count(hour)]
    print(name, "count complete")
    save_excel_file(str(name), 'Hourly Data', hour_count)
    save_text_file(filename, hour_count)
    return hour_count


def calendar_counts(data_file_name, title, day_list):
    days = []
    day_count = pandas.DataFrame(columns=['A','B'])
    day_count['A'] = day_list
    for i, value in enumerate(data_file_name['Date'].values):
        day = pandas.to_datetime(value).strftime('%-j')
        days.append(day)
    for j, date in enumerate(day_list):
        day_count.loc[date,'B'] = days.count(str(date))
    day_count = day_count.iloc[1:]
    print(day_count)
    filename = (title+('Days of Year.csv'))
    #save_excel_file('Days of Week.xlsx', 'Daily Count', day_count)
    save_text_file(filename, day_count)


def sort_by_month(data_file_name):
    #name = ('~/Documents/GitHub/SCAL_USIgnite-911/InfoFor911/Month_Data.csv')
    months = []
    month_count = pandas.DataFrame(columns= ['Month', 'Count'])
    month_list = ['1','2','3','4','5','6','7','8','9','10','11','12']
    for i, value in enumerate(data_file_name['Date'].values):
        month = pandas.to_datetime(value).strftime('%-m')
        #print(month)
        months.append(month)
    for j, monthofyear in enumerate(month_list):
        month_count.loc[j] = [monthofyear, months.count(monthofyear)]
    #print(month_count)
    save_text_file('Months Count.csv', month_count)


# def sort_by_year(data_file_name, year):



#Saving this set to a new excel sheet, when you're done
def save_excel_file_with_format(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy', )
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    format1 = workbook.add_format({'num_format': '-#\.######'})
    format2 = workbook.add_format({'num_format': 'd-mmm-yy'})
    format3 = workbook.add_format({'num_format': 'hh:mm:ss'})
    format4 = workbook.add_format({'num_format': '#\.######'})
    worksheet.set_column('B:B', 10, format4)
    worksheet.set_column('C:C', 10, format1)
    worksheet.set_column('D:D', 25, format2)
    worksheet.set_column('E:E', 10, format3)
    writer.save()


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def save_text_file(CSV_save_file_name, data_file_name):
    data_file_name.to_csv(CSV_save_file_name, sep=',', index=False, header=None)


def csv_from_excel(save_file_name, worksheet_name):
    workbook = xlrd.open_workbook(save_file_name)
    sheet = workbook.sheet_by_name(worksheet_name)
    csv_file = open(save_file_name.replace("xlsx", "csv"), 'w')
    writer = csv.writer(csv_file)

    for rownum in range(sheet.nrows):
        writer.writerow(sheet.row_values(rownum))

    csv_file.close()


def excel_from_csv(csv_file_name):
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        data = [r for r in reader]
    excelfile = pandas.DataFrame(data)
    return excelfile


def drop_duplicates(data_file_name, toremove):
    listing = []
    for i, value in enumerate(toremove.values):
        index = toremove.index.values[i]
        try:
            print(index)
            data_file_name = data_file_name.drop(index=index, inplace=False)
            print ('Dropping row at index {}'.format(index))
        except:
            listing.append(index)
            print("Error on item:  ".format(index))
    print (toremove.head())
    print (listing)
    print(len(listing))
    return data_file_name


def find_Duplicates(data_file_name, occurrence_list):
    count_doubles = 0
    data_file_copy = data_file_name.copy()
    remove = pandas.DataFrame(columns= data_file_copy.columns)
    # id1 = 0
    # id2 = data_file_copy.index[id1 + 1]
    for id1, id in enumerate(data_file_copy.values):
        id2 = data_file_copy.index[id1 + 1]
        print(id1, id2)
        duration = datetime.combine(date.min, data_file_copy.Time[id2]) - datetime.combine(date.min, data_file_copy.Time[id1])
        duration = duration.total_seconds()
        minutes = math.fabs(duration / 60.0)
        if minutes < 4:
            lat1= (int(data_file_copy.Latitude[id1]) / 1000000)
            long1 = (int(data_file_copy.Longitude[id1]) / 1000000)
            lat2 = (int(data_file_copy.Latitude[id2]) / 1000000)
            long2 = (int(data_file_copy.Longitude[id2]) / 1000000)
            latChange = math.fabs(lat1 - lat2)
            longChange = math.fabs(long1 - long2)
            if latChange < 0.0001 and longChange < 0.0001:
                count_doubles += 1
                problem1 = data_file_copy.Problem[id1].lstrip()
                problem2 = data_file_copy.Problem[id2].lstrip()
                if occurrence_list.index(problem1) >= occurrence_list.index(problem2):
                    #print("Dropping id at: ", id2)
                    remove = remove.append(data_file_copy.iloc[[id2]], ignore_index=False)
                    #data_file_name = data_file_name.drop(index=id2, inplace=False)
                else:
                    print("Dropping first id at: ", id1)
                    #print(data_file_copy.iloc[[id1]])
                    remove = remove.append(data_file_copy.iloc[[id1]], ignore_index=False)
                    #data_file_name = data_file_name.drop(index=id1, inplace=False)
        if id2 == len(data_file_copy)-1:
            print("There were :", count_doubles, "occurrences of duplicate calls.")
            save_excel_file('Call_Information1.xlsx', 'Call Info', remove)
            return remove


def main():
    file_name = 'Accident Report - 4-29-2015 - 4-29-2018.xlsx'
    save_file_name = 'Call_Information.xlsx'
    sheet = 'Call Information'
    datetime_col_name = 'Response_Date'
    FORMAT = ['Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Hour']
    occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']
    days_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    file2017 = 'Agg_CallData2017.xlsx'
    problemtest = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel:CSV Files/problemtest.xlsx'
    data_file = easy_import_excel_file(problemtest)


#To drop the excess data from the problem column in python instead of manually.
    for i, value in enumerate(data_file.values):
        value = str(value)
        problem = str(value.split(None,1)[1])
        problem = problem.split('\'',1)[0]

    # count_occurrences(data_file,occurrence_list)


    #
    #
    # hours_list = []
    # for i in range(0, 24):
    #     #print(i)
    #     hours_list.append(i)
    # #
    # day_list = []
    # for i in range(0,366):
    #     # print(i)
    #     i = int(i)
    #     day_list.append(i)

    # file = 'Accident Report - 4-29-2015 - 4-29-2018.xlsx'
    # data_file = import_excel_file(file, datetime_col_name)
    # data_file = data_file[FORMAT]
    # sort_by_month(data_file)
    # print(data_file.head())
    #save_text_file('UnFilteredMonth.csv', data_file)


    # calllog = '2017.xlsx'
    # data = easy_import_excel_file(calllog)


    # Monday_count = easy_import_excel_file('InfoFor911/Monday_Hours.xlsx')
    # Tuesday_count = easy_import_excel_file('Tuesday_Hours.xlsx')
    # Wednesday_count = easy_import_excel_file('Wednesday_Hours.xlsx')
    # Thursday_count = easy_import_excel_file('Thursday_Hours.xlsx')
    # Friday_count = easy_import_excel_file('Friday_Hours.xlsx')
    # Saturday_count = easy_import_excel_file('Saturday_Hours.xlsx')
    # Sunday_count = easy_import_excel_file('Sunday_Hours.xlsx')


    # data_file_name = import_excel_file(file_name, datetime_col_name)
    # data_file_name = data_file_name[FORMAT]
    # data_file_name = drop_empties(data_file_name)
    # data_file_name = correct_LatLong(data_file_name, get_length(data_file_name))
    # count_occurrences(data_file_name, occurrence_list)

    # save_text_file('Mid-Code Save.csv', data_file_name)

    # remove = find_Duplicates(data_file_name, occurrence_list)
    # remove = pandas.read_excel('toremove.xlsx')

    # drop_name = pandas.read_csv('dups.txt', sep="\n", header=None)
    # data_file_name = drop_duplicates(data_file_name, remove)
    # save_excel_file(save_file_name, sheet, data_file_name)
    # toremove = pandas.DataFrame(columns=data_file_name.columns)
    # data_file_name = drop_duplicates(data_file_name, toremove)



    #data_file_name = pandas.read_excel(save_file_name)
    #sort_by_month(data_file_name)

    #
    # count_occurrences(data_file_name, occurrence_list)
    # count_days(data_file_name, days_list)
    # Sixteen_count = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/InfoFor911/2016_Data.xlsx'
    # Sixteen_data = pandas.read_excel(Sixteen_count)
    # count_hours(Sixteen_data, hours_list, '2016')
    # sort_by_month(Sixteen_data)



    #Seventeen_count = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/InfoFor911/2017_Data.xlsx'
    #Eighteen_count = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/InfoFor911/2018_Data.xlsx'

    # Seventeen_data = pandas.read_excel(Seventeen_count)
    # Eighteen_data = pandas.read_excel(Eighteen_count)

    # sort_by_month(Seventeen_count)
    # sort_by_month(Eighteen_count)
    # count_days(Sixteen_data, days_list)
    #calendar_counts(data_file_name, 'Main', day_list)
    # calendar_counts(Sixteen_data, '2016', day_list)
    # calendar_counts(Seventeen_data, '2017',day_list)
    # calendar_counts(Eighteen_data, '2018',day_list)

    # Monday_count = split_by_day(data_file_name, 'Monday')
    # Tuesday_count = split_by_day(data_file_name, 'Tuesday')
    # Wednesday_count = split_by_day(data_file_name, 'Wednesday')
    # Thursday_count = split_by_day(data_file_name, 'Thursday')
    # Friday_count = split_by_day(data_file_name, 'Friday')
    # Saturday_count = split_by_day(data_file_name, 'Saturday')
    # Sunday_count = split_by_day(data_file_name, 'Sunday')
    #
    # Monday_hours = count_hours(Monday_count, hours_list, 'Monday')
    # Tuesday_hours = count_hours(Tuesday_count, hours_list, 'Tuesday')
    # Wednesday_hours = count_hours(Wednesday_count, hours_list, 'Wednesday')
    # Thursday_hours = count_hours(Thursday_count, hours_list, 'Thursday')
    # Friday_hours = count_hours(Friday_count, hours_list, 'Friday')
    # Saturday_hours = count_hours(Saturday_count, hours_list, 'Saturday')
    # Sunday_hours = count_hours(Sunday_count, hours_list, 'Sunday')


    # print(data_file_name.head())


    # save_excel_file_with_format(save_file_name, sheet, data_file_name)

    #
    # decdata = easy_import_excel_file('InfoFor911/NovCorr.xlsx')
    # data = decdata[['Waze', 'Emergency']]
    # correlation = data.corr(method='pearson')
    # print(correlation)


if __name__ == "__main__":
    main()





