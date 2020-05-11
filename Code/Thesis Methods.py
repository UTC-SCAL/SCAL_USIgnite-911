"""
A general file to hold all of my misc methods I've made during my thesis research
"""
import pandas


def automatedModelAverageAggregator():
    """
    Method to read in all the files that have the model averages, and do an automated calculation of their column
    averages and placing them into a separate file
    """
    files = []

    columns = ['Model', 'Train_Acc', 'Train_Loss', 'Test_Acc', 'Test_Loss', 'AUC', 'TN', 'FP', 'FN', 'TP', 'Accuracy',
               'Precision', 'Recall', 'Specificity', 'FPR']

    averageFile = pandas.DataFrame(columns=columns)
    rowNum = 0

    for file in files:
        data = pandas.read_csv("../%s" % file)
        print(rowNum)
        if "Grid Fix" in file:
            if "FeatSelect" in file:
                modelName = "GF " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "GF " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Hour Shift" in file:
            if "FeatSelect" in file:
                modelName = "HS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "HS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Spatial Shift" in file:
            if "FeatSelect" in file:
                modelName = "SS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "SS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Total Shift" in file:
            if "FeatSelect" in file:
                modelName = "TS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "TS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        elif "Date Shift" in file:
            if "FeatSelect" in file:
                modelName = "DS " + file.split(" ")[4] + " FS T" + file.split(" ")[8]
            else:
                modelName = "DS " + file.split(" ")[4] + " T" + file.split(" ")[7]
        else:
            print("Model naming error")
            exit()

        averageFile.at[rowNum, "Model"] = modelName
        averageFile.at[rowNum, "Train_Acc"] = data.Train_Acc.mean()
        averageFile.at[rowNum, "Train_Loss"] = data.Train_Loss.mean()
        averageFile.at[rowNum, "Test_Acc"] = data.Test_Acc.mean()
        averageFile.at[rowNum, "Test_Loss"] = data.Test_Loss.mean()
        averageFile.at[rowNum, "AUC"] = data.AUC.mean()
        averageFile.at[rowNum, "TN"] = data.TN.mean()
        averageFile.at[rowNum, "FP"] = data.FP.mean()
        averageFile.at[rowNum, "FN"] = data.FN.mean()
        averageFile.at[rowNum, "TP"] = data.TP.mean()
        averageFile.at[rowNum, "Accuracy"] = data.Accuracy.mean()
        averageFile.at[rowNum, "Precision"] = data.Precision.mean()
        averageFile.at[rowNum, "Recall"] = data.Recall.mean()
        averageFile.at[rowNum, "Specificity"] = data.Specificity.mean()
        averageFile.at[rowNum, "FPR"] = data.FPR.mean()
        rowNum = rowNum + 1

    averageFile.to_excel("../Jeremy Thesis/Model Result Averages.xlsx")
