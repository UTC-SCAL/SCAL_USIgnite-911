import os, sys
from sklearn import preprocessing
import pandas

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Get column names first
df = pandas.read_csv("../Excel & CSV Sheets/Full Data for Model.csv", sep=",")
names = df.columns
# Create the Scaler object
scaler = preprocessing.MinMaxScaler()
# Fit your data on the scaler object
scaled_df = scaler.fit_transform(df)
scaled_df = pandas.DataFrame(scaled_df, columns=names)
scaled_df.to_csv("../Excel & CSV Sheets/Full Data Standardized MinMax.csv", sep=",", index=False)