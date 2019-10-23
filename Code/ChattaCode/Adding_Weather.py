import pandas
import feather


#Importing all weather and accident files needed 
weather1718 = feather.read_dataframe("/Users/peteway/Google Drive/2017+2018 Weather Correct.feather")
weather19 = feather.read_dataframe("/Users/peteway/Google Drive/2019 Weather Correct.feather")
accidents = pandas.read_csv("Excel & CSV Sheets/ChattaData Accident System/ChattaDataAccidents.csv")

accidents['HourBefore'] = accidents['Unix'] - (60*60)

#Correcting the column name to match up weather files properly. 
weather19 = weather19.rename(columns={"timereadable": "hour"})
##Find columns in both 2017/2018 and 2019 files. 
a = weather1718.columns.intersection(weather19.columns)
#Cutting Weather files to only those columns found above. 
weather19 = weather19.loc[:, (a)]
weather1718 = weather1718.loc[:, (a)]
#Appending 2019 weather to the end of 2017/2018 weather file and correcting names of columns. 
weather = weather1718.append(weather19)
weather = weather.rename(columns={"Center_Long": "Longitude","Center_Lat": "Latitude"})
weather = weather.rename(columns={"ORIG_FID": "Grid_Block"})

#Weather columns to add to accident files, for current hour. 
weathercols = ('humidity', 'windSpeed', 'windBearing', 'uvIndex', 'precipIntensity',
       'apparentTemperature', 'windGust', 'cloudCover', 'temperature',
       'dewPoint', 'visibility', 'precipType',
       'Grid_Block', 'Unix', 'Event', 'Conditions', 'Rain', 'Cloudy',
       'Foggy', 'Snow', 'Clear')
weatherNow = weather.loc[:, (weathercols)]

#Weather 'rainbefore' column to add to the accident file.
beforecols = ('HourBefore', 'RainBefore', 'Grid_Block')
weatherBefore = weather.loc[:, (beforecols)]

#Adding previously found columns to the accident file. 
accwithweather = pandas.merge(accidents, weatherNow, on=("Grid_Block", "Unix"))
accwithweather = pandas.merge(accwithweather, weatherBefore, on=("HourBefore", "Grid_Block"))


#Printing dataframe head, then saving. 
print(accwithweather.head)
accwithweather.to_csv("Excel & CSV Sheets/ChattaData Accident System/ChattaDataAccidentswithWeather.csv", index=False)
