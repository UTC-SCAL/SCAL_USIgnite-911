# Standard imports for linear regression
# For more examples of regression: https://jakevdp.github.io/PythonDataScienceHandbook/05.06-linear-regression.html
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import sklearn
import sklearn.cross_validation
from sklearn.linear_model import LinearRegression
from scipy.stats import chisquare
import statsmodels.formula.api as smf
import statsmodels.api as sm

# # A scatter plot, slope 2, intercept -5
# # A simple straight-line fit to data #
# rng = np.random.RandomState(1)
# x = 10 * rng.rand(50)
# y = 2 * x - 5 + rng.rand(50)
# plt.scatter(x, y)
# # plt.show()
#
# # To fit this data, use Scikit LinearRegression estimator
# model = LinearRegression(fit_intercept=True)
# model.fit(x[:, np.newaxis], y)
#
# xfit = np.linspace(0, 10, 1000)
# yfit = model.predict(xfit[:, np.newaxis])
#
# plt.scatter(x, y)
# plt.plot(xfit, yfit)
# plt.show()
# # The slope and intercept of the data are contained in the model's fit parameters
# # In Scikit-Learn, these parameters are always marked by a trailing underscore
# # Ex: coefficients - coef_, intercept - intercept_
# print("Model Slope: ", model.coef_[0])
# print("Model Intercept: ", model.intercept_)


# # Below is the linear regression example using the diabetes data set #
#
# from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score
# # Load the diabetes dataset
# diabetes = datasets.load_diabetes()
#
# # Use only one feature
# diabetes_X = diabetes.data[:, np.newaxis, 2]
#
# # Split the data into training/testing sets
# diabetes_X_train = diabetes_X[:-20]
# diabetes_X_test = diabetes_X[-20:]
# # Split the targets into training/testing sets
# diabetes_y_train = diabetes.target[:-20]
# diabetes_y_test = diabetes.target[-20:]
#
# # Create linear regression object
# regr = linear_model.LinearRegression()
# # Train the model using the training sets
# regr.fit(diabetes_X_train, diabetes_y_train)
# # Make predictions using the testing set
# diabetes_y_pred = regr.predict(diabetes_X_test)
#
# # The coefficients
# print('Coefficients: \n', regr.coef_)
# # The mean squared error
# print("Mean squared error: %.2f" % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# # Explained variance score: 1 is perfect prediction
# print('Variance (r-squared) score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))
#
# # Plot outputs
# plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
# plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)
# plt.xticks(())
# plt.yticks(())
# plt.show()

# Boston Housing Data Set #
# Example from: http://bigdata-madesimple.com/how-to-run-linear-regression-in-python-scikit-learn/
import scipy.stats as stats
from sklearn.datasets import load_boston
boston = load_boston()

# explore the keys of the dictionary
boston.keys()
print(boston.data.shape)

# print the feature names of the boston data set
# print(boston.feature_names)

# Exercise goal: predict the housing prices in boston region using given features
# Print a description of the boston data set
print(boston.DESCR)

# Convert the data into a pandas data frame
bos = pd.DataFrame(boston.data)
# This prints the heads, but doesn't show column names, just numbers
# print(bos.head())
# Replace the column heads with actual names
bos.columns = boston.feature_names
print(bos.head())

# Housing prices
# print(boston.target[:5])
# Add these target prices to the bos data frame
bos["PRICE"] = boston.target

# Here, fit a linear regression model and predict the Boston housing prices
# Use least squares method as the way to estimate coefficients
# Y = boston housing price ("target" in python)
# X = all the other features (independent variables)

X = bos.drop("PRICE", axis = 1)
# Create a LinearRegression object
lm = LinearRegression()
# To see all available functions for Linear Regression, type LinearRegression.
# You can scroll through the list that appears after the "."
# Key functions to remember:
    # lm.fit(): fits a linear model
    # lm.predict(): predicts Y using linear model with estimated coefficients
    # lm.score(): returns r-squared value
    # .coef_ gives the coefficients, .intercept_ gives the estimated intercepts

# Using all 13 parameters to fit a linear regression model
lm.fit(X, bos.PRICE)

# Print an OLS Regression Results table (Jin Table)
results = sm.OLS(bos.PRICE, X).fit()
print(results.summary())

# Print the intercept and number of coefficients
print("Estimated intercept coefficient: ", lm.intercept_)
print("Number of coefficients: ", len(lm.coef_))



# Construct a data frame that contains features and estimated coefficients
boston_table = pd.DataFrame(list(zip(X.columns, lm.coef_)), columns = ["Features", "Estimated Coefficients"])
print(boston_table)
# The table shows that there's a high correlation between RM and prices
# Make a scatter plot between true housing prices and true RM
plt.scatter(bos.RM, bos.PRICE)
plt.xlabel("Average number of rooms per dwelling (RM)")
plt.ylabel("Housing Price")
plt.title("Relationship between RM and Price")
plt.show()
# The plot shows a positive correlation between RM and housing prices

# Predicting Prices
# Now, we calculate the predicted prices using lm.predict, then display the first 5 housing prices
print("First 5 Housing Price Predictions\n\t", lm.predict(X)[0:5])

# Make a scatter plot to compare the true prices and the predicted prices
plt.scatter(bos.PRICE, lm.predict(X))
plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted Prices: $\hat{Y}_i$")
plt.title("Prices vs Predicted Prices: $Y_i$ vs $\hat{Y}_i$")
plt.show()

# Nice graph, but there is some error in the prediction as housing prices increase
# Calculate the mean squared error
mseFull = np.mean((bos.PRICE - lm.predict(X)) ** 2)
print("Mean Squared Error: ", mseFull)
# However, this is only the MSE for one feature, which isn't a good thing to do

# Training and validation data sets
# Divide your data sets randomly, not by a specified amount
X_train, X_test, Y_train, Y_test = \
    sklearn.cross_validation.train_test_split(X, bos.PRICE, test_size = 0.33, random_state = 5)
print("X_train shape: ", X_train.shape)
print("X_test shape: ", X_test.shape)
print("Y_train shape: ", Y_train.shape)
print("Y_test shape: ", Y_test.shape)

# Build a linear regression model using the train-test data sets
lm_train = LinearRegression()
lm_train.fit(X_train, Y_train)

pred_train = lm_train.predict(X_train)
pred_test = lm_train.predict(X_test)


# Now, calculate the MSE for training and test data
print("Fit a model X_train, and calculate MSE with Y_train:",
      np.mean((Y_train - lm_train.predict(X_train)) ** 2))
print("Fit a model X_train, and calculate MSE with X_test, Y_test:",
      np.mean((Y_test - lm_train.predict(X_test)) ** 2))

# Residual Plots
# These are good for visualizing errors in your data
# If you've done a good job, your data should be randomly scattered around line zero
# If you see a structure in your data, that means your model is not capturing something
    # Such as, not considering interaction between 2 variables, or you are measuring time dependent data
    # If you see a structure in your data, go back and check your parameters
plt.scatter(lm_train.predict(X_train), lm_train.predict(X_train) - Y_train, c = "b", s = 40, alpha = 0.5)
plt.scatter(lm_train.predict(X_test), lm_train.predict(X_test) - Y_test, c = "g", s = 40)
plt.hlines(y = 0, xmin = 0, xmax = 50)
plt.title("Residual Plot using training (blue) and test (green) data")
plt.ylabel("Residuals")
plt.show()