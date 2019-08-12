import pandas
import numpy
from time import mktime
from pytz import utc, timezone
from datetime import datetime


# Saves the resulting file in filename
def spatial_negatives(negative_samples, weekday_2019, begin, end, filename):
    bus_dates = pandas.bdate_range(begin, end)
    columns = weekday_2019.columns.values
    count = 0
    neg_loc = 0
    for i, hour in enumerate(columns):
        print("Column: ", i)
        for j, values2 in enumerate(weekday_2019.values):
            gridblock = int(values2[0])
            accCount = weekday_2019.iat[j, i]
            if accCount == 0:
                for k, dates in enumerate(bus_dates):
                    date = datetime(dates.year, dates.month, dates.day, int(hour), 0, 0)
                    unixtime = date.strftime('%s')
                    negative_samples.at[neg_loc, "Accident"] = 0
                    negative_samples.at[neg_loc, "UnixTime"] = unixtime
                    negative_samples.at[neg_loc, "Date"] = dates
                    negative_samples.at[neg_loc, "Hour"] = hour
                    negative_samples.at[neg_loc, "Grid_Block"] = gridblock
                    center_row_num = center_points.loc[center_points['ORIG_FID'] == gridblock].index[0]
                    negative_samples.at[neg_loc, "Latitude"] = center_points.Center_Lat.values[center_row_num]
                    negative_samples.at[neg_loc, "Longitude"] = center_points.Center_Long.values[center_row_num]
                    # Get the row number to use in grid info based on the grid block of the negative sample
                    # The basic idea here is to match row numbers based on grid block numbers
                    info_row_num = grid_info.loc[grid_info["ORIG_FID"] == gridblock].index[0]
                    negative_samples.at[neg_loc, "Grid_Col"] = grid_info.at[info_row_num, "Col_Num"]
                    negative_samples.at[neg_loc, "Grid_Row"] = grid_info.at[info_row_num, "Row_Num"]
                    negative_samples.at[neg_loc, "Highway"] = grid_info.at[info_row_num, "Highway"]
                    negative_samples.at[neg_loc, "Land_Use_Mode"] = grid_info.at[info_row_num, "Land_Use_Mode"]
                    negative_samples.at[neg_loc, "Road_Count"] = grid_info.at[info_row_num, "Road_Count"]
                    neg_loc += 1
            if j % 100 == 0:
                negative_samples.to_csv(filename, index=False)
    negative_samples.to_csv(filename, index=False)

def get_Weekend_Dates(begin, end):
    weekenddates= []
    bus_dates = pandas.bdate_range(begin, end)
    delta = end - begin        # timedelta
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        if day not in bus_dates:
            weekenddates.append(day)
    return weekenddates

