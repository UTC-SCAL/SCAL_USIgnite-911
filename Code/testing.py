
# import numpy
import pandas

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("GtkAgg")
    import matplotlib.pyplot as plt

# from keras.utils import plot_model
# from sklearn import preprocessing
# from keras.callbacks import EarlyStopping
# from keras.layers import Dense, Dropout
# from keras.models import Sequential
# from keras import callbacks
# from sklearn.metrics import accuracy_score, auc, roc_curve
# from sklearn.model_selection import train_test_split
# from sklearn.utils import shuffle
# from sklearn.metrics import confusion_matrix
from datetime import datetime

# import multiprocessing
# from multiprocessing import Pool
# print(multiprocessing.cpu_count())
# exit()

# file = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GridFixed/Forecast-for6-10-2019.csv")
# gridblocks = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/Grid Oriented Info.csv")
# for i, info in enumerate(file.values):
#     print(i)
#     for j, stuff in enumerate(gridblocks.values):
#         if (file.Grid_Col.values[i] == gridblocks.Col_Num.values[j]) & (file.Grid_Row.values[i] == gridblocks.Row_Num.values[j]):
#             file.Grid_Block.values[i] = gridblocks.ORIG_FID.values[j]
# file.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GridFixed/Forecast-for6-10-2019_Done.csv", index=False)

##Splitting the date and time from the utc time to local timezone. 
weather = pandas.read_csv("../Excel & CSV Sheets/2019 Data/2019 Weather Blocks 884-905.csv")

#creating the two columns we need for this 
# weather['Timereadable'] = 0
# weather['Date'] = 0

weather.time = weather.time.astype(int)
weather.timereadable = weather.timereadable.astype(str)
weather.Date = weather.Date.astype(str)

for i, values in enumerate(weather.values):
    print(i)
    normal = datetime.fromtimestamp(int(weather.time.values[i])).strftime('%Y-%m-%d %H')
    weather.Date.values[i] = str(normal.split(" ")[0])
    weather.timereadable.values[i] = str(normal.split(" ")[1])

weather.to_csv("../Excel & CSV Sheets/2019 Data/2019 Weather Blocks 884-905.csv")
exit()

# ##Creating an image demonstrating the model. 
# model = Sequential()
# ##X.shape[1] is the number of columns inside of X. 
# model.add(Dense(32,
#                 input_dim=32, activation='sigmoid'))

# # Use for standard sized variable set
# model.add(Dense(28, activation='sigmoid'))
# model.add(Dropout(.1))
# model.add(Dense(20, activation='sigmoid'))
# model.add(Dense(18, activation='sigmoid'))
# model.add(Dense(10, activation='sigmoid'))
# model.add(Dropout(.1))

# model.add(Dense(1, activation='sigmoid'))


# #   3. Compiling a model.
# model.compile(loss='mse',
#             optimizer='nadam', metrics=['accuracy'])
# print(model.summary())

# # model.load_weights("model_CM.h5")
# plot_model(model, to_file='../Graphs & Images/model.png')

# places = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4.csv", sep=",")
# descriptions = pandas.read_csv(
#         "../Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON RAW.csv",
#         sep=",")

# for k,info in enumerate(places.values):
#     print(k)
#     if places.Hour.values[k] == 0:
#         for n, value in enumerate(descriptions.values):
#             if ((places.Route.values[k] == descriptions.ID_NUMBER.values[n]) and (descriptions.ELM.values[n] >= places.Log_Mile.values[k] >= descriptions.BLM.values[n]) 
#             and descriptions.Feature_Type[n] == 19):
#                 places.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
#                 places.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
#                 break
#     places.to_csv("../Excel & CSV Sheets/ETRIMS/FullGPSwithHourby4withPave.csv", sep=",", index=False)
# test = pandas.read_csv(
#     "../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_GPS.csv", sep=",")




##This section finds the min and max of the route's log miles. 

# routes = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv", sep=",")

# roads = routes.ID_NUMBER.unique()
# print(len(roads))

# df = pandas.DataFrame( columns=['BLM', 'ELM', 'Route'])

# df.Route = roads

# for i, info in enumerate(df.values):
#     list = []
#     print(i)
#     for j, stuff in enumerate(routes.values):
#         # min = routes.BLM.values[j]
#         if routes.ID_NUMBER.values[j] == df.Route.values[i]:

#             list.append(routes.BLM.values[j])
#             list.append(routes.ELM.values[j])
#             mini = min(list)
#             df.BLM.values[i] = mini
#             maxi = max(list)
#             df.ELM.values[i] = maxi
#             # print(mini,maxi)

# df.to_csv('../Excel & CSV Sheets/ETRIMS/UniqueRoutes.csv', sep=",")

dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data.csv", sep=",")
for i,values in enumerate(dataset.values):
    doa = dataset.Date.values[i]
    dataset.Year.values[i] = int(doa.split('/')[2])+2000
print(dataset.Year.values[0:5])
dataset.to_csv('../Excel & CSV Sheets/Full Data with Year.csv', sep=",")
