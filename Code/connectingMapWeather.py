from math import radians, cos, sin, asin, sqrt
import pandas
from datetime import datetime, date

# Haversine Formula #
def haversine(long1, lat1, long2, lat2):
    # convert decimal degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])

    # haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # the radius of the earth in miles
    return c * r

def agg_options(calldata, savename):
    # This section aggs the rainy conditions into just 'Rainy'
    event = pandas.get_dummies(calldata['Event'])
    calldata = pandas.concat([calldata,event],axis=1)
    calldata.drop(['Event'],axis=1,inplace=True)
    for i, value in enumerate(calldata.values):
        # print (i, value)
        if 1 == calldata.loc[i, 'Rain'] or 1 == calldata.loc[i, 'Light Rain'] or \
                        1 == calldata.loc[i, 'Drizzle'] or 1 == calldata.loc[i, 'Light Drizzle'] \
                or 1 == calldata.loc[i, 'Light Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Thunderstorm'] \
                or 1 == calldata.loc[i, 'Thunderstorms and Rain']:
            calldata.loc[i, 'Rainy'] = 1
        else:
            calldata.loc[i, 'Rainy'] = 0
    # calldata = calldata.drop(['Rain', 'Drizzle', 'Light Drizzle', 'Light Rain',
    #                                   'Light Thunderstorms and Rain', 'Thunderstorm', 'Thunderstorms and Rain'], axis=1)
    # This section aggs the heavy rain/thunderstorm options into just 'Rainstorm'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Heavy Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Heavy Rain']:
            calldata.loc[i, 'Rainstorm'] = 1
        else:
            calldata.loc[i, 'Rainstorm'] = 0
    # calldata = calldata.drop(['Heavy Rain', 'Heavy Thunderstorms and Rain'],axis=1)

    # This sections aggs the cloud options together into just 'Cloudy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Overcast'] or 1 == calldata.loc[i, 'Partly Cloudy'] or 1 == calldata.loc[
            i, 'Mostly Cloudy'] \
                or 1 == calldata.loc[i, 'Scattered Clouds']:
            calldata.loc[i, 'Cloudy'] = 1
        else:
            calldata.loc[i, 'Cloudy'] = 0
    # calldata = calldata.drop(['Overcast', 'Partly Cloudy', 'Mostly Cloudy', 'Scattered Clouds'],axis=1)

    # This section aggs the fog options into 'Foggy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Fog'] or 1 == calldata.loc[i, 'Light Freezing Fog'] or \
                        1 == calldata.loc[i, 'Haze'] \
                or 1 == calldata.loc[i, 'Mist'] or 1 == calldata.loc[i, 'Patches of Fog'] or \
                        1 == calldata.loc[i, 'Shallow Fog']:
            calldata.loc[i, 'Foggy'] = 1
        else:
            calldata.loc[i, 'Foggy'] = 0
    # calldata = calldata.drop(['Fog', 'Light Freezing Fog', 'Haze', 'Mist', 'Patches of Fog', 'Shallow Fog'], axis=1)

    save_excel_file(savename, 'Aggregated Weather', calldata)


