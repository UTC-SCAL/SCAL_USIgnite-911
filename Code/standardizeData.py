import os, sys
from sklearn import preprocessing
import pandas

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Read in the data you want to normalize/standardize/adjust
dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid Oriented Small Data 2017+2018.csv", sep=",")
dataset = dataset.drop(['Latitude','Longitude','Date','Time','Hour','Temperature','Temp_Min','Temp_Max','Dewpoint','Cloud_Coverage','Humidity','Grid_Block'],axis=1)
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
scaled_df.to_csv("../Excel & CSV Sheets/Grid Oriented Small Layout Test Files/Grid OS Data 2017+2018 MMR.csv", sep=",", index=False)
