import pandas
import numpy
from time import mktime
from pytz import utc, timezone
from datetime import datetime

weekday_2019 = pandas.read_csv("../Excel & CSV Sheets/2019 Data/AccidentCountsbyHourBlockWeekday2019.csv")
weekend_2019 = pandas.read_csv("../Excel & CSV Sheets/2019 Data/AccidentCountsbyHourBlockWeekend2019.csv")
bus_dates = pandas.bdate_range('2019-01-01', '2019-06-25')
negative_samples = pandas.read_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives.csv")
center_points = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/CenterPoints Ori Layout.csv")
grid_info = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Info.csv")

columns = weekday_2019.columns.values
count = 0
neg_loc = 0
for i, hour in enumerate(columns):
    print("Column: ", i)
    for j, values2 in enumerate(weekday_2019.values):
        gridblock = int(values2[0])
        # print(hour, values2[0])values2[0]
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
            negative_samples.to_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives.csv", index=False)
negative_samples.to_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives.csv", index=False)