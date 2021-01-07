import keras
import pandas
from keras import Sequential
from keras.layers import TimeDistributed, Conv1D, MaxPooling1D, Flatten, LSTM, Dense, Conv2D, MaxPooling2D, Dropout, \
    ConvLSTM2D
from sklearn.model_selection import train_test_split


# fit and evaluate a model
def evaluate_model_v1(trainX, trainy, testX, testy):
    # channel = 29 (# of input variables)

    # define model
    n_timesteps, n_features, n_outputs = trainX.shape[0], trainX.shape[1], trainy.shape[0]
    # reshape data into time steps of sub-sequences
    n_steps, n_length = 24, trainX.shape[0]
    trainX = trainX.reshape((trainX.shape[0], n_steps, n_length, n_features))
    testX = testX.reshape((testX.shape[0], n_steps, n_length, n_features))
    # define model
    model = Sequential()
    model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu'),
                              input_shape=(None, n_length, n_features)))
    model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu')))
    model.add(TimeDistributed(Dropout(0.5)))
    model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model.add(TimeDistributed(Flatten()))
    model.add(LSTM(100))
    model.add(Dropout(0.5))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(n_outputs, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    model.fit(trainX, trainy, epochs=500, batch_size=5000, verbose=1)
    # evaluate model
    _, accuracy = model.evaluate(testX, testy, batch_size=5000, verbose=1)
    return accuracy


def evaluate_model_v2(trainX, trainy, testX, testy):
    # define model
    verbose, epochs, batch_size = 0, 25, 64
    n_timesteps, n_features, n_outputs = trainX.shape[0], trainX.shape[1], trainy.shape[0]
    print(n_timesteps, n_features, n_outputs)
    # reshape into subsequences (samples, time steps, rows, cols, channels)
    n_steps, n_length = 24, trainX.shape[0]
    trainX = trainX.reshape((trainX.shape[0], n_steps, 1, n_length, n_features))
    testX = testX.reshape((testX.shape[0], n_steps, 1, n_length, n_features))
    # define model
    model = Sequential()
    model.add(ConvLSTM2D(filters=64, kernel_size=(1,3), activation='relu',
                         input_shape=(n_steps, 1, n_length, n_features)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(n_outputs, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
    # evaluate model
    _, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
    return accuracy


data = pandas.read_csv("../Main Dir/Spatial Shift Negatives/SS Data 50-50 Split.csv")

newColumns = list(data.columns[1:(len(data.columns) + 1)])
X = data.iloc[:, 1:(len(data.columns) + 1)].values  # Our independent variables
Y = data.iloc[:, 0].values  # Our dependent variable
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=7)

evaluate_model_v1(X_train, y_train, X_test, y_test)