# This file is kept empty for testing small chunks of code easily.
# Please clear this file when you are done working on the code, and put it into whatever file it needs to go in.
import pandas

accidents = pandas.read_csv("../Main Dir/Spatial Shift Negatives/SS Data 50-50 Split.csv")
accidents = accidents[accidents['Accident'] == 1]

print(accidents.columns)
# rainCount = len(accidents[accidents['Rain'] == 1])
# cloudyCount = len(accidents[accidents['Cloudy'] == 1])
# foggyCount = len(accidents[accidents['Foggy'] == 1])
# snowCount = len(accidents[accidents['Snow'] == 1])
# clearCount = len(accidents[accidents['Clear'] == 1])
# rainBeforeCount = len(accidents[accidents['RainBefore'] == 1])

# print("Total Accidents: ", len(accidents))
# print("Rain Percentage: ", round((rainCount/len(accidents) * 100), 2))
# print("Cloudy Percentage: ", round((cloudyCount/len(accidents) * 100), 2))
# print("Foggy Percentage: ", round((foggyCount/len(accidents) * 100), 2))
# print("Snow Percentage: ", round((snowCount/len(accidents) * 100), 2))
# print("Clear Percentage: ", round((clearCount/len(accidents) * 100), 2))
# print("RainBefore Percentage: ", round((rainBeforeCount/len(accidents) * 100), 2))
