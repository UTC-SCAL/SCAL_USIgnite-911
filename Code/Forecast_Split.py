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

import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
from os.path import exists
import datetime

def generate_results(y_test, predictions, hist, fpr, tpr, roc_auc, n, i):
    ##Set the preferred font size/type. Note: under 14 is sometimes hard to read. 
    font = {'family': 'serif',
            'weight': 'regular',
            'size': 14}
    plt.rc('font', **font)

    fig = plt.figure()

    # plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.yticks((0, .5, 1), (0, .5, 1))
    plt.xticks((0, .5, 1), (0, .5, 1))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # plt.title('Receiver operating characteristic curve')
    title = '../Graphs & Images/ResultsFromIterations/' + str(datetime.datetime.today()) + 'roc' + str(i) + '.png'
    fig.savefig(title, bbox_inches='tight')

    ##This section creates the first N entries prediction graph. 
    # plt.subplot(212)
    fig = plt.figure()
    plt.xticks(range(0, n), range(1, n+1), rotation=90)
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x = range(0,n)
    plt.axhline(y=0.5, color='gray', linestyle='-')
    plt.scatter(x=x, y=predictions[0:n], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:n], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    title = '../Graphs & Images/ResultsFromIterations/' + str(datetime.datetime.today()) + 'pred' + str(i) + '.png'
    fig.savefig(title, bbox_inches='tight')

    ##The font is bolded here, for ease of reading on the ROC curve graph. 
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
    title = '../Graphs & Images/ResultsFromIterations/' + str(datetime.datetime.today()) + 'lossandacc' + str(
        i) + '.png'
    fig.savefig(title, bbox_inches='tight')

def fitting_loops(X_train, y_train, X_test, y_test):
    ##Creating the model framework. 
    model = Sequential()
    model.add(Dense(X_train.shape[1],
                    input_dim=X_train.shape[1], activation='sigmoid'))
    # Usefor standard sized variable set
    model.add(Dense(25, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(20, activation='sigmoid'))
    model.add(Dense(18, activation='sigmoid'))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dropout(.1))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mse',
                optimizer='nadam', metrics=['accuracy'])
    print(model.summary())


    ##For 100 cycles, fits the model so that we can have a forecast model. 
    for i in range(0, 100):
        file = "../Excel & CSV Sheets/" + str(datetime.date.today()) + "AverageHolderForecast.csv"

        if exists('model_forecast.h5'):
            model.load_weights("model_forecast.h5")
            print("Loading Model")
        if exists(file):
            avg_holder = pandas.read_csv(file, usecols=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC"])
            j = avg_holder.shape[0]
        else:
            avg_holder = pandas.DataFrame(columns=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC"])
            j = avg_holder.shape[0]
        #Prints what cycle we are currently on. 
        print("Cycle: ", i)
        patience = 15
        stopper = callbacks.EarlyStopping(monitor='acc', patience=patience)
        hist = model.fit(X_train, y_train, epochs=500, batch_size=5000, validation_data=(X_test, y_test), verbose=1,
                        callbacks=[stopper])
        ##Saving the model to the disk after running the fitting.                 
        model.save_weights("model_forecast.h5")
        print("Saved model to disk")

        # This is evaluating the model, and printing the results of the epochs.
        scores = model.evaluate(X_train, y_train, batch_size=5000)
        print("\nModel Training Accuracy:", scores[1] * 100)
        print("Model Training Loss:", sum(hist.history['loss']) / len(hist.history['loss']))

        # Okay, now let's calculate predictions.
        predictions = model.predict(X_test)

        # Then, let's round to either 0 or 1, since we have only two options.
        predictions_round = [abs(round(x[0])) for x in predictions]

        #Finding the accuracy score. 
        accscore1 = accuracy_score(y_test, predictions_round)
        print("Rounded Test Accuracy:", accscore1 * 100)
        print("Test Loss", sum(hist.history['val_loss']) / len(hist.history['val_loss']))

        #Print the ROC/AUC
        fpr, tpr, _ = roc_curve(y_test, predictions)
        roc_auc = auc(fpr, tpr)
        print('AUC: %f' % roc_auc)

        confusion_matrix(y_test, predictions_round)

        ##Saving the averages into the CSV for future use. 
        avg_holder.loc[j, 'Train_Acc'] = scores[1] * 100
        avg_holder.loc[j, 'Train_Loss'] = sum(hist.history['loss']) / len(hist.history['loss'])
        avg_holder.loc[j, 'Test_Acc'] = accscore1 * 100
        avg_holder.loc[j, 'Test_Loss'] = sum(hist.history['val_loss']) / len(hist.history['val_loss'])
        avg_holder.loc[j, 'AUC'] = roc_auc
        avg_holder.to_csv(file, sep=",")

        #On the first, 50th, and 100th cycle, generates the 3 graphs. 
        if i ==0 or i == 50 or i == 100:
            #The numbers at the end of this call are: 
            #        the number of predictions to be shown in the predictions graph. 
            #        the cycle being shown in the graphs created. 
            generate_results(y_test, predictions, hist, fpr, tpr, roc_auc, 20, i)


dataset = pandas.read_csv("../Excel & CSV Sheets/Full Data Time Sort.csv", sep=",")

forecast = pandas.read_csv("../Excel & CSV Sheets/Forecast Files/Forecast-for4-3-2019_2019-04-02_18_minmax_withpred.csv",sep=",")

#Changing the title of prediction to accident for use in the testing. 
forecast['Accident'] = forecast['Prediction']
##Dropping the predictions and probabilities, since we now have accident. 
forecast = forecast.drop(['Prediction', 'Probability'], axis=1)

#Print the columns, so we know that we've correctly done this thing. 
print(forecast.columns.values)

#Getting X and Y from dataset, then splitting them into test and train. 
X = dataset.ix[:, 1:(len(dataset.columns) + 1)].values
Y = dataset.ix[:, 0].values
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.30, random_state=42)

##This section adds the forecast data to the test data. 
test = pandas.DataFrame(X_test, columns=dataset.columns.values[1:(len(dataset.columns.values)+1)])
y_test = list(y_test)
print(len(test.values))
test = test.append(forecast)
print(len(test.values))
test['Accident'] = y_test


y_test = test['Accident']
X_test = test.ix[:, 0:(len(test.columns)-1)].values

#Sometimes reshaping is necessary, not certain why this happens. 
# y_train = y_train.reshape(81251,1)
# y_test = y_test.reshape(131590,1)


##Saving the split data to csv, if wished. 
# test.to_csv("../Excel & CSV Sheets/Test_withForecastMMR.csv", sep=",", index=False)
# train.to_csv("../Excel & CSV Sheets/Train.csv", sep=",", index=False)

#Run the fitting loop!
fitting_loops(X_train, y_train, X_test, y_test)

