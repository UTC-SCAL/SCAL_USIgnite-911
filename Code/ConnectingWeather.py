import numpy as np
import pandas
import seaborn as sns
import sklearn
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from pylab import rcParams
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime, timedelta, date

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


def find_options(calldata, column):
    list = calldata[column].unique()

    try:
        list.sort()
    except:
        print("This list is not Sortable")
    print(*list, sep="\n")


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
    y, x = patsy.dematrices("Testing", X, calldata, return_type="dataframe")
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3)
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

    print("Printing Description:")
    for i, value in enumerate(calldata.columns.values[mini:maxi]):
        print("________________________")
        print(calldata[value].describe())
        print("________________________")

    print("Printing Histogram")
    calldata.hist()
    pl.show()

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


# Aggregate dummy variables
def agg_options(calldata):
    # event = pandas.get_dummies(calldata['Event'])
    # calldata = pandas.concat([calldata,event],axis=1)
    # calldata.drop(['Event'],axis=1,inplace=True)

    # conditions = pandas.get_dummies(calldata['Conditions'])
    # calldata = pandas.concat([calldata, conditions], axis=1)
    # calldata.drop(['Conditions'], axis=1, inplace=True)

    header_list = ("Y", 'Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Address', 'City', 'Event', 'Conditions',
                   'Hour', 'Temperature', 'Dewpoint', 'Humidity', 'Month', 'Visibility', 'Clear', 'Rain', 'Snow',
                   'Cloudy', 'Foggy')

    calldata = calldata.reindex(columns=header_list)
    # print(calldata.head())

    for i, value in enumerate(calldata.values):
        # clear = "Clear"
        # clear = re.IGNORECASE
        # print(clear)
        # string = calldata.Event.values[i]
        # print("Is Clear in ?", calldata.Event.values[i])
        # # print(string.find(clear))
        # string1 = calldata.Conditions.values[i]
        # print("Is Clear in ?",calldata.Conditions.values[i])
        # print(string1.find(clear))

        if "clear" in calldata.Event.values[i] or "clear" in calldata.Conditions.values[i] \
                or "Clear" in calldata.Event.values[i] or "Clear" in calldata.Conditions.values[i]:
            calldata.Clear.values[i] = 1
        else:
            calldata.Clear.values[i] = 0

        if "rain" in calldata.Event.values[i] or "rain" in calldata.Conditions.values[i] \
                or "Rain" in calldata.Event.values[i] or "Rain" in calldata.Conditions.values[i]:
            calldata.Rain.values[i] = 1
        else:
            calldata.Rain.values[i] = 0

        if "snow" in calldata.Event.values[i] or "snow" in calldata.Conditions.values[i] \
                or "Snow" in calldata.Event.values[i] or "Snow" in calldata.Conditions.values[i]:
            calldata.Snow.values[i] = 1
        else:
            calldata.Snow.values[i] = 0

        if "cloudy" in calldata.Event.values[i] or "cloudy" in calldata.Conditions.values[i] \
                or "Cloudy" in calldata.Event.values[i] or "Cloudy" in calldata.Conditions.values[i] \
                or "overcast" in calldata.Event.values[i] or "overcast" in calldata.Conditions.values[i] \
                or "Overcast" in calldata.Event.values[i] or "Overcast" in calldata.Conditions.values[i]:
            calldata.Cloudy.values[i] = 1
        else:
            calldata.Cloudy.values[i] = 0

        if "fog" in calldata.Event.values[i] or "foggy" in calldata.Conditions.values[i] \
                or "Fog" in calldata.Event.values[i] or "Foggy" in calldata.Conditions.values[i]:
            calldata.Foggy.values[i] = 1
        else:
            calldata.Foggy.values[i] = 0
    # print(calldata.head())
    # save_excel_file(
    #     "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/2018 Accident Report List Agg Options.xlsx",
    #     "DarkSky Weather", calldata)
    save_excel_file(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017 Data/2017 CallData Agg.xlsx",
        "DarkSky Weather", calldata)


