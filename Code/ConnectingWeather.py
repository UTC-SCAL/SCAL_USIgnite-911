import pprint
import seaborn as sns
import pandas
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, accuracy_score, recall_score, roc_curve, auc, roc_auc_score
import statsmodels.api as sm
from sklearn.preprocessing import label_binarize
import scikitplot as skplt
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm, metrics
import scipy.stats as stats
from scipy import interp
import sklearn
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier

# %matplotlib inline
rcParams['figure.figsize'] = 10, 8
sns.set_style('whitegrid')


# sns.set(style='white')
# sns.set(style='whitegrid', color_codes=True)

def easy_import_excel_file(file_name):
    data_file_name = pandas.read_excel(file_name)
    print('Import complete')
    return data_file_name

    # Saving this set to a new excel sheet, when you're done


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def save_excel_file_with_format(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy', )
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    format1 = workbook.add_format({'num_format': '-#\.######'})
    # format2 = workbook.add_format({'num_format': 'd-mmm-yy'})
    # format3 = workbook.add_format({'num_format': 'hh:mm:ss'})
    format4 = workbook.add_format({'num_format': '#\.######'})
    worksheet.set_column('B:B', 10, format4)
    worksheet.set_column('C:C', 10, format1)
    # worksheet.set_column('D:D', 25, format2)
    # worksheet.set_column('E:E', 10, format3)
    writer.save()


def agg_options(calldata):
    # This section aggs the rainy conditions into just 'Rainy'
    for i, value in enumerate(calldata.values):
        # print (i, value)
        if 1 == calldata.loc[i, 'Rain'] or 1 == calldata.loc[i, 'Light Rain'] or \
                        1 == calldata.loc[i, 'Drizzle'] or 1 == calldata.loc[i, 'Light Drizzle'] \
                or 1 == calldata.loc[i, 'Light Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Thunderstorm'] \
                or 1 == calldata.loc[i, 'Thunderstorms and Rain']:
            calldata.loc[i, 'Rainy'] = 1
        else:
            calldata.loc[i, 'Rainy'] = 0
    # This section aggs the heavy rain/thunderstorm options into just 'Rainstorm'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Heavy Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Heavy Rain']:
            calldata.loc[i, 'Rainstorm'] = 1
        else:
            calldata.loc[i, 'Rainstorm'] = 0
    # This sections aggs the cloud options together into just 'Cloudy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Overcast'] or 1 == calldata.loc[i, 'Partly Cloudy'] or 1 == calldata.loc[
            i, 'Mostly Cloudy'] \
                or 1 == calldata.loc[i, 'Scattered Clouds']:
            calldata.loc[i, 'Cloudy'] = 1
        else:
            calldata.loc[i, 'Cloudy'] = 0
    # This section aggs the fog options into 'Foggy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Fog'] or 1 == calldata.loc[i, 'Light Freezing Fog'] or \
                        1 == calldata.loc[i, 'Haze'] \
                or 1 == calldata.loc[i, 'Mist'] or 1 == calldata.loc[i, 'Patches of Fog'] or \
                        1 == calldata.loc[i, 'Shallow Fog']:
            calldata.loc[i, 'Foggy'] = 1
        else:
            calldata.loc[i, 'Foggy'] = 0

    save_excel_file('Agg_CallData.xlsx', 'Aggregated Call Log', calldata)


