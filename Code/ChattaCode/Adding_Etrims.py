import pandas
#Importing necessary files
accidents = pandas.read_csv("Excel & CSV Sheets/ChattaData Accident System/ChattaDataAccidentswithWeather.csv")
gridblocks = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System/Grid Files/Grid Oriented Layout/Grid Oriented Info.csv")
#Viewing columns from gridblocks data file. 
print(gridblocks.columns)
#Adding gridblock info to accident file. 
acc = pandas.merge(accidents, gridblocks, on=("Grid_Block"))
#Saving accident file with gridblock data. 
acc.to_csv("Excel & CSV Sheets/ChattaData Accident System/ChattaDataAccidentswithEtrims.csv", index=False)