
import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential

filename = "../Excel & CSV Sheets/ Forecast Files/Forecast-for3-22-2019_2019-03-22_0.csv"
test = pandas.read_csv(filename,sep=",")
# test = shuffle(test)
# test = shuffle(test)
trained = "../Excel & CSV Sheets/Full Data MinMax Reduced.csv"
trainingset = pandas.read_csv(trained,sep=",")
columns = trainingset.columns.values[1:len(trainingset.columns.values)]
print(columns)
test2 = test[columns]
print(test2.columns.values)


# test2.to_csv("../Excel & CSV Sheets/ Forecast Files/Forecast Test.csv")

X_test = test2

print("Size of X_Test:", X_test.shape)

model = Sequential()
model.add(Dense(X_test.shape[1], input_dim=X_test.shape[1], activation='sigmoid'))
model.add(Dense(25, activation='sigmoid'))
model.add(Dropout(.1))
model.add(Dense(20, activation='sigmoid'))
model.add(Dense(18, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dropout(.1))
model.add(Dense(1, activation='sigmoid'))

#           3. Compiling a model.
model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
model.load_weights("model.h5")
# Okay, now let's calculate predictions.
predictions = model.predict(X_test)
test["Probability"] = predictions
# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]
test["Prediction"] = predictions_round
# print(rounded)
print("Head of predicitons: ", predictions[0:10])
print("Head of predictions_round: ", predictions_round[0:10])
print("Accidents predicted: ", sum(predictions_round[0:-1]))

test.to_csv("../Excel & CSV Sheets/ Forecast Files/Forecast-for3-22-2019_2019-03-22_0_reducedmodel.csv", sep=",",index=False)