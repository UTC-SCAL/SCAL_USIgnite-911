from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2, RFECV
import pandas
import warnings
import os, sys
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
import numpy as np



warnings.filterwarnings("ignore")
path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

# MAIN Calldata 2018 + 2017 #
calldata = pandas.read_excel("../Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Accident Report List Agg Options.xlsx",
                             dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
                                     'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
                                     'Temperature': float, 'Dewpoint': float, 'Event': str, 'Humidity': float,
                                     'Month': int, 'Visibility': float, 'Conditions': str})

X = calldata.ix[:, 1:len(calldata.columns.values)].values
Y = calldata.ix[:, 0].values

# Removing features with low variance #
print("X before feature selection: \n", X)
# Setting variance threshold to 0.5, it keeps Hour, Temperature, Dewpoint, Month, Visibility
sel = VarianceThreshold(threshold=0.5)
print("X after feature selection: \n", sel.fit_transform(X))

# Univariate feature selection #
print("Shape of X before test: ", X.shape)
# Running the test and keeping the 2 most important variables, it keeps Month and Clear
X_new = SelectKBest(chi2, k=4).fit_transform(X, Y)
print("X after test: ", X_new.shape)
print(X_new)

# Recursive feature elimination with cross-validation #
# Create the RFE object and compute a cross-validation score
svc = SVC(kernel="linear")
# The accuracy scoring is proportional to the number of correct classifications
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2), scoring="accuracy")
rfecv.fit(X, Y)
print("Optimal number of features: %d" % rfecv.n_features_)
# Plot the number of features vs the cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (# of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()
