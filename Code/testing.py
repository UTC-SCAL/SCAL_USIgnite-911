##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.


import pandas
import feather


#Importing all weather, gridblock, and accident files needed 
weather1718 = feather.read_dataframe("/Users/peteway/Google Drive/2017+2018 Weather Correct.feather")
# weather19 = feather.read_dataframe("/Users/peteway/Google Drive/2019 Weather Correct.feather")
print(len(weather1718))
weather1718.drop_duplicates(subset =["ORIG_FID", "Unix"], 
                     keep = 'last', inplace = True)
feather.write_dataframe(weather1718, "/Users/peteway/Documents/GitHub/Ignore/2017+2018 Weather Correct.feather")
print(len(weather1718))

tab = pandas.DataFrame(weather1718, columns=('ORIG_FID', 'Date'))
tab = tab.groupby(['ORIG_FID', 'Date']).size()
tab = tab.to_frame()
tab.to_csv("Excel & CSV Sheets/ChattaData Accident System/WeatherGridBlocks.csv")
