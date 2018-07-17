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
    # calldata = calldata.drop(['Rain', 'Drizzle', 'Light Drizzle', 'Light Rain',
    #                                   'Light Thunderstorms and Rain', 'Thunderstorm', 'Thunderstorms and Rain'], axis=1)

    # This section aggs the heavy rain/thunderstorm options into just 'Rainstorm'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Heavy Thunderstorms and Rain'] or 1 == calldata.loc[i, 'Heavy Rain']:
            calldata.loc[i, 'Rainstorm'] = 1
        else:
            calldata.loc[i, 'Rainstorm'] = 0

    # calldata = calldata.drop(['Heavy Rain', 'Heavy Thunderstorms and Rain'],axis=1)

    # This sections aggs the cloud options together into just 'Cloudy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Overcast'] or 1 == calldata.loc[i, 'Partly Cloudy'] or 1 == calldata.loc[
            i, 'Mostly Cloudy'] \
                or 1 == calldata.loc[i, 'Scattered Clouds']:
            calldata.loc[i, 'Cloudy'] = 1
        else:
            calldata.loc[i, 'Cloudy'] = 0

    # calldata = calldata.drop(['Overcast', 'Partly Cloudy', 'Mostly Cloudy', 'Scattered Clouds'],axis=1)

    # This section aggs the fog options into 'Foggy'
    for i, value in enumerate(calldata.values):
        if 1 == calldata.loc[i, 'Fog'] or 1 == calldata.loc[i, 'Light Freezing Fog'] or 1 == calldata.loc[i, 'Haze'] \
                or 1 == calldata.loc[i, 'Mist'] or 1 == calldata.loc[i, 'Patches of Fog'] or 1 == calldata.loc[
            i, 'Shallow Fog']:
            calldata.loc[i, 'Foggy'] = 1
        else:
            calldata.loc[i, 'Foggy'] = 0

    # calldata = calldata.drop(['Fog', 'Light Freezing Fog', 'Haze', 'Mist', 'Patches of Fog', 'Shallow Fog'], axis=1)

    # calldata = calldata.drop(
    #    ['Event_Unknown', 'Direction_Unknown', 'ENE', 'ESE', 'East', 'NE', 'NNE', 'NNW', 'NW',
    #              'North', 'SE', 'SSE', 'SSW', 'SW', 'South', 'Variable', 'WNW', 'WSW', 'West', 'Smoke'], axis=1)

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


