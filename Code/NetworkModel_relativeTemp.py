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
import numpy
import pandas
import talos
from sklearn import preprocessing
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix

# Import matplotlib pyplot safely
try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib

    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
from os.path import exists
import datetime


def fitting_loops(X, Y):
    #   2. Defining a Neural Network
    # creating the model
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X. 
    model.add(Dense(X.shape[1],
                    input_dim=X.shape[1], activation='sigmoid'))

    # Use for standard sized variable set
    model.add(Dense(X.shape[1] - 5, activation='sigmoid'))
    # model.add(Dropout(.1))
    model.add(Dense(X.shape[1] - 10, activation='sigmoid'))
    # model.add(Dense(X.shape[1]-15, activation='sigmoid'))
    # model.add(Dense(X.shape[1]-20, activation='sigmoid'))
    # model.add(Dropout(.1))

    model.add(Dense(1, activation='sigmoid'))

    #   3. Compiling a model.
    model.compile(loss='mse',
                  optimizer='nadam', metrics=['accuracy'])
    print(model.summary())

    for i in range(0, 50):
        file = "../Excel & CSV Sheets/Grid Layout Test Files/" + str(datetime.date.today()) + "GridAverageHolder.csv"

        ##Splitting data into train and test. 
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, test_size=0.30, random_state=42)

        ##If the model already exists, import and update/use it. If not, create it. 
        if exists('model_aggST'):
            model.load_weights("model_aggST")
            print("Loading Grid Model")

        ##If the average holder file exists, import it. If not, create it. 
        if exists(file):
            avg_holder = pandas.read_csv(file,
                                         usecols=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC", "TN", "FP",
                                                  "FN", "TP"])
            j = avg_holder.shape[0]

        else:
            avg_holder = pandas.DataFrame(
                columns=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC", "TN", "FP", "FN", "TP"])
            j = avg_holder.shape[0]

        ###What cycle of the loop are we on? 
        print("Cycle: ", i)

        # Patience is 15 epochs. If the model doesn't improve over the past 15 epochs, exit training
        patience = 15
        stopper = callbacks.EarlyStopping(monitor='acc', patience=patience)
        hist = model.fit(X_train, y_train, epochs=8000, batch_size=5000, validation_data=(X_test, y_test), verbose=1,
                         callbacks=[stopper])

        ##Save the weights for next run. 
        model.save_weights("model_aggST")
        print("Saved grid model to disk")

        # This is evaluating the model, and printing the results of the epochs.
        scores = model.evaluate(X_train, y_train, batch_size=5000)
        print("\nModel Training Accuracy:", scores[1] * 100)
        print("Model Training Loss:", sum(hist.history['loss']) / len(hist.history['loss']))

        # Okay, now let's calculate predictions probability.
        predictions = model.predict(X_test)

        # Then, let's round to either 0 or 1, since we have only two options.
        predictions_round = [abs(round(x[0])) for x in predictions]

        ##Finding accuracy score of the predictions versus the actual Y. 
        accscore1 = accuracy_score(y_test, predictions_round)
        ##Printing it as a whole number instead of a percent of 1. (Just easier for me to read) 
        print("Rounded Test Accuracy:", accscore1 * 100)
        ##Find the Testing loss as well: 
        print("Test Loss", sum(hist.history['val_loss']) / len(hist.history['val_loss']))

        ##Finding the AUC for the cycle: 
        fpr, tpr, _ = roc_curve(y_test, predictions)
        roc_auc = auc(fpr, tpr)
        print('AUC: %f' % roc_auc)

        ##Confusion Matrix: 
        tn, fp, fn, tp = confusion_matrix(y_test, predictions_round).ravel()
        print(tn, fp, tn, tp)

        ##Adding the scores to the average holder file. 
        avg_holder.loc[j, 'Train_Acc'] = scores[1] * 100
        avg_holder.loc[j, 'Train_Loss'] = sum(hist.history['loss']) / len(hist.history['loss'])
        avg_holder.loc[j, 'Test_Acc'] = accscore1 * 100
        avg_holder.loc[j, 'Test_Loss'] = sum(hist.history['val_loss']) / len(hist.history['val_loss'])
        avg_holder.loc[j, 'AUC'] = roc_auc
        avg_holder.loc[j, 'TP'] = tp
        avg_holder.loc[j, 'TN'] = tn
        avg_holder.loc[j, 'FP'] = fp
        avg_holder.loc[j, 'FN'] = fn

        # Save the average holder file: 
        avg_holder.to_csv(file, sep=",")

        # If we are on the 1st, 50th, or 100th cycle, make some graphs: 
        if i % 10 == 0:
            generate_results(y_test, predictions, hist, fpr, tpr, roc_auc, i)


def generate_results(y_test, predictions, hist, fpr, tpr, roc_auc, i):
    font = {'family': 'serif',
            'weight': 'regular',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(fpr, tpr, label='Grid ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.yticks((0, .5, 1), (0, .5, 1))
    plt.xticks((0, .5, 1), (0, .5, 1))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic curve')
    title = '../Graphs & Images/ResultsFromGridIterations/' + str(datetime.datetime.today()) + 'roc' + str(i) + '.png'
    fig.savefig(title, bbox_inches='tight')
    # plt.subplot(212)
    fig = plt.figure()
    plt.xticks(range(0, 20), range(1, 21), rotation=90)
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    plt.axhline(y=0.5, color='gray', linestyle='-')
    plt.scatter(x=x, y=predictions[0:20], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:20], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    title = '../Graphs & Images/ResultsFromGridIterations/' + str(datetime.datetime.today()) + 'pred' + str(i) + '.png'
    fig.savefig(title, bbox_inches='tight')

    font = {'family': 'serif',
            'weight': 'bold',
            'size': 14}
    plt.rc('font', **font)
    fig = plt.figure()
    a1 = fig.add_subplot(2, 1, 1)
    a1.plot(hist.history['acc'])
    a1.plot(hist.history['val_acc'])
    a1.set_ylabel('Accuracy')
    a1.set_xlabel('Epoch')
    a1.set_yticks((.5, .65, .8))
    a1.set_xticks((0, (len(hist.history['val_acc']) / 2), len(hist.history['val_acc'])))
    a1.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right', fontsize='small')
    # plt.show()
    # fig.savefig('acc.png', bbox_inches='tight')
    # summarize history for loss
    # fig = plt.figure()
    a2 = fig.add_subplot(2, 1, 2)
    # fig = plt.figure()
    a2.plot(hist.history['loss'])
    a2.plot(hist.history['val_loss'])
    a2.set_ylabel('Loss')
    a2.set_xlabel('Epoch')
    a2.set_yticks((.15, .20, .25,))
    a2.set_xticks((0, (len(hist.history['val_loss']) / 2), len(hist.history['val_loss'])))
    a2.legend(['Train Loss', 'Test Loss'], loc='upper right', fontsize='small')
    # plt.show()
    title = '../Graphs & Images/ResultsFromGridIterations/' + str(datetime.datetime.today()) + 'lossandacc' + str(
        i) + '.png'
    fig.savefig(title, bbox_inches='tight')


## The steps of creating a neural network or deep learning model ##
# 1. Load Data
# 2. Defining a neural network
# 3. Compile a Keras model using an efficient numerical backend
# 4. Train a model on some data.
# 5. Evaluate that model on some data!


#           1. Load Data
dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018 MMR.csv", sep=",")

#           Shuffling if needed. 
dataset = shuffle(dataset)
dataset = shuffle(dataset)

#           Creating X and Y. Accident is the first column, therefore it is 0. 
X = dataset.ix[:, 1:(len(dataset.columns) + 1)].values
Y = dataset.ix[:, 0].values

##      Steps 2-5 are inside the fitting loops method. 
fitting_loops(X, Y)


