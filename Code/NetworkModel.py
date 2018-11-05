from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import numpy
import os
import sys
import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, auc
from sklearn.utils import shuffle
# Import matplotlib pyplot safely
try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(
        save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def generate_results(y_test, y_score, hist):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic curve')
    print('AUC: %f' % roc_auc)

    plt.subplot(212)
    plt.plot(predictions[0:100], color='red', label="Predictions")
    plt.plot(y_test[0:100], color='blue', label="Accident Occurred")
    plt.legend(loc='upper right', fontsize=8)
    plt.show()

    plt.figure()
    plt.subplot(211)
    plt.plot(hist.history['acc'])
    plt.plot(hist.history['val_acc'])
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right')
    # summarize history for loss
    plt.subplot(212)

    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    plt.show()

## The steps of creating a neural network or deep learning model ##
    # 1. Load Data
    # 2. Defining a neural network
    # 3. Compile a Keras model using an efficient numerical backend
    # 4. Train a model on some data.
    # 5. Evaluate that model on some data!


numpy.random.seed(7)

#           1. Load Data

dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data for Model.csv", sep=",")

dataset = shuffle(dataset)
dataset = shuffle(dataset)


X = dataset.ix[:, 1:(len(dataset.columns)+1)].values

Y = dataset.ix[:, 0].values

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.30, random_state=42)
X_test, X_valid, y_test, y_valid = train_test_split(
    X_test, y_test, test_size=0.90, random_state=42)

print("Number of X variables: ", X.shape[1])

#           2. Defining a Neural Network
# creating the model
model = Sequential()

model.add(Dense(X_train.shape[1],
                input_dim=X_train.shape[1], activation='selu'))

model.add(Dense(28, activation='selu'))
model.add(Dense(20, activation='selu'))
model.add(Dense(18, activation='selu'))
model.add(Dense(10, activation='selu'))

model.add(Dense(1, activation='sigmoid'))

#           3. Compiling a model.
model.compile(loss='binary_crossentropy',
              optimizer='adamax', metrics=['accuracy'])
print(model.summary())

#           4. Train that model on some data!
# Fitting the model to train the data

# es = EarlyStopping(monitor='val_acc', min_delta=.5, patience=5,verbose=1,restore_best_weights=True)
# , callbacks=[es]

hist = model.fit(X_train, y_train, epochs=10000,
                 batch_size=1000, validation_data=(X_valid, y_valid))

#           5. Evaluate that model!
# This is evaluating the model, and printing the results of the epochs.
scores = model.evaluate(X_train, y_train, batch_size=1000)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# Okay, now let's calculate predictions.
predictions = model.predict(X_test)
print(predictions)

# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]
# print(rounded)
accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded:", accscore1)

generate_results(y_test, predictions, hist)
