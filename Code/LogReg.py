import pprint
import seaborn as sns
import pandas
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from pylab import rcParams
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.ensemble import ExtraTreesClassifier


def make_unknown(calldata, column):
    for i, value in enumerate(calldata[column].values):
        if (calldata.loc[i, column]) is None:
            calldata.ix[i, column] = 'Unknown'

def easy_import_excel_file(file_name):
    data_file_name = pandas.read_excel(file_name)
    print("Import Complete")
    return data_file_name

def save_excel_file_with_format(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy', )
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    format1 = workbook.add_format({'num_format': '-#\.######'})
    format2 = workbook.add_format({'num_format': 'd-mmm-yy'})
    format3 = workbook.add_format({'num_format': 'hh:mm:ss'})
    format4 = workbook.add_format({'num_format': '#\.######'})
    worksheet.set_column('C:C', 10, format4)
    worksheet.set_column('D:D', 10, format1)
    worksheet.set_column('E:E', 25, format2)
    worksheet.set_column('F:F', 10, format3)
    writer.save()


def fill_blanks(calldata, column_to_fill):
    for i, value in enumerate(calldata[column_to_fill].values):
        if pandas.isnull(calldata.loc[i, column_to_fill]) == True or calldata.loc[i, column_to_fill] == None:
            calldata.ix[i, column_to_fill] = -100


def main():
    # header_list = ('Y','Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Hour', 'Temperature', 'Dewpoint', 'Humidity',
    #                'Wind_Speed', 'Wind_Gust_Speed', 'Wind_Direction_in_Degrees', 'Wind_Direction', 'Pressure', 'Event',
    #                'Conditions', 'Weekday', 'Month')
    # calldata = test.easy_import_excel_file('Call_Data.xlsx')
    # calldata = calldata.reindex(columns=header_list)
    # event = pandas.get_dummies(calldata['Event'])
    # calldata.drop(['Event'],axis=1,inplace=True)
    # for i, value in enumerate(calldata.values):
    #     calldata.ix[i,'Weekday'] = value[3].strftime('%w')

    # data =(pandas.get_dummies(data))
    # make_unknown(calldata,'Wind_Direction')
    # wind = pandas.get_dummies(calldata['Wind_Direction'])
    # calldata.drop(['Wind_Direction'],axis=1,inplace=True)
    # calldata = pandas.concat([calldata, event, wind], axis=1)
    #
    # pprint.pprint(calldata.head())
    # save_excel_file_with_format('Binary_Data.xlsx', 'Call Data', calldata)

    # nums = []
    #
    #
    # for i in range(7, 57):
    #     nums.append(i)
    #
    # print(nums)


    calldata = easy_import_excel_file('Binary_Data.xlsx')
    for col in calldata:
        fill_blanks(calldata,col)



    # features_list = calldata.columns.values[7:56]
    # X = calldata.values[:,7:56]
    # Y = calldata.values[:,0]
    # Y = Y.astype('int')
    #
    # forest = RandomForestClassifier(oob_score=True, n_estimators=10000)
    # forest.fit(X,Y)
    # feature_importance = forest.feature_importances_
    #
    # feature_importance = 100.00 * (feature_importance / feature_importance.max())
    #
    # fi_threshold = 15
    #
    # important_ids = np.where(feature_importance > fi_threshold)[0]
    #
    # important_features = features_list[important_ids]
    #
    # print("n", important_features.shape[0], "Important features(>", fi_threshold, "% of max importance):n", important_features)
    #
    # sorted_ids = np.argsort(feature_importance[important_ids])[::-1]
    # print("nFeatures sorted by importance (DESC):n", important_features[sorted_ids])
    #
    # pos = np.arange(sorted_ids.shape[0])+.5
    # plt.subplot(1,2,2)
    # plt.barh(pos,feature_importance[important_ids][sorted_ids[::-1]],align='center')
    # plt.yticks(pos, important_features[sorted_ids[::-1]])
    # plt.xlabel('Relative Importance')
    # plt.ylabel('Variable Importance')
    # plt.draw()
    # plt.show()
    #
    # X= X[:,important_ids][:,sorted_ids]

    features_list = calldata.columns.values[5:56]
    #print(features_list)
    print(type(features_list))
    features_list.tolist()
    X = calldata.values[:,5:56]
    Y = calldata.values[:,1]
    Y = Y.astype('int')
    model = ExtraTreesClassifier()
    model.fit(X,Y)
    S = []
    T = []
    for i in range(0,50):
        print(features_list[i],":",model.feature_importances_[i])
        S.append(features_list[i])
        T.append(model.feature_importances_[i])


    # forest = RandomForestClassifier(oob_score=True, n_estimators=10000)
    # forest.fit(X,Y)
    # feature_importance = forest.feature_importances_
    #
    # feature_importance = 100.00 * (feature_importance / feature_importance.max())
    #
    # fi_threshold = 15
    #
    # important_ids = np.where(feature_importance > fi_threshold)[0]
    #
    # important_features = features_list[important_ids]
    #
    # print("n", important_features.shape[0], "Important features(>", fi_threshold, "% of max importance):n", important_features)
    #
    # sorted_ids = np.argsort(feature_importance[important_ids])[::-1]
    # print("nFeatures sorted by importance (DESC):n", important_features[sorted_ids])
    #
    # pos = np.arange(sorted_ids.shape[0])+.5
    # plt.subplot(1,2,2)
    # plt.barh(pos,feature_importance[important_ids][sorted_ids[::-1]],align='center')
    # plt.yticks(pos, important_features[sorted_ids[::-1]])
    # plt.xlabel('Relative Importance')
    # plt.ylabel('Variable Importance')
    # plt.draw()
    # plt.show()

if __name__ == "__main__":
    main()
