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

## The steps of creating a neural network or deep learning model ##
    # 1. Load Data
    # 2. Defining a neural network
    # 3. Compile a Keras model using an efficient numerical backend
    # 4. Train a model on some data.
    # 5. Evaluate that model on some data!

numpy.random.seed(7)


#           1. Load Data
# Loading the sample data in
# dataset = numpy.loadtxt(folderpath + "Excel & CSV Sheets/pima-indians-diabetes.csv", delimiter=",")

# Loading the accident data in
# dataset = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/Accident Data Full.xlsx")
# dataset = pandas.read_excel(folderpath + "Excel & CSV Sheets/2017+2018 Data/Accident Data Cut.xlsx")
dataset = pandas.read_csv(folderpath + "Excel & CSV Sheets/2017+2018 Data/Accident Data Cut.csv", sep=",")

# Splitting the data in input (x) and output (Y) variables
# X = dataset[:,0:]
# Y = dataset[:,8]

#Splitting the data with an excel file:
# dataset = dataset[dataset.columns[dataset.dtypes != object]]
# dataset = dataset.drop(['Latitude', 'Longitude', 'Temperature', 'Daily_Avg_Temp', 'Monthly_Avg_Temp', 'Dewpoint'], axis=1)
# dataset = dataset.dropna()
# dataset = dataset.drop(dataset[dataset.Speed_Limit < 0].index)
# dataset = dataset.drop(['Illumination'],axis=1)
print(dataset.shape)

# dataset = shuffle(dataset)
#
# dataset = dataset.drop(["Dewpoint"], axis=1)
X = dataset.ix[:,1:(len(dataset.columns)+1)].values
print(X)

Y = dataset.ix[:,0].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)

print(X.shape)
print(Y.shape)

#           2. Defining a Neural Network
#creating the model
model = Sequential()

# Fully connected layers are made using the Dense class. So, you can specify the number of neurons in the layer as the
# first argument, the initialization method as the second argument (using init) and the activation function using the
# activation argument.


# Adding the first layer, with 12 neurons, the input dimensions being the size of X,
# and the activation function as Rectifier. (Better performance than using sigmoid or tanh)
model.add(Dense(31, input_dim=X_train.shape[1], activation='relu'))
# This layer has 8 neurons, with Rectifier still being the activation.
model.add(Dense(8,activation='sigmoid'))
# Last layer has 1 neuron, so it can predict the class (diabetes or not)
model.add(Dense(1,activation='sigmoid'))

#           3. Compiling a model.
# Compiling the model.
# The loss function is used to evaluate a set of weights,and we're losing logarithmic loss with a binary classification
#   problem. This means we need to use binary cross entropy.
# The optimizer is used to search through different weights. We're using Adam before it's efficient and the default.
# Finally, we collect/report the classification accuracy as the metric.
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
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
predictions = model.predict(X_test)
print(predictions)

# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]
# print(rounded)
accscore1 = accuracy_score(y_test, predictions_round)
print("Rounded:",accscore1)


print(len(predictions))
print(len(y_test))
generate_results(y_test, predictions_round)
# plt.plot(predictions[0:100], color='red', label="Predictions")
plt.plot(y_test[0:100], color='blue', label="Y Values")
plt.plot(predictions_round[0:100], color='green', label = "Rounded Predictions")
plt.legend()
plt.show()