def make_Weekend_negatives(weekday_2019, weekend_2019, dates, negative_samples, filename):
    count = 0
    neg_loc = 0
    newblocks = []
    columnswd = weekday_2019.columns.values[1:-1]
    columnswe = weekend_2019.columns.values[1:-1]
    for i, hour in enumerate(columnswd):
        begin = datetime.now()
        if int(hour) <=4  or int(hour) >= 18:
            dayframe= 1
        elif   (int(hour) >= 5 and int(hour) <= 9):
            dayframe= 2
        elif  (int(hour) >= 10 and int(hour) <= 12):
            dayframe= 3
        elif  (int(hour) >= 13 and int(hour) <= 17):
            dayframe= 4
        print("Column: ", i)
        for j, values2 in enumerate(weekday_2019.values):
            gridblock = int(values2[0])
            # print(j, gridblock, i, hour)
            # print(hour, values2[0])values2[0]
            accCount = weekday_2019.iat[j, i]
            if accCount != 0:
                try:
                    row_num = weekend_2019.loc[weekend_2019['GridBlock'] == gridblock].index[0]
                    check = weekend_2019.iat[int(row_num), int(hour)]
                    # print(accCount, check)
                    if check == 0:
                        for k, day in enumerate(dates):
                            # print("\t Negative Available")
                            date = datetime(day.year, day.month, day.day, int(hour), 0, 0)
                            unixtime = date.strftime('%s')
                            negative_samples.at[neg_loc, "Accident"] = 0
                            negative_samples.at[neg_loc, "UnixTime"] = unixtime
                            negative_samples.at[neg_loc, "Date"] = str(day)
                            negative_samples.at[neg_loc, "Time"] = date
                            negative_samples.at[neg_loc, "DayFrame"] = dayframe
                            negative_samples.at[neg_loc, "WeekDay"] = 0
                            negative_samples.at[neg_loc, "WeekEnd"] = 1
                            negative_samples.at[neg_loc, "Hour"] = hour
                            negative_samples.at[neg_loc, "Grid_Block"] = gridblock
                            center_row_num = center_points.loc[center_points['ORIG_FID'] == gridblock].index[0]
                            negative_samples.at[neg_loc, "Latitude"] = center_points.Center_Lat.values[center_row_num]
                            negative_samples.at[neg_loc, "Longitude"] = center_points.Center_Long.values[center_row_num]
                            # Get the row number to use in grid info based on the grid block of the negative sample
                            # The basic idea here is to match row numbers based on grid block numbers
                            info_row_num = grid_info.loc[grid_info["ORIG_FID"] == gridblock].index[0]
                            negative_samples.at[neg_loc, "Grid_Col"] = grid_info.at[info_row_num, "Col_Num"]
                            negative_samples.at[neg_loc, "Grid_Row"] = grid_info.at[info_row_num, "Row_Num"]
                            negative_samples.at[neg_loc, "Highway"] = grid_info.at[info_row_num, "Highway"]
                            negative_samples.at[neg_loc, "Land_Use_Mode"] = grid_info.at[info_row_num, "Land_Use_Mode"]
                            negative_samples.at[neg_loc, "Road_Count"] = grid_info.at[info_row_num, "Road_Count"]
                            neg_loc += 1
                except IndexError:
                    # print("\t Block not here, adding.")
                    for k, day in enumerate(dates):
                        date = datetime(day.year, day.month, day.day, int(hour), 0, 0)
                        unixtime = date.strftime('%s')
                        negative_samples.at[neg_loc, "Accident"] = 0
                        negative_samples.at[neg_loc, "UnixTime"] = unixtime
                        negative_samples.at[neg_loc, "Date"] = str(day)
                        negative_samples.at[neg_loc, "Time"] = date
                        negative_samples.at[neg_loc, "Hour"] = hour
                        negative_samples.at[neg_loc, "DayFrame"] = dayframe
                        negative_samples.at[neg_loc, "WeekDay"] = 0
                        negative_samples.at[neg_loc, "WeekEnd"] = 1
                        negative_samples.at[neg_loc, "DayFrame"] = dayframe
                        center_row_num = center_points.loc[center_points['ORIG_FID'] == gridblock].index[0]
                        negative_samples.at[neg_loc, "Latitude"] = center_points.Center_Lat.values[center_row_num]
                        negative_samples.at[neg_loc, "Longitude"] = center_points.Center_Long.values[center_row_num]
                        # Get the row number to use in grid info based on the grid block of the negative sample
                        # The basic idea here is to match row numbers based on grid block numbers
                        info_row_num = grid_info.loc[grid_info["ORIG_FID"] == gridblock].index[0]
                        negative_samples.at[neg_loc, "Grid_Col"] = grid_info.at[info_row_num, "Col_Num"]
                        negative_samples.at[neg_loc, "Grid_Row"] = grid_info.at[info_row_num, "Row_Num"]
                        negative_samples.at[neg_loc, "Highway"] = grid_info.at[info_row_num, "Highway"]
                        negative_samples.at[neg_loc, "Land_Use_Mode"] = grid_info.at[info_row_num, "Land_Use_Mode"]
                        negative_samples.at[neg_loc, "Road_Count"] = grid_info.at[info_row_num, "Road_Count"]
                        neg_loc += 1
            if j % 100 == 0:
                negative_samples.to_csv(filename, index=False)
            end = datetime.now()    
        print("Column",i," took :", end-begin)
    negative_samples.to_csv(filename, index=False)

                # except: 
                #     print("Block not Present")
                #     newblocks.append(gridblock)


##All standard files needed
weekday_2019 = pandas.read_csv("../Excel & CSV Sheets/Systematic Negative Sampling/AccidentCountsbyHour&BlockWeekday2019.csv", index_col='Index')
weekend_2019 = pandas.read_csv("../Excel & CSV Sheets/Systematic Negative Sampling/AccidentCountsbyHour&BlockWeekend2019.csv", index_col='Index')
center_points = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/CenterPoints Ori Layout.csv")
grid_info = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Info.csv")

# Begin/End Dates must be in this form: '2019-06-25'.
begin = '2019-1-1'
end = '2019-5-12'


##Spatial Files
negative_samples = pandas.read_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives.csv")
spatial_negatives(negative_samples, weekday_2019, begin, end, filename)

##Temporal Files 
negative_samples = pandas.read_csv("../Excel & CSV Sheets/Systematic Negative Sampling/2019_Systematic_Negatives_Temporal_Shift.csv")
dates = get_Weekend_Dates(start, end)
make_Weekend_negatives(weekday_2019, weekend_2019, dates, negative_samples, filename)