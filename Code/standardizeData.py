import os, sys
from sklearn import preprocessing
import pandas

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Get column names first
# df = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-02_18.csv", sep=",")

# dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data_MMR.csv", sep=",")
# columns = dataset.columns.values[1:len(dataset.columns.values)]
# df = df[columns]
# df = df.dropna()
# # # Create the Scaler object
# scaler = preprocessing.MinMaxScaler()
# # # Fit your data on the scaler object
# scaled_df = scaler.fit_transform(df)
# scaled_df = pandas.DataFrame(scaled_df, columns=columns)
# scaled_df.to_csv("../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-03_12_minmax.csv", sep=",", index=False)


##Undoing the MinMax scaler to refind the Latitude/Longitude Values: 
dataset = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-02_18_minmax_withpred.csv", sep=",")
dataset = dataset.loc[dataset['Prediction'] == 1]
print(dataset.Latitude.values[0:5])
print(max(dataset.Latitude.values), min(dataset.Latitude.values))
unscaled_Latitude = dataset.Latitude.values * (max(dataset.Latitude.values) - min(dataset.Latitude.values)) + min(dataset.Latitude.values)
print(unscaled_Latitude[0:5])