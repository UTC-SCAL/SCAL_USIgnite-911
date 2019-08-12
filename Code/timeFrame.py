import pandas
import os, sys

path = os.path.dirname(sys.argv[0])

data = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")

def finding_Dayframe(data)
    for i, value in enumerate(data.values):
        if 0 <= data.Hour.values[i] <= 4 or 18 <= data.Hour.values[i] <= 23:
            data.DayFrame.values[i] = 1
        elif 5 <= data.Hour.values[i] <= 9:
            data.DayFrame.values[i] = 2
        elif 10 <= data.Hour.values[i] <= 12:
            data.DayFrame.values[i] = 3
        elif 13 <= data.Hour.values[i] <= 17:
            data.DayFrame.values[i] = 4
    return data


def finding_DayframeALT(data):
    data["DayFrameAlt"] = ""
    for i, value in enumerate(data.values):
        if 6 <= data.Hour.values[i] <= 12:
            data.DayFrameAlt.values[i] = 1
        elif 13 <= data.Hour.values[i] <= 18:
            data.DayFrameAlt.values[i] = 2
        elif 19 <= data.Hour.values[i] <= 23 or 0 <= data.Hour.values[i] <= 5:
            data.DayFrameAlt.values[i] = 3
    return data


def finding_holidays(data, holidays):
    data.Date = data.Date.astype(str)
    holidays.Dates = holidays.Dates.astype(str)
    for i, value in enumerate(data.values):
        print(i)
        # Set the default values for an entry to being a weekday, and it's only changed if the day
        # is a travel day or a weekend
        for j, value2 in enumerate(holidays.values):
            data.TravelDay.values[i] = 0
            data.WeekEnd.values[i] = 0
            data.WeekDay.values[i] = 1
            # if data.Date.values[i] == holidays.Dates.values[j]:
            #     data.TravelDay.values[i] = 1
            #     data.WeekEnd.values[i] = 0
            #     data.WeekDay.values[i] = 0
            #     break
            # elif data.Weekday.values[i] == 5 or data.Weekday.values[i] == 6:
            if data.Weekday.values[i] == 5 or data.Weekday.values[i] == 6:
                data.TravelDay.values[i] = 0
                data.WeekEnd.values[i] = 1
                data.WeekDay.values[i] = 0
                break
            else:
                pass
    return data


# Call in your data and the holiday file
data = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")
holidays = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/HolidayList.csv")


data = finding_holidays(data, holidays)
