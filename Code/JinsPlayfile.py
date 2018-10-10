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

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


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


numpy.random.seed(7)

dataset = pandas.read_csv(folderpath + "Excel & CSV Sheets/2017+2018 Data/Accident Data Cut.csv", sep=",")

print(dataset.shape)
X = dataset.ix[:,1:(len(dataset.columns)+1)].values
print(X)

Y = dataset.ix[:,0].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)

print(X.shape)
print(Y.shape)

model = Sequential()

model.add(Dense(31, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(8,activation='sigmoid'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=10, batch_size=8)

scores = model.evaluate(X_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions = model.predict(X_test)
print(predictions)

predictions_round = [abs(round(x[0])) for x in predictions]
accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded:",accscore1)


print(len(predictions))
print(len(y_test))
generate_results(y_test, predictions_round)
plt.plot(y_test[0:100], color='blue', label="Y Values")
plt.plot(predictions_round[0:100], color='green', label = "Rounded Predictions")
plt.legend()
plt.show()