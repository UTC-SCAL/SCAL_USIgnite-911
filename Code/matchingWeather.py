import pandas
import os, sys
from datetime import datetime
from darksky import forecast

path = os.path.dirname(sys.argv[0])


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


# weather_data = pandas.read_csv("../")
negative_samples = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS GridFix Master List.csv")

negative_samples.Event = negative_samples.Event.astype(str)
negative_samples.Conditions = negative_samples.Conditions.astype(str)
negative_samples.Precipitation_Intensity = negative_samples.Precipitation_Intensity.astype(float)
negative_samples.Center_Lat = negative_samples.Center_Long.astype(float)
negative_samples.Center_Long = negative_samples.Center_Long.astype(float)
negative_samples.Time = negative_samples.Time.astype(str)
negative_samples.EventBefore = negative_samples.EventBefore.astype(str)
negative_samples.ConditionBefore = negative_samples.ConditionBefore.astype(str)
negative_samples.Grid_Block = negative_samples.Grid_Block.astype(int)
# weather_data.ORIG_FID = weather_data.ORIG_FID.astype(str)
weather_section1 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_0_50_Full.csv")
weather_section2 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_50_100_Full.csv")
weather_section3 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_100_150_Full.csv")
weather_section4 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_150_200_Full.csv")
weather_section5 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_200_250_Full.csv")
weather_section6 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_250_300_Full.csv")
weather_section7 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_300_350_Full.csv")
weather_section8 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_350_400_Full.csv")
weather_section9 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_400_450_Full.csv")
weather_section10 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_450_500_Full.csv")
weather_section11 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_500_550_Full.csv")
weather_section12 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_550_600_Full.csv")
weather_section13 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_600_650_Full.csv")
weather_section14 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_650_700_Full.csv")
weather_section15 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_700_750_Full.csv")
weather_section16 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_750_800_Full.csv")
weather_section17 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_800_850_Full.csv")
weather_section18 = pandas.read_csv("../Excel & CSV Sheets/ALLWeather_850_906_Full.csv")

