import pandas
import glob
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from keras import optimizers

##For getting rid of the -1 entries in prediction files. 
def cut_data():
    files = glob.glob('./Excel & CSV Sheets/Forecasts/*/Forecast/*.csv')

    ##Each of the files from the glob is pulled in, and saved into the modelframes dictionary. 
    for f in files: 
        model = (f.split("/")[5]).replace("_Forecast.csv", "")
        date = f.split("/")[3]
        reftitle = model + " " + date
        reftitle = pandas.read_csv(f, sep = ",")
        print(model, "Length of data:",len(reftitle))
        reftitle = reftitle[reftitle['Road_Count'] > 0]
        reftitle = reftitle[reftitle['Land_Use_Mode'] >= 0]
        print(model, "Length of data:",len(reftitle))
        reftitle.to_csv(f, index=False)

def find_Y(date, pred):
    date = str(date)
    if '2019' in date: 
        accidents = pandas.read_csv("Excel & CSV Sheets/Accident Only Files/2019 Accidents.csv")
    else: 
        accidents = pandas.read_csv("Excel & CSV Sheets/Accident Only Files/2017+2018 Accidents.csv")
    accidents.Date = accidents.Date.astype(str)

    name = "gridLocations_" + date
    print(name)
    name = []

    for i, _ in enumerate(accidents.values):
        if accidents.Date.values[i] == date:
            name.append(accidents.Grid_Block.values[i])

    # We have our list of grid blocks with accidents for a given day, but there may be duplicates
    # We create a dictionary, using the list of grid blocks as keys
    # This automatically removes any duplicate values since dictionaries can't have duplicate keys
    # Then, we convert it back to a list, and wham! No more dupes
    name = list(dict.fromkeys(name))
    name.sort()
    name = pandas.DataFrame(name, columns= ['Grid_Block'])
    allblocks = list(pred.Grid_Block.unique())
    allblocks.sort()
    allblocks = pandas.DataFrame(allblocks, columns= ['Grid_Block'])
    pred['Y'] = 0
    print("Sum of accidents:", len(name))
    for i in allblocks.Grid_Block: 
        for j in name.Grid_Block: 
            if i == j: 
                # print(i, j)
                pred.Y[i] = 1 
    return pred

def network(data):

    X = data.ix[:, 0:(len(data.columns) - 2)].values
    Y = data['Y']
    print(X.shape)
    # print(X)
    # exit()
    model = Sequential()
    ##X.shape[1] is the number of columns inside of X.
    model.add(Dense(X.shape[1],input_dim=X.shape[1], activation='sigmoid'))


    model.add(Dense(int(X.shape[1] * .75), activation='sigmoid'))
    model.add(Dense(int(X.shape[1] / 2), activation='sigmoid'))
    model.add(Dense(int(X.shape[1] * .25), activation='sigmoid'))

    model.add(Dense(1, activation='sigmoid'))

    #   3. Compiling a model.
    model.compile(loss='mse',
                    optimizer='rmsprop', metrics=['accuracy'])
    print(model.summary())
    avg_holder = pandas.DataFrame(
                columns=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC", "TN", "FP", "FN", "TP"])
    for i in range(0, 50):
        X_train, X_test, y_train, y_test = train_test_split(
                    X, Y, test_size=0.30, random_state=42)

        # Patience is 15 epochs. If the model doesn't improve over the past 15 epochs, exit training
        patience = 30
        stopper = callbacks.EarlyStopping(monitor='acc', patience=patience)
        hist = model.fit(X_train, y_train, epochs=2000, batch_size=80, validation_data=(X_test, y_test), verbose=1,
                            callbacks=[stopper])
        scores = model.evaluate(X_train, y_train, batch_size=80)
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

        fpr, tpr, _ = roc_curve(y_test, predictions)
        roc_auc = auc(fpr, tpr)
        print('AUC: %f' % roc_auc)

        ##Confusion Matrix: 
        tn, fp, fn, tp = confusion_matrix(y_test, predictions_round).ravel()
        print(tn, fp, fn, tp)
        avg_holder.at[i, 'Train_Acc'] = scores[1] * 100
        avg_holder.at[i, 'Train_Loss'] = sum(hist.history['loss']) / len(hist.history['loss'])
        avg_holder.at[i, 'Test_Acc'] = accscore1 * 100
        avg_holder.at[i, 'Test_Loss'] = sum(hist.history['val_loss']) / len(hist.history['val_loss'])
        avg_holder.at[i, 'AUC'] = roc_auc
        avg_holder.at[i, 'TP'] = tp
        avg_holder.at[i, 'TN'] = tn
        avg_holder.at[i, 'FP'] = fp
        avg_holder.at[i, 'FN'] = fn
    avg_holder.to_csv("Excel & CSV Sheets/Forecasts/2017-5-16/Ensemble/ModelAverage.csv", sep=",", index=False)

filename = "Excel & CSV Sheets/Forecasts/2017-5-16/Ensemble/2017-5-16Prediction.csv"
# day = "2017-03-12"
# exit()
pred = pandas.read_csv(filename,sep= ",")

pred = shuffle(pred)
pred = shuffle(pred)
pred.to_csv("Excel & CSV Sheets/Forecasts/2017-5-16/Ensemble/2017-5-16PredictionShuffled.csv", sep=",", index=False)

pred = pred.drop(['Spatial_50-50', 'CutRan_50-50', 'FullGF_50-50', 'FullGF_75-25', 'FullGF_Test', 'FullRan_50-50', 'FullRan_75-25', 'FullRan_Test', 'Temporal_75-25', 'Temporal_Test'], axis=1)
# pred = find_Y(day ,pred)
# print(pred.head())
print("Sum of Y:",sum(pred.Y))
exit()

# pred.to_csv(filename, index=False)
network(pred)
