from keras.models import Sequential
from keras.layers import Dense
import numpy
import os, sys
import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

numpy.random.seed(7)
path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

def generate_results(y_test, y_score):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic curve')
    plt.show()
    print('AUC: %f' % roc_auc)

calldata = pandas.read_excel(folderpath+ "Excel & CSV Sheets/2017+2018 Data/Accident Data Cut.xlsx")
dataset = pandas.read_excel(folderpath+ "Excel & CSV Sheets/2017+2018 Data/I24AccidentHours Agg Reduced.xlsx")

dataset = dataset[dataset.columns[dataset.dtypes != object]]
calldata = calldata[calldata.columns[calldata.dtypes != object]]


X_train = calldata.ix[:, 1:(len(calldata.columns)+1)].values
y_train = calldata.ix[:,0].values

X_test = dataset.ix[:, 1:(len(dataset.columns)+1)].values
y_test = dataset.ix[:, 0].values


print("X Train",X_train.shape)
print("Y Train",y_train.shape)
print("X Test",X_test.shape)
print("Y Test",y_test.shape)


model = Sequential()
model.add(Dense(X_train.shape[1], input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(30,activation='tanh'))
model.add(Dense(16,activation='tanh'))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=10, batch_size=8)
scores = model.evaluate(X_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions = model.predict(X_test)
predictions_round = [abs(round(x[0])) for x in predictions]
accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded:",accscore1)

print(predictions)
print(predictions_round)
print(y_test)
generate_results(y_test, predictions_round)
plt.plot(predictions, color='red', label="Predictions")
plt.plot(y_test, color='blue', label="Y Values")
plt.plot(predictions_round, color='green', label = "Rounded Predictions")
plt.legend()
plt.show()