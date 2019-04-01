import os, sys
from sklearn import preprocessing
import pandas


## This standardizes the data based on MinMax scaler ##
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
scaled_df.to_csv("../Excel & CSV Sheets/Full Data MinMax.csv", sep=",", index=False)



## This reduces the negative sample data by 1/3 ##
calldata = pandas.read_csv("../Excel & CSV Sheets/Negative Samples Only.csv",sep=",")
reduced = calldata.copy()

# print(len(calldata))
listing = []
for i, info in enumerate(calldata.values):
    if i % 3 == 0:
        pass
    else:
        listing.append(i)
reduced.drop(reduced.index[listing], inplace=True)
reduced.to_csv("../Excel & CSV Sheets/Full Data MinMax Reduced.csv", sep=",")