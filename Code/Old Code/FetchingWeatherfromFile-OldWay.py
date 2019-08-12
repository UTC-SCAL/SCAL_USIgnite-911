import pandas
import os, sys
from datetime import datetime
from darksky import forecast


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

data = pandas.read_csv("../Excel & CSV Sheets/2019 Data/Negative Samples/2019 Sys Negatives Blocks 401 - 599 Matched.csv")
weather_section1 = pandas.read_csv("../Excel & CSV Sheets/2019 Data/Weather2019_400_500_Full.csv")
weather_section2 = pandas.read_csv("../Excel & CSV Sheets/2019 Data/Weather2019_500_600_Full.csv")
weather_before = pandas.read_csv("/home/jeremy/Downloads/ALLWeatherComplete.csv")
weather_before[['Date', 'time']] = weather_before['time'].str.split(' ', expand=True)
weather_before['hour'] = weather_before['time'].str.split(':').str[0]
weather_before['hour'] = weather_before['hour'].astype(str)


def get_weather_byfile(calldata):
    calldata.Event = calldata.Event.astype(str)
    calldata.Conditions = calldata.Conditions.astype(str)
    calldata.Precipitation_Intensity = calldata.Precipitation_Intensity.astype(float)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.EventBefore = calldata.EventBefore.astype(str)
    calldata.ConditionBefore = calldata.ConditionBefore.astype(str)
    # The key for using DarkSky API
    key = find_cred("darksky")
    # Iterate through negative_samples and assign weather data for each incident
    for k, info in enumerate(calldata.values):
        print(k)
        if calldata.EventBefore.values[k] == "nan":
            if 400 <= calldata.Grid_Block.values[k] <= 499:
                weather_data = weather_section1
            elif 500 <= calldata.Grid_Block.values[k] <= 599:
                weather_data = weather_section2
            # All variables are blank-of-accident, thus year is yoa.
            hoa = int(calldata.Hour.values[k])
            # toa = calldata.Time.values[k]
            # mioa = int(toa.split(':')[1])
            # soa = int(toa.split(':')[2])
            doa = calldata.Date.values[k]
            yoa = int(doa.split('-')[0])
            moa = int(doa.split('-')[1])
            dayoa = int(doa.split('-')[2])
            grid_block = calldata.Grid_Block.values[k]
            weather_data.timereadable = weather_data.timereadable.astype(int)
            weather_before['hour'] = weather_before['hour'].astype(int)

            # print(type(weather_data['Date'].values[0]), type(calldata.Date.values[0]))
            # print(type(weather_before['hour'].values[0]))
            # print(type(weather_data['ORIG_FID'].values[0]), type(calldata.Grid_Block.values[0]))
            # exit()

            # Retrieve the previous hour's weather event and conditions for each incident
            # A series of if statements to see what day of the year it is
            # If it is the first of the month, then we call the weather data for the last day of the previous month
            if hoa == 0 and dayoa == 1:  # If 1/1, get weather data from 12/31, reduce year by 1
                if moa == 1:
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 12
                    new_yoa = yoa - 1
                    # new_date = str(new_yoa) + str(new_moa) + str(new_dayoa)
                    seperator = '-'
                    new_date = (str(new_yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # print(new_date, new_hoa, grid_block)
                    # exit()
                    # Get weather data
                    # The following line needs to have this format:
                    try:
                        row_num = weather_data.loc[(weather_before['Date'] == new_date) &
                                                   (weather_before['hour'] == new_hoa) &
                                                   (weather_before['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_before.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_before.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_before.precipIntensity.values[row_num]
                        print("Found weather")
                        continue
                        # exit()
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                        # exit()
                elif moa == 2:  # If 2/1, get weather data from 1/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 1
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 3:  # If 3/1, get weather data from 2/28, same year
                    new_hoa = 23
                    new_dayoa = 28
                    new_moa = 2
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 4:  # If 4/1, get weather data from 3/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 3
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 5:  # If 5/1, get weather data from 4/30, same year
                    new_hoa = 23
                    new_dayoa = 30
                    new_moa = 4
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 6:  # If 6/1, get weather data from 5/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 5
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 7:  # If 7/1, get weather data from 6/30, same year
                    new_hoa = 23
                    new_dayoa = 30
                    new_moa = 6
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 8:  # If 8/1, get weather data from 7/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 7
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 9:  # If 9/1, get weather data from 8/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 8
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 10:  # If 10/1, get weather data from 9/30, same year
                    new_hoa = 23
                    new_dayoa = 30
                    new_moa = 9
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 11:  # If 11/1, get weather data from 10/31, same year
                    new_hoa = 23
                    new_dayoa = 31
                    new_moa = 10
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                elif moa == 12:  # If 12/1, get weather data from 11/30, same year
                    new_hoa = 23
                    new_dayoa = 30
                    new_moa = 11
                    seperator = '-'
                    new_date = (str(yoa), str(new_moa).zfill(2), str(new_dayoa).zfill(2))
                    new_date = seperator.join(new_date)
                    # Get weather data
                    try:
                        row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                   (weather_data['timereadable'] == new_hoa) &
                                                   (weather_data['ORIG_FID'] == grid_block)].index[0]
                        calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                        calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                        calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                        continue
                    except Exception as e:
                        print("Error in finding previous hour")
                        print(e)
                else:
                    print("Error in calculating previous day")
            elif hoa == 0 and dayoa != 1:
                new_dayoa = dayoa - 1
                new_hoa = 23
                seperator = '-'
                new_date = (str(yoa), str(moa).zfill(2), str(new_dayoa).zfill(2))
                new_date = seperator.join(new_date)

                # print(type(new_date), type(new_hoa), type(grid_block))
                # exit()
                # Get weather data
                try:
                    row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                               (weather_data['timereadable'] == new_hoa) &
                                               (weather_data['ORIG_FID'] == grid_block)].index[0]
                    calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                    calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                    calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                    continue
                except Exception as e:
                    print("Error in finding previous hour")
                    print(e)
            elif hoa > 0:
                new_hoa = hoa - 1
                seperator = '-'
                new_date = (str(yoa), str(moa).zfill(2), str(dayoa).zfill(2))
                new_date = seperator.join(new_date)
                # Get weather data
                try:
                    row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                               (weather_data['timereadable'] == new_hoa) &
                                               (weather_data['ORIG_FID'] == grid_block)].index[0]
                    calldata.EventBefore.values[k] = weather_data.icon.values[row_num]
                    calldata.ConditionBefore.values[k] = weather_data.summary.values[row_num]
                    calldata.Precipitation_Intensity.values[k] = weather_data.precipIntensity.values[row_num]
                    continue
                except Exception as e:
                    print("Error in finding previous hour")
                    print(e)
            else:
                print("One of the hours was 0 and didn't register")
    calldata.to_csv("../Excel & CSV Sheets/2019 Data/Negative Samples/2019 Sys Negatives Blocks 401 - 599 Matched 2.csv")
    print("Doing aggregation")
    for i, value in enumerate(calldata.values):
        print(i)
        if "clear" in calldata.Event.values[i] or "clear" in calldata.Conditions.values[i] \
                or "Clear" in calldata.Event.values[i] or "Clear" in calldata.Conditions.values[i]:
            calldata.Clear.values[i] = 1
        else:
            calldata.Clear.values[i] = 0

        if "rain" in calldata.Event.values[i] or "rain" in calldata.Conditions.values[i] \
                or "Rain" in calldata.Event.values[i] or "Rain" in calldata.Conditions.values[i] \
                or "Drizzle" in calldata.Event.values[i] or "Drizzle" in calldata.Conditions.values[i] \
                or "drizzle" in calldata.Event.values[i] or "drizzle" in calldata.Conditions.values[i]:
            calldata.Rain.values[i] = 1
        else:
            calldata.Rain.values[i] = 0

        if "snow" in calldata.Event.values[i] or "snow" in calldata.Conditions.values[i] \
                or "Snow" in calldata.Event.values[i] or "Snow" in calldata.Conditions.values[i]:
            calldata.Snow.values[i] = 1
        else:
            calldata.Snow.values[i] = 0

        if "cloudy" in calldata.Event.values[i] or "cloudy" in \
                calldata.Conditions.values[i] or "Cloudy" in calldata.Event.values[i] or "Cloudy" in \
                calldata.Conditions.values[i] or "overcast" in calldata.Event.values[i] or "overcast" in \
                calldata.Conditions.values[i] or "Overcast" in calldata.Event.values[i] or "Overcast" in \
                calldata.Conditions.values[i]:
            calldata.Cloudy.values[i] = 1
        else:
            calldata.Cloudy.values[i] = 0

        if "fog" in calldata.Event.values[i] or "foggy" in calldata.Conditions.values[i] \
                or "Fog" in calldata.Event.values[i] or "Foggy" in calldata.Conditions.values[i]:
            calldata.Fog.values[i] = 1
        else:
            calldata.Fog.values[i] = 0
        if "rain" in calldata.EventBefore.values[i] or "rain" in calldata.ConditionBefore.values[i] \
                or "Rain" in calldata.EventBefore.values[i] or "Rain" in calldata.ConditionBefore.values[i]:
            calldata.RainBefore.values[i] = 1
        else:
            calldata.RainBefore.values[i] = 0
    calldata.to_csv("../Excel & CSV Sheets/2019 Data/Negative Samples/2019 Sys Negatives Blocks 401 - 599 Matched 3.csv")


get_weather_byfile(data)