def add_weather(calldata, weatherdata, i):
    value = calldata.values[i]
    # print("\tLooking at value: ", value)
    header_list = ("Y", "Latitude", "Longitude", "Date","Time", "Problem", "Hour", "Temperature",
                   "Dewpoint", "Humidity", "Month", "Rainy", "Rainstorm", "Cloudy",
                   "Foggy", "Precipitation_Rate", "Station")
    date = value[3].strftime('%Y-%m-%d')
    hour = value[7]
    hour = int(hour)
    calldata = calldata.reindex(columns=header_list)

    for j, info in enumerate(weatherdata.values):
        wd = datetime.strptime(info[0], '%m/%d/%Y')
        weatherdate = wd.date()
        weathertime = datetime.strptime(info[1], '%H:%M:%S')
        weatherhour = int(weathertime.hour)
        if (str(weatherdate) == date) and (weatherhour == hour):
            try:
                calldata.Temperature.values[i] = weatherdata.loc[j, 'temperature']
                calldata.Dewpoint.values[i] = weatherdata.loc[j, 'dewpoint']
                calldata.Humidity.values[i] = weatherdata.loc[j, 'humidity']
                calldata.Precipitation_Rate.values[i] = weatherdata.loc[j, 'precip_rate']
            except:
                pass
    return calldata


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def main():
    # MAIN: Weather Stations for 2017 #
    # weather_stations = data_file_name = \
    #     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Stations_Covering_2017_Reduced.xlsx")

    # MAIN: Weather Stations for 2018 #
    weather_stations = data_file_name = \
        pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/2018 Weather Stations.xlsx")

    # MAIN: Call Data for 2017 #
    # calldata = data_file_name = \
    #     pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Call_Data_2017_NewStations_NoBlanks.xlsx")

    # MAIN: Call Data for 2018 #
    calldata = data_file_name = \
        pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/Agg_CallData2018_Stations.xlsx")


    # Weather Stations used for 2017 #
    # ktnchatt14 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT14_2017_Only.csv",
    #                             sep=",")
    # ktnchatt20 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT20_2017_Only.csv",
    #                 sep=",")
    # ktnchatt77 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT77_2017-01-01_2017-12-31.csv",
    #                 sep=",")
    # ktneastr2 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNEASTR2_2017_Only.csv",
    #                 sep=",")
    # ktnsoddy29 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY29_2017_Only.csv",
    #                 sep=",")
    # ktnchatt57 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT57_2017-01-01_2017-12-31.csv",
    #                 sep=",")
    # ktnsoddy12 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY12_2017-01-01_2017-12-31.csv",
    #                 sep=",")
    # ktnsoddy6 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY6_2017-01-01_2017-12-31.csv",
    #                 sep=",")

    # Weather Stations used for 2018 #
    ktnchatt14 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT14_2018.csv", sep=",")
    ktnchatt20 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT20_2018.csv", sep=",")
    ktnchatt88 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT88_2018.csv", sep=",")
    ktneastr2 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNEASTR2_2018.csv", sep=",")
    ktnharri26 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNHARRI26_2018.csv", sep=",")
    ktnoolte32 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNOOLTE32_2018.csv", sep=",")
    ktnsoddy29 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNSODDY29_2018.csv", sep=",")
    ktnsoddy11 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNSODDY11_2018.csv", sep=",")
    ktntenne3 = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNTENNE3_2018.csv", sep=",")


    latcoords = []  # Weather station latitudes
    longcoords = []  # Weather station longitudes
    coords = []  # Weather station coordinates
    # Placing the weather station coordinates into lists
    for i, value in enumerate(weather_stations.values):
        coords.append(str(str(value[4]) + "," + str(value[5])))
        latcoords.append((value[4]))
        longcoords.append((value[5]))

    for i in range(len(calldata.values)):
        print(i)
        if calldata.Station.values[i] == "KTNCHATT14": # 2017 & 2018
            # load in the corresponding weather station file #
            weatherdata = ktnchatt14

        elif calldata.Station.values[i] == "KTNCHATT20": # 2017 & 2018
            # load in the corresponding weather station file #
            weatherdata = ktnchatt20

        # elif calldata.Station.values[i] == "KTNCHATT77": # 2017
        elif calldata.Station.values[i] == "KTNCHATT88":  # 2018
            # load in the corresponding weather station file #
            # weatherdata = ktnchatt77
            weatherdata = ktnchatt88

        elif calldata.Station.values[i] == "KTNEASTR2": # 2017 & 2018
            # load in the corresponding weather station file #
            weatherdata = ktneastr2

        elif calldata.Station.values[i] == "KTNSODDY29": # 2017 & 2018
            # load in the corresponding weather station file #
            weatherdata = ktnsoddy29

        # elif calldata.Station.values[i] == "KTNCHATT57": # 2017
        elif calldata.Station.values[i] == "KTNHARRI26":  # 2018
            # load in the corresponding weather station file #
            # weatherdata = ktnchatt57
            weatherdata = ktnharri26

        # elif calldata.Station.values[i] == "KTNSODDY12": # 2017
        elif calldata.Station.values[i] == "KTNOOLTE32":  # 2018
            # load in the corresponding weather station file #
            # weatherdata = ktnsoddy12
            weatherdata = ktnoolte32

        # elif calldata.Station.values[i] == "KTNSODDY6": # 2017
        elif calldata.Station.values[i] == "KTNSODDY11":  # 2018
            # load in the corresponding weather station file #
            # weatherdata = ktnsoddy6
            weatherdata = ktnsoddy11
        elif calldata.Station.values[i] == "KTNTENNE3": # 2018
            # load in the corresponding weather station file #
            weatherdata = ktntenne3

        else:
            # weather_station_paths = [ktnchatt14, ktnchatt20, ktnchatt77, ktneastr2,
            #                          ktnsoddy29, ktnchatt57, ktnsoddy12, ktnsoddy6] # 2017
            weather_station_paths = [ktnchatt14, ktnchatt20, ktnchatt88, ktneastr2, ktnharri26, ktnoolte32, ktnsoddy29,
                                     ktnsoddy11, ktntenne3]  # 2018

            # weather_station_names = ["ktnchatt14", "ktnchatt20", "ktnchatt77", "ktneastr2",
            #                          "ktnsoddy29", "ktnchatt57", "ktnsoddy12", "ktnsoddy6"] # 2017
            weather_station_names = ["ktnchatt14", "ktnchatt20", "ktnchatt88", "ktneastr2", "ktnharri26", "ktnoolte32",
                                     "ktnsoddy29", "ktnsoddy11", "ktntenne3"]  # 2018
            call_lat = (calldata.Latitude.values[i]) / 1000000
            call_long = (calldata.Longitude.values[i]) / -1000000
            index = 0
            for j in range(0, len(latcoords)):
                mini = haversine(call_long, call_lat, longcoords[j], latcoords[j])
                if j + 1 != len(latcoords) and haversine(call_long, call_lat, longcoords[j + 1], latcoords[j + 1]) < mini:
                    try:
                        mini = haversine(call_long, call_lat, longcoords[j + 1], latcoords[j + 1])
                        index = j + 1
                    except:
                        pass
                break
            # load in the corresponding weather station file #
            weatherdata = weather_station_paths[index]
            # Here, set the call log's weather station from "Out of Range" to the specified weather station found above
            calldata.Station.values[i] = weather_station_names[index]
        calldata = add_weather(calldata, weatherdata, i)

    save_excel_file('/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData 2018 Stations.xlsx', 'Updated Call Log', calldata)
if __name__ == "__main__":
    main()