def specify_stats(names, min, max, calldata):
    max += 1
    X = calldata.ix[:, min:max].values
    Y = calldata.ix[:, 0].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3, random_state=50)
    LogReg = LogisticRegression()
    # LogReg.fit(X, np.ravel(Y.astype(int)))
    LogReg.fit(X, Y)
    # X = X.reshape(-1, 1)
    # Odds ratio with single variables
    # print(np.exp(LogReg.coef_)[:, 0])
    print(LogReg.fit(X_train, Y_train))
    Y_pred = LogReg.predict(X_test)
    from sklearn.metrics import confusion_matrix
    confusion_matrix = confusion_matrix(Y_test, Y_pred)
    accscore = accuracy_score(Y_test, Y_pred)
    rescore = recall_score(Y_test, Y_pred, average='micro')
    print("Confusion Matrix: \n", confusion_matrix)
    print("Accuracy Score: ", accscore)
    print("Recall Score: ", rescore)
    print("Classification Report: \n", classification_report(Y_test, Y_pred))
    print("Printing Regression Results Table:\n")
    X2 = sm.add_constant(X)
    est_t = sm.Logit(Y, X2)
    est_t_fit = est_t.fit()
    print(est_t_fit.summary(xname=names))
    for i in range(min, max):
        # Odds ratio
        j = i - min
        print("Odds Ratio of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(LogReg.coef_)[0, j]))


def main():
    # weatherdata = easy_import_excel_file('KCHA_2016-10-01_2018-05-28.xlsx')
    # calldata = easy_import_excel_file('Oct16_Updated_Call_Log_with_Y.xlsx')
    # allcalldata = easy_import_excel_file('All_Call_Data.xlsx')
    # calldata = test.easy_import_excel_file('Updated_Call_Log1.xlsx')
    # binarydata = easy_import_excel_file('Binary_Data.xlsx')
    # calldata = easy_import_excel_file("Updated_Call_Log_with_Y.xlsx")

    # agg_rain(calldata, binarydata)

    # add_weather(calldata, weatherdata)
    # calldata = add_weather(allcalldata, weatherdata)

    # For loop fills blanks, event is the dummy maker for converting strings to binary values. Please remember to concat, Pete.
    # for col in calldata:
    #     fill_blanks(calldata, col)
    # event = pandas.get_dummies(calldata['Event'])
    # calldata = pandas.concat([calldata,event],axis=1)
    # calldata.drop(['Event'],axis=1,inplace=True)
    # print(calldata.head())
    # save_excel_file('File.xlsx','Sheet',calldata)
    # calldata = easy_import_excel_file('Agg_CallData.xlsx')

    # calldata = agg_options(calldata)

    # This shows all options for all columns
    # for column in calldata:
    #     print('Available Options for :',column)
    #     find_options(calldata, column)
    #     print ('\n\n')


    # Creates graph for the Regression count
    # graph = (calldata['Event'].value_counts())
    # events = ['Mostly Cloudy','Scattered Clouds','Overcast', 'Clear', 'Partly Cloudy', 'Light Rain','Haze', 'Rain',
    #     'Light Drizzle', 'Patches of Fog', 'Drizzle', 'Smoke' ,'Heavy Rain', 'Thunderstorms and Rain',  'Heavy Thunderstorms and Rain',
    #     'Light Thunderstorms and Rain',  'Fog', 'Thunderstorm', 'Shallow Fog', 'Unknown',  'Mist','Light Freezing Fog']
    # plot = sns.countplot(x='Event', data=calldata, palette='hls')
    # plot.set_xticklabels(events, rotation=90)
    # Graphing.plt.show()
    #
    # count =  test.pandas.DataFrame(calldata.groupby('Y').mean())

    # test.save_excel_file_with_format('Testing.xlsx', 'Mean values',count)
    #
    # fill_blanks(calldata,'Wind_Gust_Speed')
    # print(find_options(calldata, 'Wind_Gust_Speed'))
    # pprint.pprint(calldata['Wind_Gust_Speed'])
    # fill_blanks(calldata, 'Wind_Direction')

    # for i, value in enumerate(calldata.values):
    #     calldata.ix[i,'Weekday'] = value[2].strftime('%w')
    # nums = []
    for col in calldata:
        fill_blanks(calldata, col)

    # data = easy_import_excel_file('Call_data.xlsx')
    # mean_of_y = (data.groupby('Y').mean())
    # save_excel_file_with_format('Mean_of_Y.xlsx', 'Mean of Y', mean_of_y)

    # for i in range(7, 57):
    #     nums.append(i)

    # Original:
    calldata = calldata.drop(["Wind Direction in Degrees"], axis=1)
    # X = calldata.ix[:, 6:20].values


    # No C: Pressure
    # calldata = calldata.drop(["Pressure"], axis=1)
    # X = calldata.ix[:, 6:19].values

    # No BC
    # calldata = calldata.drop(["Pressure", "Humidity"], axis=1)
    # X = calldata.ix[:, 6:18].values

    # No BC
    # calldata = calldata.drop(["Pressure", "Humidity", "Dewpoint"], axis=1)
    # X = calldata.ix[:, 6:17].values

    # Y = calldata.ix[:, 0].values

    # X = calldata['Month'].values.reshape(5663, 1)
    # Y = calldata['Y'].values.reshape(5663, 1)
    #
    # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3, random_state=50)
    #
    # LogReg = LogisticRegression()
    # LogReg.fit(X, np.ravel(Y.astype(int)))
    # LogReg.fit(X, Y)

    # plt.scatter(X, LogReg.predict_proba(X)[:, 1])
    # plt.xlabel("Month")
    # xticks = ['October', 'November', 'December']
    # xticks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # plt.xticks(np.arange(10, 13), xticks)
    # plt.ylabel("Probability")


    # print(LogReg.fit(X_train, Y_train))
    # Y_pred = LogReg.predict(X_test)
    # from sklearn.metrics import confusion_matrix
    # confusion_matrix = confusion_matrix(Y_test, Y_pred)
    # accscore = accuracy_score(Y_test, Y_pred)
    # rescore = recall_score(Y_test, Y_pred, average='micro')
    # print("Confusion Matrix: \n", confusion_matrix)
    # print("Accuracy Score: ", accscore)
    # print("Recall Score: ", rescore)
    # print("Classification Report: \n", classification_report(Y_test, Y_pred))
    # printing the odds ratio by taking the exponent of the coefficient
    # for i in range(6, 20):
    #     j = i - 6
    #     print("Odds Ratio of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(LogReg.coef_)[0, j]))

    # No C: Pressure
    # for i in range(6, 19):
    #     j = i - 6
    #     print("Odds Ratio of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(LogReg.coef_)[0, j]))

    # No BC: Pressure, Humidity
    # for i in range(6, 18):
    #     j = i - 6
    #     print("Odds Ratio of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(LogReg.coef_)[0, j]))

    # No ABC: Pressure, Humidity, Dewpoint
    # for i in range(6, 17):
    #     j = i - 6
    #     print("Odds Ratio of :", '{0:25} {1:3} {2:4}'.format(calldata.columns[i], "is", np.exp(LogReg.coef_)[0, j]))



    # print("Printing Regression Results Table:\n")
    # X2 = sm.add_constant(X)
    # est_t = sm.Logit(Y, X2)
    # est_t_fit = est_t.fit()
    # print("\n")
    # Original:
    # print(est_t_fit.summary(xname=['Hour', 'Temperature', 'Dewpoint', 'Humidity', 'Wind Speed', 'Wind Gust Speed',
    #                                'Pressure', 'Weekday', 'Month', 'Clear', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy']))

    # No C: Pressure
    # print(est_t_fit.summary(xname=['Hour', 'Temperature', 'Dewpoint', 'Humidity', 'Wind Speed', 'Wind Gust Speed',
    #                                'Pressure', 'Weekday', 'Month', 'Clear', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy']))
    # No BC: Pressure, Humidity
    # print(est_t_fit.summary(xname=['Hour', 'Temperature', 'Dewpoint', 'Wind Speed', 'Wind Gust Speed', 'Weekday',
    #                               'Month', 'Clear', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy']))
    #
    # No ABC: Pressure, Humidity, Dewpoint
    # print(est_t_fit.summary(xname=['Hour', 'Temperature', 'Wind Speed', 'Wind Gust Speed', 'Weekday',
    #                               'Month', 'Clear', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy']))



    # Shows correlation between individual variables
    data = calldata[['Hour', 'Temperature', 'Dewpoint', 'Humidity','Pressure', 'Month', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy']]
    correlation = data.corr(method='pearson')
    print(correlation)
    sns.heatmap(correlation)
    plt.yticks(rotation = 0)
    plt.xticks(rotation = 90)
    plt.show()
    # save_excel_file('CorrelationData.xlsx', 'Cor Data', correlation)

    # test.save_excel_file_with_format('Call_Data.xlsx', 'Call Data', calldata)
    # test.get_col_names(weatherdata)
    # print(type(weatherdata))
    # print(weatherdata.head())
    # print(calldata.head())

    # print("Printing out ROC curve now.")
    # random_state = np.random.RandomState(0)
    # classifier = OneVsRestClassifier(svm.SVC(kernel="linear", probability=True, random_state=random_state))
    # Y_score = classifier.fit(X_train, Y_train).decision_function(X_test)
    # # Compute ROC curve and ROC area for each class
    # fpr = dict()
    # tpr = dict()
    # roc_auc = dict()
    # for i in range(7, 22):
    #     fpr[i], tpr[i], _ = roc_curve(Y_test, Y_score)
    #     roc_auc[i] = auc(fpr[i], tpr[i])
    #
    # fpr["micro"], tpr["micro"], _ = roc_curve(Y_test.ravel(), Y_score.ravel())
    # roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    # # Aggregate all false positive rates
    # all_fpr = np.unique(np.concatenate([fpr[i] for i in range(7, 22)]))
    # # Interpolate all ROC curves at this point
    # mean_tpr = np.zeros_like(all_fpr)
    # for i in range(7, 22):
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
    # plt.plot(fpr["micro"], tpr["micro"], label='micro-average ROC curve (area = {0:0.2f})'''.format(roc_auc["micro"]), linewidth=2)
    #
    # plt.plot(fpr["macro"], tpr["macro"], label='macro-average ROC curve (area = {0:0.2f})'''.format(roc_auc["macro"]), linewidth=2)
    #
    # for i in range(7, 22):
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

    # Y count graph
    # calldata["Y"].value_counts()
    # sns.countplot(x="Y", data=calldata, palette="hls")
    # plt.title("Y Count")
    # plt.show()

    # Whole Data Set
    # specify_stats(['Hour', 'Temperature', 'Dewpoint', 'Humidity', 'Wind Speed', 'Wind Gust Speed',
    #                   'Pressure', 'Weekday', 'Month', 'Clear', 'Rainy', 'Rainstorm', 'Cloudy', 'Foggy'],6,19,calldata)
    # # Hour
    # specify_stats(["Hour"], 6, 6, calldata)
    # # Temperature
    # specify_stats(["Temperature"], 7, 7, calldata)
    # # Dewpoint
    # specify_stats(["Dewpoint"], 8, 8, calldata)
    # # Humidity
    # specify_stats(["Humidity"], 9, 9, calldata)
    # # Wind Speed
    # specify_stats(["Wind Speed"], 10, 10, calldata)
    # # Wind Gust Speed
    # specify_stats(["Wind Gust Speed"], 11, 11, calldata)
    # # Pressure
    # specify_stats(["Pressure"], 12, 12, calldata)
    # # Weekday
    # specify_stats(["Weekday"], 13, 13, calldata)
    # # Month
    # specify_stats(["Month"], 14, 14, calldata)
    # # Clear
    # specify_stats(["Clear"], 15, 15, calldata)
    # # Rainy
    # specify_stats(["Rainy"], 16, 16, calldata)
    # # Rainstorm
    # specify_stats(["Rainstorm"], 17, 17, calldata)
    # # Cloudy
    # specify_stats(["Cloudy"], 18, 18, calldata)
    # # Foggy
    # specify_stats(["Foggy"], 19, 19, calldata)


if __name__ == "__main__":
    main()