def graph_maker(calldata, wsdata):
    ordered = calldata.groupby(
        [pandas.to_datetime(calldata.Date.values).strftime('%Y-%m-%d')])['Temperature'].mean().reset_index(
        name='DailyAverage')
    # print(ordered.head())
    x = ordered.index.values
    y = ordered.DailyAverage.values

    orderedws = wsdata.groupby(
        [pandas.to_datetime(wsdata.Date.values).strftime('%Y-%m-%d')])['Temperature_in_F'].mean().reset_index(
        name='DailyAverage')
    # print(orderedws.head())


    x1 = orderedws.index.values
    y1 = orderedws.DailyAverage.values
    xdif = []

    for i, value in enumerate(ordered.DailyAverage.values):
        xdif.append(abs((ordered.DailyAverage.values[i]) - (orderedws.DailyAverage.values[i])))

    # print(orderedws.index.values)
    plt.plot(x, y, label='DarkSky', linewidth=2)
    plt.plot(x1, y1, label='Stations', linewidth=2)
    # plt.plot(xdif, y, label='Difference')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title('Temperature Comparison')
    # plt.legend()
    # plt.show()

    diffframe = pandas.DataFrame(columns=['Day', 'Difference'])
    diffframe.Day = ordered.index.values
    diffframe.Difference = xdif

    print(diffframe.values)

    plt.plot(diffframe.Day.values, diffframe.Difference.values, label='Difference', linewidth=2)
    # plt.xlabel('Date')
    # plt.ylabel('Temperature Difference')
    # plt.title('Temperature Comparison')
    plt.legend()
    plt.show()


def main():
    # Link for example: https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

    # calldata = easy_import_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017 Data/2017 CallData Raw.xlsx")
    # agg_options(calldata)

    # MAIN CallData 2018 #
    calldata = easy_import_excel_file(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/2018 Accident Report List Agg Options.xlsx")

    # Testing  #
    # calldata = easy_import_excel_file("")
    # calldata.drop(["Clear", "Rain", "Snow", "Cloudy", "Foggy"], axis=1, inplace=True)
    # calldata.drop([""], axis=1, inplace=True)
    #

    mini = calldata.columns.get_loc("Hour")
    maxi = len(calldata.columns)

    # Add in the intercept for the Jin table
    names = ["Intercept"]
    for i in range(mini, maxi):
        names.append(calldata.columns.values[i])

    # for i, value in enumerate(calldata.values[0:10]):
    #     str_date = str(calldata.Date.values[i])
    #     dateof = date.strptime(str_date, '%m/%d/%Y')
    #     monthof = dateof.month
    #     print(monthof)

    # Pearson tests #
    # X = calldata.ix[:, mini:maxi].values
    # Y = calldata.ix[:, 0].values
    # for column in calldata.columns[mini:maxi]:
    #     # print(calldata[column])
    #     print("Pearson for :", column, "is", pearsonr(calldata[column], Y))
        # print(len(calldata[column]))


    # Y count graph #
    # calldata["Y"].value_counts()
    # sns.countplot(x="Y", data=calldata, palette="hls")
    # plt.title("Y Count")
    # plt.show()

    # Printing Variable Importance #
    # X = calldata.values[:, mini:maxi]
    # Y = calldata.values[:, 0]
    # Y = Y.astype('int')
    # #Build a forest and compute the feature importances
    # forest = ExtraTreesClassifier()
    #
    # forest.fit(X, Y)
    # importances = forest.feature_importances_
    # std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
    # indices = np.argsort(importances)[::-1]
    #
    # # Print the feature ranking
    # print("Feature ranking:")
    # features_list = calldata.columns.values[mini:maxi]
    # features_list.tolist()
    # for f in range(X.shape[1]):
    #     print("%d. %s (%f)" % (f + 1, features_list, importances[indices[f]]))
    #
    #
    # # Plot the feature importances of the forest
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title("Feature Importance")
    # plt.bar(range(X.shape[1]), importances[indices], color="r", yerr=std[indices], align="center")
    # plt.xticks(range(X.shape[1]), features_list)
    # plt.xlim([-1, X.shape[1]])
    # plt.xlabel("Feature Name")
    # plt.ylabel("Variable Importance Level")
    # plt.show()


    # Call the specify_stats method, running Logistic Regression Analysis and making the Jin Table
    LogReg = specify_stats(names, mini, maxi, calldata)


if __name__ == "__main__":
    main()
