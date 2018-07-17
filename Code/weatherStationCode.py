# import email
# import imaplib
# import os
# from datetime import datetime, timedelta
# import pandas
# from math import radians, cos, sin, asin, sqrt
# import gmplot
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon
#
#
# # Code for getting data from emails #
# def get_Email():
#     # connecting to the gmail imap server
#     m = imaplib.IMAP4_SSL("imap.gmail.com")
#     m.login('utcscal2018@gmail.com', 'EMCS 335')
#     m.select("INBOX")  # here you a can choose a mail box like INBOX instead
#     # use m.list() to get all the mailboxes
#
#     resp, items = m.search(None,"ALL")  # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
#     items = items[0].split()  # getting the mails id
#
#     #This is the number of emails in the inbox.
#     # print(len(items))
#
#     for emailid in items:
#         resp, data = m.fetch(emailid, "(RFC822)")  # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
#         email_body = data[0][1]  # getting the mail content
#         mail = email.message_from_bytes(email_body)
#
#
#         today = (datetime.now()).date()
#         dateofemail = mail["Date"]
#         dateofemail = (email.utils.parsedate_to_datetime(dateofemail)).date() #What time the email was sent, first just from the email, then transformed into something we can work with.
#         day = timedelta(1) #one day in timedelta format. So, exactly 24 hours ago.
#         daybefore = (dateofemail - day)#this is yesterday, which helps in labelling for the file itself.
#
#
#         if dateofemail == today:    #So, if the email is from today.
#             if mail["From"] == '<reports@hc911.org>' and 'Accident Report was executed for HC911' in mail["Subject"]:   #Selecting only the emails that pertain to call records.
#
#                 # Check if any attachments at all
#                 if mail.get_content_maintype() != 'multipart':
#                     continue
#                 # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
#                 for part in mail.walk():
#                     # multipart are just containers, so we skip them
#                     if part.get_content_maintype() == 'multipart':
#                         continue
#
#                     # is this part an attachment ?
#                     if part.get('Content-Disposition') is None:
#                         continue
#
#                     filename = part.get_filename()
#                     print("Downloading this email: ", mail["Subject"])
#
#                     if filename is not None:    #Saves the attachment in the daily record folder with a tidy name.
#                         sv_path = os.path.join('/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/'+ str(daybefore)+'.csv')
#                         if not os.path.isfile(sv_path):
#                             print(sv_path)
#                             fp = open(sv_path, 'wb')
#                             fp.write(part.get_payload(decode=True))
#                             fp.close()
#     file = '/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/' + str(daybefore) + '.csv'
#     calllog = pandas.read_csv(file,sep=",")
#     return calllog
#
#
# # Alters specific columns from data #
# def split_datetime(calldata):
#
#     for i, value in enumerate(calldata.values):
#         header_list = ('Response_Date', 'Fixed_Time_CallClosed', 'Address', 'City', 'Latitude',
#  'Longitude' ,'Problem', 'Date','Time','Hour' )
#         calldata = calldata.reindex(columns=header_list)
# #next three lines are a necessary workaround due to pandas error
#         calldata.Date = calldata.Date.astype(str)
#         calldata.Time = calldata.Time.astype(str)
#         calldata.Hour = calldata.Hour.astype(str)
#
#         date = datetime.strptime(calldata.Response_Date.values[i], '%m/%d/%Y %I:%M:%S %p')
#
#         calldata.Date.values[i] = str(date.date())
#         calldata.Time.values[i] = str(date.time())
#         calldata.Hour.values[i] = date.hour
#     print('Time/Date Split complete.')
#     return calldata
#
#
# # Cleans data from emails #
# def clean_problems(calldata):
#     # To drop the excess data from the problem column in python instead of manually.
#     for i, value in enumerate(calldata.Problem.values):
#         value = str(value)
#         problem = str(value.split(None, 1)[1])
#         problem = problem.split('\'',1)[0]
#         calldata.Problem.values[i] = problem
#     return calldata
#
#
# # Placing 911 incidents on the map and connecting the incidents to their nearest weather station #
# def station_matching(calldata, weather_stations):
#     # Place map
#     gmap = gmplot.GoogleMapPlotter(35.14, -85.17, 11)
#
#     calldata["Station"] = ""
#
#     # print(calldata.head())
#     # Call Data Lat = 1, Long = 2
#     # print(weather_stations.head())
#     # Weather Stations Lat = 4, Long = 5
#
#     latcoords = []  # Weather station latitudes
#     longcoords = []  # Weather station longitudes
#     coords = []  # Weather station coordinates
#     # Dataframe containing the 9 weather stations used
#     station_matches = pandas.DataFrame(index=range(len(calldata)), columns=weather_stations.Station.values)
#     # print(station_matches.head())
#
#     # Placing the weather station coordinates into lists
#     for i, value in enumerate(weather_stations.values):
#         coords.append(str(str(value[4]) + "," + str(value[5])))
#         latcoords.append((value[4]))
#         longcoords.append((value[5]))
#
#     # Placing the weather station identifiers into a list
#     # Doing this allows us to hover our mouse over a weather station and see which one it is
#     stations = []
#     for i, value in enumerate(weather_stations.values):
#         stations.append(value[1])
#
#     # Placing all the weather station pins on the map, marked by cyan pin
#     for i, value in enumerate(latcoords[0:len(latcoords)]):
#         gmap.marker(latcoords[i], longcoords[i], 'c', title=stations[i])
#
#     # Placing all of the 911 incident pins on the map, marked by gray and red pins
#     # for i, value in enumerate(calldata.values):
#     #     lat = (value[1] / 1000000)
#     #     long = (value[2] / -1000000)
#     #     if value[0] == 0:
#     #         gmap.marker(lat, long, '#DCDCDC', title=i) # Places a gray marker if no injury
#     #     elif value[0] == 1:
#     #         gmap.marker(lat, long, '#FF0000', title=i) # Places a red marker if injury
#
#     for i in range(0, len(latcoords)):
#         # Center for the polygon (the weather station)
#         poly_lat = latcoords[i]
#         poly_long = longcoords[i]
#         # Coordinates for the polygon's edges
#         # The A_lat, A_long, B_lat...represent the cardinal points of the octagon (which alone represent a diamond)
#         # Think of them like north, south, east, west points
#         # The P1_lat, P1_long, P2_lat...represent the points in between the cardinal points in the octagon
#         A_lat, A_long = poly_lat + 0.10, poly_long
#         P1_lat, P1_long = poly_lat + 0.09, poly_long + 0.105
#         B_lat, B_long = poly_lat, poly_long + 0.115
#         P2_lat, P2_long = poly_lat - 0.09, poly_long + 0.105
#         C_lat, C_long = poly_lat - 0.10, poly_long
#         P3_lat, P3_long = poly_lat - 0.09, poly_long - 0.105
#         D_lat, D_long = poly_lat, poly_long - 0.115
#         P4_lat, P4_long = poly_lat + 0.09, poly_long - 0.105
#         E_lat, E_long = poly_lat + 0.10, poly_long
#
#         # Drawing an Octagon covering ~ 6.5 - 7 miles
#         station_lats, station_longs = zip(*[(A_lat, A_long), (P1_lat, P1_long), (B_lat, B_long), (P2_lat, P2_long),
#                                             (C_lat, C_long), (P3_lat, P3_long), (D_lat, D_long), (P4_lat, P4_long),
#                                             (E_lat, E_long)])
#         # Placing the previously drawn octagon on the map (just a visual assistant)
#         gmap.plot(station_lats, station_longs, 'cornflowerblue', edge_width=10)
#
#         # Making the actual polygon using the coordinates above
#         poly_coords = ((A_lat, A_long), (P1_lat, P1_long), (B_lat, B_long), (P2_lat, P2_long), (C_lat, C_long),
#                        (P3_lat, P3_long), (D_lat, D_long), (P4_lat, P4_long), (E_lat, E_long))
#         poly = Polygon(poly_coords)
#         for j, value in enumerate(calldata.values):
#             # take in the 911 incident lat and long one at a time
#             call_lat = (calldata.Latitude.values[j]) / 1000000
#             call_long = (calldata.Longitude.values[j]) / -1000000
#             call_incident = Point(call_lat, call_long)
#             # See if the 911 incident is in the current polygon (representing a weather station)
#             if poly.contains(call_incident):
#                 station_matches.loc[j, str(stations[i])] = stations[i]
#             else:
#                 station_matches.loc[j, str(stations[i])] = 0
#
#     # print(station_matches.head())
#     # save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData 2018 Update.xlsx",
#     #                             "station_matching", calldata)
#
#     # Taking out the 0's in weather station matches
#     my_dwindling_sanity = []
#     match_list = station_matches
#     for i, value in enumerate(match_list.values):
#         call_lat = (calldata.Latitude.values[i]) / 1000000
#         call_long = (calldata.Longitude.values[i]) / -1000000
#         call_stations = []
#         # removes 0 values from match_list
#         for station in value:
#             call_stations = [x for x in value if x != 0]
#         # Gets the weather station that has the lowest haversine value (the smallest distance to the 911 incident)
#         if len(call_stations) == 1:
#             value = value[value != 0]
#             my_dwindling_sanity.append(value[0])
#         elif len(call_stations) == 0:
#             my_dwindling_sanity.append("Out of Range")
#         else:
#             min_list = []
#             for j in range(0, len(call_stations)):
#                 index = 0
#                 mini = haversine(call_long, call_lat, longcoords[j], latcoords[j])
#                 if j+1 != len(call_stations) and haversine(call_long, call_lat, longcoords[j+1], latcoords[j+1]) < mini:
#                     try:
#                         mini = haversine(call_long, call_lat, longcoords[j+1], latcoords[j+1])
#                         index = j+1
#                     except:
#                         pass
#                 my_dwindling_sanity.append(call_stations[index])
#                 break
#     calldata["Station"] = my_dwindling_sanity
#     save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData 2018 Update.xlsx",
#                     "station_matching_added_stations", calldata)
#     return calldata
#
#
# def adding_weather_to_incidents(calldata, weather_stations):
#     # Weather Stations used for 2018 #
#     ktnchatt14 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT14_2018.csv",
#         sep=",")
#     ktnchatt20 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT20_2018.csv",
#         sep=",")
#     ktnchatt88 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNCHATT88_2018.csv",
#         sep=",")
#     ktneastr2 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNEASTR2_2018.csv",
#         sep=",")
#     ktnharri26 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNHARRI26_2018.csv",
#         sep=",")
#     ktnoolte32 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNOOLTE32_2018.csv",
#         sep=",")
#     ktnsoddy29 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNSODDY29_2018.csv",
#         sep=",")
#     ktnsoddy11 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNSODDY11_2018.csv",
#         sep=",")
#     ktntenne3 = pandas.read_csv(
#         r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KTNTENNE3_2018.csv",
#         sep=",")
#
#     latcoords = []  # Weather station latitudes
#     longcoords = []  # Weather station longitudes
#     coords = []  # Weather station coordinates
#     # Placing the weather station coordinates into lists
#     for i, value in enumerate(weather_stations.values):
#         coords.append(str(str(value[4]) + "," + str(value[5])))
#         latcoords.append((value[4]))
#         longcoords.append((value[5]))
#
#     for i in range(len(calldata.values)):
#         print(i)
#         if calldata.Station.values[i] == "KTNCHATT14":
#             # load in the corresponding weather station file #
#             weatherdata = ktnchatt14
#
#         elif calldata.Station.values[i] == "KTNCHATT20":
#             # load in the corresponding weather station file #
#             weatherdata = ktnchatt20
#
#         elif calldata.Station.values[i] == "KTNCHATT88":
#             # load in the corresponding weather station file #
#             weatherdata = ktnchatt88
#
#         elif calldata.Station.values[i] == "KTNEASTR2":
#             # load in the corresponding weather station file #
#             weatherdata = ktneastr2
#
#         elif calldata.Station.values[i] == "KTNSODDY29":
#             # load in the corresponding weather station file #
#             weatherdata = ktnsoddy29
#
#         elif calldata.Station.values[i] == "KTNHARRI26":
#             # load in the corresponding weather station file #
#             weatherdata = ktnharri26
#
#         elif calldata.Station.values[i] == "KTNOOLTE32":
#             # load in the corresponding weather station file #
#             weatherdata = ktnoolte32
#
#         elif calldata.Station.values[i] == "KTNSODDY11":
#             # load in the corresponding weather station file #
#             weatherdata = ktnsoddy11
#         elif calldata.Station.values[i] == "KTNTENNE3":
#             # load in the corresponding weather station file #
#             weatherdata = ktntenne3
#
#         else:
#             weather_station_paths = [ktnchatt14, ktnchatt20, ktnchatt88, ktneastr2, ktnharri26, ktnoolte32, ktnsoddy29,
#                                      ktnsoddy11, ktntenne3]
#             weather_station_names = ["ktnchatt14", "ktnchatt20", "ktnchatt88", "ktneastr2", "ktnharri26", "ktnoolte32",
#                                      "ktnsoddy29", "ktnsoddy11", "ktntenne3"]
#             call_lat = (calldata.Latitude.values[i]) / 1000000
#             call_long = (calldata.Longitude.values[i]) / -1000000
#             index = 0
#             for j in range(0, len(latcoords)):
#                 mini = haversine(call_long, call_lat, longcoords[j], latcoords[j])
#                 if j + 1 != len(latcoords) and haversine(call_long, call_lat, longcoords[j + 1],
#                                                          latcoords[j + 1]) < mini:
#                     try:
#                         mini = haversine(call_long, call_lat, longcoords[j + 1], latcoords[j + 1])
#                         index = j + 1
#                     except:
#                         pass
#                 break
#             # load in the corresponding weather station file #
#             weatherdata = weather_station_paths[index]
#             # Here, set the call log's weather station from "Out of Range" to the specified weather station found above
#             calldata.Station.values[i] = weather_station_names[index]
#         calldata = add_weather(calldata, weatherdata, i)
#
#     save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData 2018 Update.xlsx",
#                     "adding_weather_to_incidents", calldata)
#     return calldata
#
#
# # Making dummy variables for data
# def get_weather_dummies(calldata):
#     # Getting dummy variables
#     event = pandas.get_dummies(calldata['Event'])
#     calldata = pandas.concat([calldata, event], axis=1)
#     calldata.drop(['Event'], axis=1, inplace=True)
#     return calldata
# # Aggregating the weather data dummy variables
#
#
# # Getting the y for the incidents
# def find_y(calldata):
#     for i, value in enumerate(calldata.values):
#         if 'No Injuries' in calldata.loc[i, 'Problem'] or 'Unknown Injuries' in calldata.loc[
#             i, 'Problem'] or 'Delayed' in calldata.loc[i, 'Problem']:
#             calldata.ix[i, 'Y'] = 0
#         else:
#             calldata.ix[i, 'Y'] = 1
#     return calldata
#
#
# def agg_options(calldata):
#     # This section aggs the rainy conditions into just 'Rainy'
#     event = pandas.get_dummies(calldata['Event'])
#     calldata = pandas.concat([calldata,event],axis=1)
#     calldata.drop(['Event'],axis=1,inplace=True)
#     for i, value in enumerate(calldata.values):
#         # print (i, value)
#         if 1 == calldata.loc[i, 'Rain'] or 1 == calldata.loc[i, 'Light Rain'] or \
#                         1 == calldata.loc[i, 'Drizzle'] or 1 == calldata.loc[i, 'Light Drizzle'] \
#                 or 1 == calldata.loc[i, 'Light Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Thunderstorm'] \
#                 or 1 == calldata.loc[i, 'Thunderstorms and Rain']:
#             calldata.loc[i, 'Rainy'] = 1
#         else:
#             calldata.loc[i, 'Rainy'] = 0
#     # calldata = calldata.drop(['Rain', 'Drizzle', 'Light Drizzle', 'Light Rain',
#     #                                   'Light Thunderstorms and Rain', 'Thunderstorm', 'Thunderstorms and Rain'], axis=1)
#     # This section aggs the heavy rain/thunderstorm options into just 'Rainstorm'
#     for i, value in enumerate(calldata.values):
#         if 1 == calldata.loc[i, 'Heavy Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Heavy Rain']:
#             calldata.loc[i, 'Rainstorm'] = 1
#         else:
#             calldata.loc[i, 'Rainstorm'] = 0
#     # calldata = calldata.drop(['Heavy Rain', 'Heavy Thunderstorms and Rain'],axis=1)
#
#     # This sections aggs the cloud options together into just 'Cloudy'
#     for i, value in enumerate(calldata.values):
#         if 1 == calldata.loc[i, 'Overcast'] or 1 == calldata.loc[i, 'Partly Cloudy'] or 1 == calldata.loc[
#             i, 'Mostly Cloudy'] \
#                 or 1 == calldata.loc[i, 'Scattered Clouds']:
#             calldata.loc[i, 'Cloudy'] = 1
#         else:
#             calldata.loc[i, 'Cloudy'] = 0
#     # calldata = calldata.drop(['Overcast', 'Partly Cloudy', 'Mostly Cloudy', 'Scattered Clouds'],axis=1)
#
#     # This section aggs the fog options into 'Foggy'
#     for i, value in enumerate(calldata.values):
#         if 1 == calldata.loc[i, 'Fog'] or 1 == calldata.loc[i, 'Light Freezing Fog'] or \
#                         1 == calldata.loc[i, 'Haze'] \
#                 or 1 == calldata.loc[i, 'Mist'] or 1 == calldata.loc[i, 'Patches of Fog'] or \
#                         1 == calldata.loc[i, 'Shallow Fog']:
#             calldata.loc[i, 'Foggy'] = 1
#         else:
#             calldata.loc[i, 'Foggy'] = 0
#     # calldata = calldata.drop(['Fog', 'Light Freezing Fog', 'Haze', 'Mist', 'Patches of Fog', 'Shallow Fog'], axis=1)
#     return calldata
#
#
# # Code for working on data for project #
# def haversine(long1, lat1, long2, lat2):
#     # convert decimal degrees to radians
#     long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])
#
#     # haversine formula
#     dlong = long2 - long1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 3956 # the radius of the earth in miles
#     return c * r
#
#
# def add_weather(calldata, weatherdata, i):
#     kcha = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/WeatherStations/Stations Covering 2018/KCHA_events.csv",
#                              sep=",")
#
#     header_list = ("Latitude", "Longitude", "Date","Time", "Problem", "Hour", "Temperature",
#                    "Dewpoint", "Humidity", "Month", "Event", "Precipitation_Rate", "Station")
#     calldata = calldata.reindex(columns=header_list)
#     date = calldata.Date.values[i]
#     hour = calldata.Hour.values[i]
#     month = calldata.Date.values[i].split('-')[1]
#     hour = int(hour)
#     calldata.Month.values[i] = month
#     weatherdata.date = weatherdata.date.astype(str)
#     weatherdata.time = weatherdata.time.astype(str)
#     weatherdata.event = weatherdata.event.astype(str)
#     for k, info in enumerate(kcha.values):
#         wd = datetime.strptime(kcha.date[k], '%m/%d/%Y')
#         weatherdate = wd.date()
#         weathertime = datetime.strptime(kcha.time[k], '%H:%M:%S')
#         weatherhour = int(weathertime.hour)
#         if (str(weatherdate) == date) and (weatherhour == hour):
#             try:
#                 calldata.loc[i, 'Event'] = kcha.loc[k, 'event']
#
#             except:
#                 pass
#     for j, info in enumerate(weatherdata.values):
#         wd = datetime.strptime(weatherdata.date[j], '%m/%d/%Y')
#         weatherdate = wd.date()
#         weathertime = datetime.strptime(weatherdata.time[j], '%H:%M:%S')
#         weatherhour = int(weathertime.hour)
#         if (str(weatherdate) == date) and (weatherhour == hour):
#             try:
#                 calldata.Temperature.values[i] = weatherdata.loc[j, 'temperature']
#                 calldata.Dewpoint.values[i] = weatherdata.loc[j, 'dewpoint']
#                 calldata.Humidity.values[i] = weatherdata.loc[j, 'humidity']
#                 calldata.Precipitation_Rate.values[i] = weatherdata.loc[j, 'precip_rate']
#             except:
#                 pass
#     return calldata
#
#
# def save_excel_file(save_file_name, sheet, data_file_name):
#     writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
#     data_file_name.to_excel(writer, sheet_name=sheet)
#     workbook = writer.book
#     worksheet = writer.sheets[sheet]
#     writer.save()
#
#
# def main():
#     # Run this line each morning #
#     # calldata = get_Email()
#     # Each morning, download new weather data using this link #
#     # http://oco-carbon.com/wunderground-weather-data-downloader/
#
#     calldata = pandas.read_csv(r"/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018-07-11.csv", sep=",")
#     # MAIN: Weather Stations for 2018 #
#     weather_stations = data_file_name = \
#         pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/Weather Stations/2018 Weather Stations.xlsx")
#
#     #Reading file directly for testing.
#     # file = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel:CSV Files/daily report/911_Reports_for_2018-07-10.csv'
#     # calldata = pandas.read_csv(file, sep=",")
#
#     #Removing the excess text from the problem column.
#     calldata = clean_problems(calldata)
#
#     #Splitting and tidying the Response Date to the accident.
#     calldata = split_datetime(calldata)
#     calldata = calldata.drop(['Response_Date', 'Fixed_Time_CallClosed'], axis=1)
#     header_list = ( 'Latitude', 'Longitude','Date', 'Time', 'Problem','Hour','Address', 'City')
#     calldata = calldata.reindex(columns=header_list)
#
#     calldata = station_matching(calldata, weather_stations)
#     calldata = adding_weather_to_incidents(calldata, weather_stations)
#     # for i, value in enumerate(calldata.values[0:2]):
#     #     print(i, value)
#     calldata = get_weather_dummies(calldata)
#     calldata = find_y(calldata)
#     # print(calldata.head())
#     agg_options(calldata)
#     save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/CallData 7-11-2018.xlsx",
#                     "agg_options", calldata)
#
# if __name__ == "__main__":
#     main()