# Match the weather and negative sample by grid block, date, and hour
key = find_cred("darksky")
for i, values in enumerate(negative_samples.values):
    print(i)
    negative_samples.Grid_Block = negative_samples.Grid_Block.astype(int)
    if 0 <= negative_samples.Grid_Block.values[i] < 50:
        weather_data = weather_section1
    elif 50 <= negative_samples.Grid_Block.values[i] < 100:
        weather_data = weather_section2
    elif 100 <= negative_samples.Grid_Block.values[i] < 150:
        weather_data = weather_section3
    elif 150 <= negative_samples.Grid_Block.values[i] < 200:
        weather_data = weather_section4
    elif 200 <= negative_samples.Grid_Block.values[i] < 250:
        weather_data = weather_section5
    elif 250 <= negative_samples.Grid_Block.values[i] < 300:
        weather_data = weather_section6
    elif 300 <= negative_samples.Grid_Block.values[i] < 350:
        weather_data = weather_section7
    elif 350 <= negative_samples.Grid_Block.values[i] < 400:
        weather_data = weather_section8
    elif 400 <= negative_samples.Grid_Block.values[i] < 450:
        weather_data = weather_section9
    elif 450 <= negative_samples.Grid_Block.values[i] < 500:
        weather_data = weather_section10
    elif 500 <= negative_samples.Grid_Block.values[i] < 550:
        weather_data = weather_section11
    elif 550 <= negative_samples.Grid_Block.values[i] < 600:
        weather_data = weather_section12
    elif 600 <= negative_samples.Grid_Block.values[i] < 650:
        weather_data = weather_section13
    elif 650 <= negative_samples.Grid_Block.values[i] < 700:
        weather_data = weather_section14
    elif 700 <= negative_samples.Grid_Block.values[i] < 750:
        weather_data = weather_section15
    elif 750 <= negative_samples.Grid_Block.values[i] < 800:
        weather_data = weather_section16
    elif 800 <= negative_samples.Grid_Block.values[i] < 850:
        weather_data = weather_section17
    elif 850 <= negative_samples.Grid_Block.values[i] < 906:
        weather_data = weather_section18

    weather_data.ORIG_FID = weather_data.ORIG_FID.astype(str)
    negative_samples.Grid_Block = negative_samples.Grid_Block.astype(str)
    negative_date = negative_samples.Date.values[i]
    negative_hour = negative_samples.Hour.values[i]
    negative_block = negative_samples.Grid_Block.values[i]

    try:
        row_num = weather_data.loc[(weather_data['Date'] == negative_date) &
                                   (weather_data['time'] == negative_hour) &
                                   (weather_data['ORIG_FID'] == negative_block)].index[0]

        negative_samples.Event.values[i] = weather_data.icon.values[row_num]
        negative_samples.Conditions.values[i] = weather_data.summary.values[row_num]

        # Retrieve the previous hour's weather event and conditions for each incident
        # A series of if statements to see what day of the year it is
        # If it is the first of the month, then we call the weather data for the last day of the previous month
        hoa = negative_hour
        dayoa = negative_date.split("-")[2]
        moa = negative_date.split("-")[1]
        yoa = negative_date.split("-")[0]
        if hoa == 0 and dayoa == 1:  # If 1/1, get weather data from 12/31, reduce year by 1
            if moa == 1:
                new_hoa = 23
                new_dayoa = 31
                new_moa = 12
                new_yoa = yoa - 1
                # Get weather data
                # The following line needs to have this format:
                t = datetime(new_yoa, new_moa, new_dayoa, new_hoa, 0, 0).isoformat()
                call = key, negative_samples.Center_Lat.values[i], negative_samples.Center_Long.values[i]
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        negative_samples.EventBefore.values[i] = value.icon
                        negative_samples.ConditionBefore.values[i] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 2:  # If 2/1, get weather data from 1/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 1
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                           (weather_data['time'] == new_hoa) &
                                           (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 3:  # If 3/1, get weather data from 2/28, same year
                new_hoa = 23
                new_dayoa = 28
                new_moa = 2
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 4:  # If 4/1, get weather data from 3/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 3
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 5:  # If 5/1, get weather data from 4/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 4
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 6:  # If 6/1, get weather data from 5/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 5
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 7:  # If 7/1, get weather data from 6/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 6
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 8:  # If 8/1, get weather data from 7/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 7
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 9:  # If 9/1, get weather data from 8/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 8
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 10:  # If 10/1, get weather data from 9/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 9
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 11:  # If 11/1, get weather data from 10/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 10
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            elif moa == 12:  # If 12/1, get weather data from 11/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 11
                new_date = yoa + new_moa + new_dayoa
                prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                                (weather_data['time'] == new_hoa) &
                                                (weather_data['ORIG_FID'] == negative_block)].index[0]
                negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
                negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
            else:
                print("Error in calculating previous day")
        elif hoa == 0 and dayoa != 1:
            new_dayoa = dayoa - 1
            new_hoa = 23
            new_date = yoa + moa + new_dayoa
            prev_row_num = weather_data.loc[(weather_data['Date'] == new_date) &
                                            (weather_data['time'] == new_hoa) &
                                            (weather_data['ORIG_FID'] == negative_block)].index[0]
            negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
            negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
        elif hoa > 0:
            new_hoa = hoa - 1
            prev_row_num = weather_data.loc[(weather_data['Date'] == negative_date) &
                                            (weather_data['time'] == new_hoa) &
                                            (weather_data['ORIG_FID'] == negative_block)].index[0]
            negative_samples.EventBefore.values[i] = weather_data.icon.values[prev_row_num]
            negative_samples.ConditionBefore.values[i] = weather_data.summary.values[prev_row_num]
        else:
            print("One of the hours was 0 and didn't register")
        negative_samples.Precipitation_Intensity.values[i] = weather_data.precipIntensity.values[row_num]
        # Aggregate the weather variables into their binary values
        if "clear" in negative_samples.Event.values[i] or "clear" in negative_samples.Conditions.values[i] \
                or "Clear" in negative_samples.Event.values[i] or "Clear" in negative_samples.Conditions.values[i]:
            negative_samples.Clear.values[i] = 1
        else:
            negative_samples.Clear.values[i] = 0

        if "rain" in negative_samples.Event.values[i] or "rain" in negative_samples.Conditions.values[i] \
                or "Rain" in negative_samples.Event.values[i] or "Rain" in negative_samples.Conditions.values[i] \
                or "Drizzle" in negative_samples.Event.values[i] or "Drizzle" in negative_samples.Conditions.values[i] \
                or "drizzle" in negative_samples.Event.values[i] or "drizzle" in \
                negative_samples.Conditions.values[i]:
            negative_samples.Rain.values[i] = 1
        else:
            negative_samples.Rain.values[i] = 0

        if "snow" in negative_samples.Event.values[i] or "snow" in negative_samples.Conditions.values[i] \
                or "Snow" in negative_samples.Event.values[i] or "Snow" in negative_samples.Conditions.values[i]:
            negative_samples.Snow.values[i] = 1
        else:
            negative_samples.Snow.values[i] = 0

        if "cloudy" in negative_samples.Event.values[i] or "cloudy" in negative_samples.Conditions.values[i] \
                or "Cloudy" in negative_samples.Event.values[i] or "Cloudy" in negative_samples.Conditions.values[i] \
                or "overcast" in negative_samples.Event.values[i] or "overcast" in negative_samples.Conditions.values[i] \
                or "Overcast" in negative_samples.Event.values[i] or "Overcast" in negative_samples.Conditions.values[i]:
            negative_samples.Cloudy.values[i] = 1
        else:
            negative_samples.Cloudy.values[i] = 0

        if "fog" in negative_samples.Event.values[i] or "foggy" in negative_samples.Conditions.values[i] \
                or "Fog" in negative_samples.Event.values[i] or "Foggy" in negative_samples.Conditions.values[i]:
            negative_samples.Fog.values[i] = 1
        else:
            negative_samples.Fog.values[i] = 0
        if "rain" in negative_samples.EventBefore.values[i] or "rain" in negative_samples.ConditionBefore.values[i] \
                or "Rain" in negative_samples.EventBefore.values[i] or "Rain" in negative_samples.ConditionBefore.values[i]:
            negative_samples.RainBefore.values[i] = 1
        else:
            negative_samples.RainBefore.values[i] = 0
    except:
        print("Couldn't match blocks")
    if i % 1000 == 0:
        negative_samples.to_csv(
            "../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS GridFix Master List Matched.csv")
negative_samples.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS GridFix Master List Matched.csv")