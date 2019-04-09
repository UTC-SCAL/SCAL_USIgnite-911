import os, sys
from sklearn import preprocessing
import pandas

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Get column names first
model = pandas.read_csv("../Excel & CSV Sheets/Full Data Time Sort for Model.csv",sep=",")
dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data Time Sort Less.csv", sep=",")
columns = model.columns.values[0:len(model.columns.values)]
dataset = dataset[columns]
##Drop any empties now, since we don't want empties here!
# df = df.dropna()

# # Create the Scaler object
scaler = preprocessing.MinMaxScaler()

# # Fit your data on the scaler object
scaled_df = scaler.fit_transform(dataset)
scaled_df = pandas.DataFrame(scaled_df, columns=columns)
##Send it to a csv file!
scaled_df.to_csv("../Excel & CSV Sheets/Full Data Time Sort for Model_MMR.csv", sep=",", index=False)
