# Use the plaidml backend dynamically if AMD GPU is in use
try:
    import tensorflow as tf
    from tensorflow.python.client import device_lib
    LST = [x.device_type for x in device_lib.list_local_devices()]
    if not 'GPU' in LST:
        import os
        os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
except ImportError:
    import os
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import os
import sys

# Import matplotlib pyplot safely
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas
import talos
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

from ann_visualizer.visualize import ann_viz
from keras_sequential_ascii import keras2ascii


def generate_results(y_test, y_score,hist):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    font = {'family': 'serif',
            'weight': 'bold',
            'size': 16}

    plt.rc('font', **font)
    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic curve')
    print('AUC: %f' % roc_auc)
    fig.savefig('roc.png', bbox_inches='tight')
    # plt.subplot(212)
    print("This point reached. ")
    fig = plt.figure()

    plt.xticks(range(0, 20), range(1, 21))
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
 
    plt.scatter(x=x, y=predictions_round[0:20], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:20], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    fig.savefig('pred.png', bbox_inches='tight')

    print("Second point reached. ")

    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(hist.history['acc'])
    plt.plot(hist.history['val_acc'])
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right')
    # plt.show()
    fig.savefig('acc.png', bbox_inches='tight')
    print("Third point reached. ")
    # summarize history for loss
    # plt.subplot(212)
    fig = plt.figure()
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    # plt.show()
    fig.savefig('loss.png', bbox_inches='tight')
    print("End reached. ")

## The steps of creating a neural network or deep learning model ##
    # 1. Load Data
    # 2. Defining a neural network
    # 3. Compile a Keras model using an efficient numerical backend
    # 4. Train a model on some data.
    # 5. Evaluate that model on some data!


#           1. Load Data
dataset = pandas.read_csv(
    "../Excel & CSV Sheets/Full Data for Model.csv", sep=",")
dataset = shuffle(dataset)
dataset = shuffle(dataset)

# train = pandas.read_csv(
#     "../Excel & CSV Sheets/Full Data TestDay.csv", sep=",")
# train = shuffle(train)
# train = shuffle(train)


X = dataset.ix[:, 1:(len(dataset.columns)+1)].values
Y = dataset.ix[:, 0].values
# names = train.columns.values[1:-1]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.30, random_state=42)

# test = pandas.read_csv(
#     "../Excel & CSV Sheets/TestDay.csv", sep=",")
# test = shuffle(test)
# test = shuffle(test)

# X_test = test.ix[:, 1:(len(test.columns)+1)].values
# y_test = (test.ix[:, 0].values).reshape((138, 1))
# print("Size of X_Test:", X_test.shape, "Size of y_test:", y_test.shape)

X_test, X_valid, y_test, y_valid = train_test_split(
    X_test, y_test, test_size=0.90, random_state=42)

# print("Number of X variables: ", X.shape[1])


#           2. Defining a Neural Network
# creating the model
model = Sequential()

model.add(Dense(X_train.shape[1],
                input_dim=X_train.shape[1], activation='sigmoid'))
# Usefor standard sized variable set
model.add(Dense(28, activation='sigmoid'))
model.add(Dropout(.1))
model.add(Dense(20, activation='sigmoid'))
model.add(Dense(18, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dropout(.1))

model.add(Dense(1, activation='sigmoid'))

#           3. Compiling a model.
model.compile(loss='mse',
              optimizer='nadam', metrics=['accuracy'])
print(model.summary())

#           4. Train that model on some data!
# Fitting the model to train the data

hist = model.fit(X_train, y_train, epochs=300,
                 batch_size=200, validation_data=(X_valid, y_valid))

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

ann_viz(model, view=True, filename="network.gv", title="Model")
keras2ascii(model)

#     return hist, model
# This is evaluating the model, and printing the results of the epochs.
scores = model.evaluate(X_train, y_train, batch_size=200)
print("\n Model Training Accuracy:", scores[1]*100)

# Okay, now let's calculate predictions.
predictions = model.predict(X_test)
print(predictions[0:5])

# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]
# print(rounded)
accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded Test Accuracy:", accscore1*100)

generate_results(y_test, predictions, hist)
