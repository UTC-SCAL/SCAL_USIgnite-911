from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import pandas
import os


# Read in the data you want to normalize/standardize/adjust
dataset = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/Random/All NS Variables/TS_All.csv", sep=",")

dataset = dataset.drop(['Date','City','GRID_ID', 'precipType','Event','Conditions'], axis=1)
# Get the columns of the data
columns = dataset.columns.values[0:len(dataset.columns.values)]

# Drop any empties now, since we don't want empties here!
# df = df.dropna()

# Create the Scaler object
scaler = preprocessing.MinMaxScaler()

# Fit your data on the scaler object
scaled_df = scaler.fit_transform(dataset)
scaled_df = pandas.DataFrame(scaled_df, columns=columns)

# Send it to a csv file!
scaled_df.to_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Negative Sampling/Random/All NS Variables/TS_All_MMR.csv",
                 sep=",", index=False)