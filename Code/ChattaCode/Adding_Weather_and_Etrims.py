import pandas
import feather
from datetime import datetime 
# import swifter

#Importing all weather, gridblock, and accident files needed 
weather1718 = feather.read_dataframe("/Users/peteway/Documents/GitHub/Ignore/2017+2018 Weather Correct.feather")
weather19 = feather.read_dataframe("/Users/peteway/Documents/GitHub/Ignore/2019 Weather.feather")
accidents = pandas.read_csv("/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/ChattaData Accident System/No_Interstate_Chatta.csv")
# gridblocks = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System/Grid Files/Grid Oriented Layout/Grid Oriented Info.csv")

# accidents['Unix'] = accidents.apply(lambda x : pandas.datetime.strptime(x.Date + " " + str(x.Hour).zfill(2), "%m/%d/%y %H"), axis=1)
#     # This actually makes the column
# accidents['Unix'] = accidents.apply(lambda x : x.Unix.strftime('%s'), axis=1)
# accidents['Unix'] = accidents['Unix'].astype(int)
# accidents['HourBefore'] = accidents.apply(lambda x : int(x.Unix) - (60*60), axis=1)

print(accidents[['DateTime', 'Date','Hour','Unix']].values[0:5])
# exit()
accidents = accidents.drop_duplicates()
print("Beginning length:",len(accidents.Unix))

#Correcting the column name to match up weather files properly. 
weather19 = weather19.rename(columns={"timereadable": "hour"})
# ##Find columns in both 2017/2018 and 2019 files. 
a = weather1718.columns.intersection(weather19.columns)
# #Cutting Weather files to only those columns found above. 
weather19 = weather19.loc[:, (a)]
weather1718 = weather1718.loc[:, (a)]
# #Appending 2019 weather to the end of 2017/2018 weather file and correcting names of columns, then dropping duplicates. 
weather = weather1718.append(weather19, ignore_index=True)
weather = weather.rename(columns={"Center_Long": "Longitude","Center_Lat": "Latitude"})
weather = weather.rename(columns={"ORIG_FID": "Grid_Block"})
weather['Unix'] = weather['Unix'].astype(int)

#Adding gridblock info to accident file. 
# accidents = pandas.merge(accidents, gridblocks, on=("Grid_Block"))
# print("Length after etrims merge:",len(accidents.Accident))
# accidents.to_csv("Excel & CSV Sheets/ChattaData Accident System/ChattaDataAccidentsEtrims.csv", index=False)
# exit()

#Adding current hour weather columns to the accident file. 
# accidents = accidents.drop(['humidity', 'windSpeed', 'windBearing', 'uvIndex', 'precipIntensity',
# 'apparentTemperature', 'windGust', 'cloudCover', 'temperature','dewPoint', 'visibility',
# 'precipType','Grid_Block', 'Unix', 'Rain', 'Cloudy','Foggy', 'Snow', 'Clear'], axis=1)
weatherNow = weather.loc[:,('humidity', 'windSpeed', 'windBearing', 'uvIndex', 'precipIntensity',
'apparentTemperature', 'windGust', 'cloudCover', 'temperature','dewPoint', 'visibility',
'precipType','Grid_Block', 'Unix', 'Rain', 'Cloudy','Foggy', 'Snow', 'Clear')]
accidents = pandas.merge(accidents, weatherNow, on=["Grid_Block", "Unix"], how='left')
accidents = accidents.drop_duplicates()
print("Length after first weather merge:",len(accidents.Unix))


#Adding previous hour weather columns to accident file
# accidents = accidents.drop('RainBefore')
weatherThen = weather[['HourBefore', 'RainBefore', 'Grid_Block']]
accidents = pandas.merge(accidents, weatherThen, on=["HourBefore", "Grid_Block"], how='left')
accidents = accidents.drop_duplicates()
print("Length after second weather merge:",len(accidents.Unix))
#Saving accident file with gridblock data. 
bool_series = pandas.isnull(accidents["humidity"]) 
  
# filtering data 
# displayind data only with team = NaN 
empties = accidents[bool_series] 
print(len(empties.Grid_Block.unique()))
accidents.to_csv("/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/ChattaData Accident System/No_Interstate_Chatta_Complete.csv", index=False)
exit()

