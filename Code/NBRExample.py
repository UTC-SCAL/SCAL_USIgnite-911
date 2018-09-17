from datetime import datetime
import pandas
import numpy as np
from scipy.stats import nbinom


def _ll_nb2(y, X, beta, alpha):
    mu = np.exp(np.dot(X, beta))
    size = 1/alpha
    prob = size/(size+mu)
    ll = nbinom.logpmf(y, size, prob)
    return ll


# Get the data
calldata = \
    pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx",
                  dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
                          'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
                          'Temperature': float, "Temp_Max": float, "Temp_Min": float, "Monthly_Mean_Temp": float,
                          "Temp_below_0": int, "Temp_0to10": int, "Temp_10to20": int, "Temp_20to30": int,
                          "Temp_30to40": int, "Temp_above_40": int, 'Dewpoint': float, 'Event': str, 'Humidity': float,
                          'Month': int, 'Visibility': float, 'Conditions': str, "Cloud_Coverage": float,
                          "Precipitation_Type": str, "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
                          "Precip_Intensity_Time": float, "EventBefore": str, "ConditionBefore": str})
# Drop certain columns to include only the usable test data in the dataframe
# calldata.drop(["Y", "Latitude", "Longitude", "Date", "Time", "Problem", "Address", "City", "Monthly_Avg_Temp",
#                "Temp_Below_0"], axis=1, inplace=True)
calldata.drop(["Monthly_Avg_Temp", "Temp_Below_0", "Dewpoint"], axis=1, inplace=True)

mini = calldata.columns.get_loc("Event")
maxi = len(calldata.columns)
X = calldata.ix[:, mini:maxi].values
y = 44358
