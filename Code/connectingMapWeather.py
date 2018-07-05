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


def add_weather(calldata, weatherdata):
    print('Call Info: ')
    for i, value in enumerate(calldata.values):
        header_list = ('Date', 'Time', 'Problem', 'Hour', 'Temperature', 'Dewpoint',
                       'Humidity', 'Event', 'Weekday', 'Month')
        date = value[0].strftime('%Y-%m-%d')
        time = value[1]
        hour = value[2]
        hour = int(hour)
        day = value[0].strftime('%w')
        month = value[0].strftime('%-m')
        calldata = calldata.reindex(columns=header_list)

        for j, info in enumerate(weatherdata.values):
            weatherdate = info[0].strftime('%Y-%m-%d')
            weathertime = info[1].strftime('%-H:%M:%S')
            weatherhour = info[1].strftime('%-H')
            weatherhour = int(weatherhour)

            if (weatherdate == date) and (weatherhour == hour):
                calldata.loc[i, 'Temperature'] = weatherdata.loc[j, 'temperature']
                calldata.loc[i, 'Dewpoint'] = weatherdata.loc[j, 'dewpoint']
                calldata.loc[i, 'Humidity'] = weatherdata.loc[j, 'humidity']
                if weatherdata.loc[j, 'event'] is None:
                    pass
                else:
                    calldata.loc[i, 'Event'] = weatherdata.loc[j, 'event']
    save_excel_file('Call_Data_2017_NewStations.xlsx', 'Updated Call Log', calldata)
    return calldata


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def main():
    # Currently Used Weather Stations #
    weather_stations = data_file_name = \
        pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/Current Weather Stations.xlsx")
    # Call Data #
    calldata = data_file_name = \
        pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Agg_CallData2017_Stations.xlsx")

    latcoords = []  # Weather station latitudes
    longcoords = []  # Weather station longitudes
    coords = []  # Weather station coordinates
    # Placing the weather station coordinates into lists
    for i, value in enumerate(weather_stations.values):
        coords.append(str(str(value[4]) + "," + str(value[5])))
        latcoords.append((value[4]))
        longcoords.append((value[5]))

    for i in range(len(calldata.columns)):
        # if calldata.loc[i, "Station"] == "KTNCHATT14":
        if calldata.Station.values[i] == "KTNCHATT14":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT14_2017_Only.csv",
                                sep=",")
            for i, value in enumerate(calldata.values):
                header_list = ('Date', 'Time', 'Problem', 'Hour', 'Temperature', 'Dewpoint',
                               'Humidity', 'Event', 'Weekday', 'Month')
                # I adjusted the original values for data and hour, as the numbers used for the index #
                print(calldata.head())
                date = value[3].strftime('%Y-%m-%d')
                # print("The date: ", date)
                hour = value[6]
                # print("The hour: ", hour)
                hour = int(hour)
                calldata = calldata.reindex(columns=header_list)

                for j, info in enumerate(weatherdata.values):
                    print(weatherdata.head())
                    # This throws an error, likey becuase it tries to reference something that we don't intend it to #
                    print(info[1])
                    weatherdate = datetime.strptime(info[0],'%m/%d/%Y')
                    weatherhour = info[1].strftime('%-H')
                    weatherhour = int(weatherhour)

                    if (weatherdate == date) and (weatherhour == hour):
                        calldata.loc[i, 'Temperature'] = weatherdata.loc[j, 'temperature']
                        calldata.loc[i, 'Dewpoint'] = weatherdata.loc[j, 'dewpoint']
                        calldata.loc[i, 'Humidity'] = weatherdata.loc[j, 'humidity']
                        if weatherdata.loc[j, 'event'] is None:
                            pass
                        else:
                            calldata.loc[i, 'Event'] = weatherdata.loc[j, 'event']
        elif calldata.Station.values[i] == "KTNCHATT20":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT20_2017_Only.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNCHATT77":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT77_2017-01-01_2017-12-31.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNEASTR2":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNEASTR2_2017_Only.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNSODDY29":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY29_2017_Only.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNCHATT57":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT57_2017-01-01_2017-12-31.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNSODDY12":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY12_2017-01-01_2017-12-31.csv",
                    sep=",", index_col=[0])

        elif calldata.Station.values[i] == "KTNSODDY6":
            # load in the corresponding weather station file #
            weatherdata = \
                pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY6_2017-01-01_2017-12-31.csv",
                    sep=",", index_col=[0])

        else:
            weather_station_paths = [
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT14_2017_Only.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT20_2017_Only.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT77_2017-01-01_2017-12-31.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNEASTR2_2017_Only.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY29_2017_Only.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNCHATT57_2017-01-01_2017-12-31.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY12_2017-01-01_2017-12-31.csv",
                "/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2017/KTNSODDY6_2017-01-01_2017-12-31.csv"
            ]
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

    save_excel_file('/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Call_Data_2017_NewStations.xlsx', 'Updated Call Log', calldata)

if __name__ == "__main__":
    main()