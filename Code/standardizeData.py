import os, sys
from sklearn import preprocessing
import pandas

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Get column names first
df = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-03_12.csv", sep=",")

dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data_MMR.csv", sep=",")
columns = dataset.columns.values[1:len(dataset.columns.values)]
df = df[columns]
df = df.dropna()
# Create the Scaler object
scaler = preprocessing.MinMaxScaler()
# Fit your data on the scaler object
scaled_df = scaler.fit_transform(df)
scaled_df = pandas.DataFrame(scaled_df, columns=columns)
scaled_df.to_csv("../Excel & CSV Sheets/ETRIMS/Forecast-for4-3-2019_2019-04-03_12_minmax.csv", sep=",", index=False)