import pandas
import os, sys


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


# Call in your dataset and the holiday file
dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")
holidays = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/HolidayList.csv")
dataset.Date = dataset.Date.astype(str)
holidays.Dates = holidays.Dates.astype(str)
for i, value in enumerate(dataset.values):
    print(i)
    # Set the default values for an entry to being a weekday, and it's only changed if the day
    # is a travel day or a weekend
    for j, value2 in enumerate(holidays.values):
        dataset.TravelDay.values[i] = 0
        dataset.WeekEnd.values[i] = 0
        dataset.WeekDay.values[i] = 1
        if dataset.Date.values[i] == holidays.Dates.values[j]:
            dataset.TravelDay.values[i] = 1
            dataset.WeekEnd.values[i] = 0
            dataset.WeekDay.values[i] = 0
            break
        elif dataset.Weekday.values[i] == 5 or dataset.Weekday.values[i] == 6:
            dataset.TravelDay.values[i] = 0
            dataset.WeekEnd.values[i] = 1
            dataset.WeekDay.values[i] = 0
            break
        else:
            pass
dataset.to_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")