from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import pandas
import os

# path = os.path.dirname(sys.argv[0])
# folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# Read in the data you want to normalize/standardize/adjust
dataset = pandas.read_csv("../", sep=",")

dataset = dataset.drop(['Date','Time'], axis=1)
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
scaled_df.to_csv("../",
                 sep=",", index=False)