def add_weather(calldata, weatherdata):
    print('Call Info: ')
    for i, value in enumerate(calldata.values):
        header_list = (
            'Date', 'Time', 'Problem', 'Hour', 'Temperature', 'Dewpoint', 'Humidity',
            'Wind Speed', 'Wind Gust Speed', 'Wind Direction in Degrees', 'Wind Direction', 'Pressure', 'Event',
            'Weekday', 'Month')
        date = value[0].strftime('%Y-%m-%d')
        time = value[1]
        hour = value[2]
        hour = int(hour)
        day = value[0].strftime('%w')
        month = value[0].strftime('%-m')
        calldata = calldata.reindex(columns=header_list)

        for j, info in enumerate(weatherdata.values):
            weatherdate = info[0].strftime('%Y-%m-%d')
            weathertime = info[1].strftime('%-H:%M:%S')
            weatherhour = info[1].strftime('%-H')
            weatherhour = int(weatherhour)

            if (weatherdate == date) and (weatherhour == hour):
                calldata.loc[i, 'Temperature'] = weatherdata.loc[j, 'temperature']
                calldata.loc[i, 'Dewpoint'] = weatherdata.loc[j, 'dewpoint']
                calldata.loc[i, 'Humidity'] = weatherdata.loc[j, 'humidity']
                calldata.loc[i, 'Wind Speed'] = weatherdata.loc[j, 'wind_speed']
                calldata.loc[i, 'Wind Gust Speed'] = weatherdata.loc[j, 'wind_gust_speed']
                calldata.loc[i, 'Wind Direction in Degrees'] = weatherdata.loc[j, 'wind_dir_degrees']
                calldata.loc[i, 'Wind Direction'] = weatherdata.loc[j, 'wind_dir']
                calldata.loc[i, 'Pressure'] = weatherdata.loc[j, 'pressure']
                calldata.loc[i, 'Event'] = weatherdata.loc[j, 'event']
                # calldata.loc[i, 'Conditions'] = weatherdata.loc[j, 'conditions']
                calldata.loc[i, 'Weekday'] = day
                calldata.ix[i, 'Month'] = month

                # print(weatherdate, date, " : ", weathertime, time, ";",)
    save_excel_file_with_format('All_call_with_Weather.xlsx', 'Updated Call Log', calldata)
    return calldata


def find_y(calldata):
    for i, value in enumerate(calldata.values):
        if 'No Injuries' in calldata.loc[i, 'Problem'] or 'Unknown Injuries' in calldata.loc[
            i, 'Problem'] or 'Delayed' in calldata.loc[i, 'Problem']:
            calldata.ix[i, 'Y'] = 0
        else:
            calldata.ix[i, 'Y'] = 1
    save_excel_file_with_format('Oct16_Updated_Call_Log_with_Y.xlsx', 'Updated Call Log', calldata)
    return calldata


def find_options(calldata, column):
    list = calldata[column].unique()

    try:
        list.sort()
    except:
        print("This list is not Sortable")
    print(*list, sep="\n")


def fill_blanks(calldata, column_to_fill):
    for i, value in enumerate(calldata[column_to_fill].values):
        if pandas.isnull(calldata.loc[i, column_to_fill]) == True or calldata.loc[i, column_to_fill] == None:
            calldata.ix[i, column_to_fill] = 0


def find_occur(calldata, col):
    occured = 0
    for i, value in enumerate(calldata.values):
        if value[0] == 1:
            occured += 1
    print("The number of injury occurrences is: ", occured)
    total = len(calldata)
    print("The total number of records is: ", total)
    odd = ((occured / (total - occured)) * 100.00)
    print("The odds are: ", "%.2f" % odd)


