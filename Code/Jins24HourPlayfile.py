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
# print(dataset.head())
dataset = dataset[dataset.columns[dataset.dtypes != object]]
calldata = calldata[calldata.columns[calldata.dtypes != object]]


X_train = calldata.ix[:,1:(len(calldata.columns)+1)].values
y_train = calldata.ix[:,0].values

X_test = dataset.ix[:,1:(len(dataset.columns)+1)].values
y_test = dataset.ix[:,0].values


print("X Train",X_train.shape)
print("Y Train",y_train.shape)
print("X Test",X_test.shape)
print("Y Test",y_test.shape)


model = Sequential()

# Fully connected layers are made using the Dense class. So, you can specify the number of neurons in the layer as the
# first argument, the initialization method as the second argument (using init) and the activation function using the
# activation argument.


# Adding the first layer, with 12 neurons, the input dimensions being the size of X,
# and the activation function as Rectifier. (Better performance than using sigmoid or tanh)
model.add(Dense(X_train.shape[1], input_dim=X_train.shape[1], activation='relu'))
# This layer has 8 neurons, with Rectifier still being the activation.
model.add(Dense(20,activation='relu'))
model.add(Dense(16,activation='relu'))
# Last layer has 1 neuron, so it can predict the class (diabetes or not)
model.add(Dense(1,activation='sigmoid'))

#           3. Compiling a model.
# Compiling the model.
# The loss function is used to evaluate a set of weights,and we're losing logarithmic loss with a binary classification
#   problem. This means we need to use binary cross entropy.
# The optimizer is used to search through different weights. We're using Adam before it's efficient and the default.
# Finally, we collect/report the classification accuracy as the metric.
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
print(model.summary())



#           4. Train that model on some data!
# Fitting the model
# Fitting the model means the training process will run for a fixed number of iterations through the data set. These
# iterations are referred to as epochs. We also set the number of instances evaluated before a weight update is
# performed in the network. (That's batch size, set with, you guessed it: batch_size.)
# The numbers used here are quite small, but the right number can be discovered via trial and error.

model.fit(X_train, y_train, epochs=10, batch_size=8)

# Evaluating the model
# This part tells us how well we've modeled the data set.
# The evaluate() function lets you evaluate the model on the training data set, passing it the same
# input/output used to train the model.

# That generates a prediction for each input/output pair and collects the scores, including the average loss and
# any metrics configured (like the accuracy)


#           5. Evaluate that model!
#This is evaluating the model, and printing the results of the epochs.
scores = model.evaluate(X_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# Okay, now let's calculate predictions.
predictions = model.predict(X_train[0:100])


# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]

accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded:",accscore1)

print(predictions)
print(predictions_round)
print(y_test)
generate_results(y_test, predictions_round)
plt.plot(predictions, color='red', label="Predictions")
plt.plot(y_train[0:100], color='blue', label="Y Values")
plt.plot(predictions_round[0:100], color='green', label = "Rounded Predictions")
plt.legend()
plt.show()