import numpy as np
import os, sys
import pandas
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

np.random.seed(7)
dataset = pandas.read_excel(folderpath + "Excel & CSV Sheets/AD Original+Hours.xlsx")

dataset = dataset[dataset.columns[dataset.dtypes != object]]
print(dataset.shape)
dataset = dataset.dropna()
print(dataset.shape)
dataset = shuffle(dataset)
X = dataset.ix[:,1:-1].values
Y = dataset.ix[:,0].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.35, random_state=42)

clf = SVC()
clf.fit(X_train, y_train)
result = clf.predict(X_test)
print(result)
accscore = accuracy_score(y_test, result)
print(accscore)
plt.plot(result, color='r')
plt.plot(y_test, color='b')
plt.show()