def specify_stats(names, mini, maxi, calldata):
    X = calldata.ix[:, mini:maxi].values
    Y = calldata.ix[:, 0].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3, random_state=50)
    LogReg = LogisticRegression()
    LogReg.fit(X, Y)
    print(LogReg.fit(X_train, Y_train))
    Y_pred = LogReg.predict(X_test)
    from sklearn.metrics import confusion_matrix
    confusion_matrix = confusion_matrix(Y_test, Y_pred)
    accscore = sklearn.metrics.accuracy_score(Y_test, Y_pred)
    rescore = sklearn.metrics.recall_score(Y_test, Y_pred, average='micro')
    print("Confusion Matrix: \n", confusion_matrix)
    print("Accuracy Score: ", accscore)
    print("Recall Score: ", rescore)
    print("Classification Report: \n", sklearn.metrics.classification_report(Y_test, Y_pred))
    print("Printing Regression Results Table:\n")
    X2 = sm.add_constant(X)
    est_t = sm.Logit(Y, X2)
    est_t_fit = est_t.fit()

    print(est_t_fit.summary(xname=names))
    for i in range(mini, maxi + 1):
        # Odds ratio
        j = i - mini + 1
        # print("P Value of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(est_t_fit.pvalues)[j]))
        try:
            print("Odds Ratio of :",
                  '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(est_t_fit.params)[j]))
        except:
            print('End of Odds List')
            break
            # print("\t\t\t\t\t\t\t\tParams: ",est_t_fit.params[j])

    # Printing an ROC curve #
    # print("Printing out ROC curve")
    # random_state = np.random.RandomState(0)
    # classifier = OneVsRestClassifier(svm.SVC(kernel="linear", probability=True, random_state=random_state))
    # Y_score = classifier.fit(X_train, Y_train).decision_function(X_test)
    # # Compute ROC curve and ROC area for each class
    # fpr = dict()
    # tpr = dict()
    # roc_auc = dict()
    # for i in range(7, 20):
    #     fpr[i], tpr[i], _ = roc_curve(Y_test, Y_score)
    #     roc_auc[i] = auc(fpr[i], tpr[i])
    #
    # fpr["micro"], tpr["micro"], _ = roc_curve(Y_test.ravel(), Y_score.ravel())
    # roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    # # Aggregate all false positive rates
    # all_fpr = np.unique(np.concatenate([fpr[i] for i in range(7, 20)]))
    # # Interpolate all ROC curves at this point
    # mean_tpr = np.zeros_like(all_fpr)
    # for i in range(7, 20):
    #     mean_tpr += interp(all_fpr, fpr[i], tpr[i])
    # # Average it and compute AUC
    # mean_tpr /= 14
    #
    # fpr["macro"] = all_fpr
    # tpr["macro"] = mean_tpr
    # roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    #
    # # Plot all ROC curves
    # plt.figure()
    # plt.plot(fpr["micro"], tpr["micro"],
    #          label='micro-average ROC curve (area = {0:0.2f})'''.format(roc_auc["micro"]), linewidth=2)
    #
    # plt.plot(fpr["macro"], tpr["macro"],
    #          label='macro-average ROC curve (area = {0:0.2f})'''.format(roc_auc["macro"]), linewidth=2)
    #
    # for i in range(7, 20):
    #     plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i]))
    #
    # plt.plot([0, 1], [0, 1], 'k--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Some extension of Receiver operating characteristic to multi-class')
    # plt.legend(loc="lower right")
    # plt.show()

    print("\n")
    print("Printing EST:", est_t_fit, "Printing LogReg:", LogReg)
    return LogReg


def odds(mini, maxi, LogReg, calldata):
    for i in range(mini, maxi):
        # Odds ratio
        j = i - mini
        print("Odds Ratio of :",
              '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is 0:.4f" % np.exp(LogReg.coef_)[0, j]))


def main():
    calldata = easy_import_excel_file('Agg_CallData2017_NoBlanks.xlsx')

    # Drop certain values for testing
    calldata = calldata.drop(["Wind Speed", "Wind Gust Speed", "Wind Direction in Degrees",
                              "Pressure", "Weekday", "Clear"], axis=1)

    mini = 6
    maxi = len(calldata.columns)

    # Add in the intercept for the Jin table
    names = ['Intercept']
    for i in range(mini, maxi):
        names.append(calldata.columns.values[i])


# Modifying Independent Variable Inputs #
    # No Humidity (No BC)
    # calldata = calldata.drop(["Humidity"], axis=1)

    # No Humidity, Dewpoint (No ABC)
    # calldata = calldata.drop(["Humidity", "Dewpoint"], axis=1)


# Y count graph #
    # calldata["Y"].value_counts()
    # sns.countplot(x="Y", data=calldata, palette="hls")
    # plt.title("Y Count")
    # plt.show()

# Printing Variable Importance #
#     X = calldata.values[:, mini:maxi]
#     Y = calldata.values[:, 1]
#     Y = Y.astype('int')
#     # Build a forest and compute the feature importances
#     forest = ExtraTreesClassifier()
#
#     forest.fit(X, Y)
#     importances = forest.feature_importances_
#     std = np.std([tree.feature_importances_ for tree in forest.estimators_],
#                  axis=0)
#     indices = np.argsort(importances)[::-1]
#
#     # Print the feature ranking
#     print("Feature ranking:")
#     features_list = calldata.columns.values[mini:maxi]
#     features_list.tolist()
#     for f in range(X.shape[1]):
#         print("%d. %s (%f)" % (f + 1, features_list[f], importances[indices[f]]))
#
#
#     # Plot the feature importances of the forest
#     plt.figure()
#     plt.rcParams.update({'font.size': 20})
#     plt.title("Feature Importance")
#     plt.bar(range(X.shape[1]), importances[indices],
#            color="r", yerr=std[indices], align="center")
#     plt.xticks(range(X.shape[1]), features_list)
#     plt.xlim([-1, X.shape[1]])
#     plt.xlabel("Feature Name")
#     plt.ylabel("Variable Importance Level")
#     plt.show()


# Call the specify_stats method, running Logistic Regression Analysis and making the Jin Table
    LogReg = specify_stats(names, mini, maxi, calldata)


if __name__ == "__main__":
    main()
