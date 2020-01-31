import pandas 
from os.path import exists

def matrix_quantities_grid(accForCompare, date, saveFile, modelType):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    print(modelType, date)
    for i, _ in enumerate(accForCompare.values):
        if accForCompare.Accident.values[i] == 0:
            if accForCompare.Forecast.values[i] == 0:
                tn += 1 
            elif accForCompare.Forecast.values[i] > 0:
                fp += 1
        elif accForCompare.Accident.values[i] > 0:
            if accForCompare.Forecast.values[i] == 0:
                fn += 1 
            elif accForCompare.Forecast.values[i] > 0:
                tp += 1
    try: 
        accuracy = (tn + tp) / (tp+tn+fp+fn)
    except: 
        accuracy = 0
    try: 
        precision = tp / (fp + tp)
    except: 
        precision = 0
    try: 
        recall = tp / (fn + tp)
    except: 
        recall = 0
    try: 
        fpr = fp / (tn + fp)
    except: 
        fpr = 0
    try:
        specificity = tn / (tn + fp)
    except: 
        specificity = 0

    appendList = [date, modelType, tp, tn, fp, fn, accuracy, precision, recall, fpr, specificity]

            # If the average holder file exists, import it. If not, create it.
    if exists(saveFile):
        saveFrame = pandas.read_csv(saveFile,
                                        usecols=['Date', "ModelType", 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'Precision', 'Recall', 'FPR', 'Specificity'])

    else:
        saveFrame = pandas.DataFrame(
            columns=['Date', "ModelType", 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'Precision', 'Recall', 'FPR', 'Specificity'])

    appendSeries = pandas.Series(appendList, index=saveFrame.columns)
    saveFrame = saveFrame.append(appendSeries, ignore_index=True)
    saveFrame.to_csv(saveFile, index=False)

def matrix_quantities_hex(accForCompare, date, saveFile, modelType):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    print(modelType, date)
    for i, _ in enumerate(accForCompare.values):
        if accForCompare.Accident.values[i] == 0:
            if accForCompare.Forecast.values[i] == 0:
                tn += 1 
            elif accForCompare.Forecast.values[i] > 0:
                fp += 1
        elif accForCompare.Accident.values[i] > 0:
            if accForCompare.Forecast.values[i] == 0:
                fn += 1 
            elif accForCompare.Forecast.values[i] > 0:
                tp += 1
    try: 
        accuracy = (tn + tp) / (tp+tn+fp+fn)
    except: 
        accuracy = 0
    try: 
        precision = tp / (fp + tp)
    except: 
        precision = 0
    try: 
        recall = tp / (fn + tp)
    except: 
        recall = 0
    try: 
        fpr = fp / (tn + fp)
    except: 
        fpr = 0
    try:
        specificity = tn / (tn + fp)
    except: 
        specificity = 0


    appendList = [date, modelType, tp, tn, fp, fn, accuracy, precision, recall, fpr, specificity]

            # If the average holder file exists, import it. If not, create it.
    if exists(saveFile):
        saveFrame = pandas.read_csv(saveFile,
                                        usecols=['Date', "ModelType", 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'Precision', 'Recall', 'FPR', 'Specificity'])

    else:
        saveFrame = pandas.DataFrame(
            columns=['Date', "ModelType", 'TP', 'TN', 'FP', 'FN', 'Accuracy', 'Precision', 'Recall', 'FPR', 'Specificity'])

    appendSeries = pandas.Series(appendList, index=saveFrame.columns)
    saveFrame = saveFrame.append(appendSeries, ignore_index=True)
    saveFrame.to_csv(saveFile, index=False)


def main (): 
    test = pandas.read_csv("Excel & CSV Sheets/Forecasts/1-1-2019/TestforPrediction.csv")
    saveFile = 'Excel & CSV Sheets/Forecasts/1-1-2019/Confusion Matrix Quantities.csv'

    ##Grid layout
    modeltypes = ["CutGF_50-50","CutGF_75-25","CutGF_Test","CutRan_50-50","CutRan_75-25",
    "CutRan_Test","FullGF_50-50","FullGF_75-25","FullGF_Test","FullRan_50-50", "FullRan_75-25",
    "FullRan_Test","Spatial_50-50","Spatial_75-25","Spatial_Test","Temporal_50-50","Temporal_75-25",
    "Temporal_Test"]
    dates = ["1/1/2019","2/4/2018","3/12/2017","3/17/2019","4/12/2019","4/22/2018","5/11/2019",
        "5/16/2017","7/9/2017","8/16/2018"]

    for date in dates:
        for modeltype in modeltypes: 
            print(date, modeltype)
            filedate = date.replace("/", "-")
            filename = "Excel & CSV Sheets/Forecasts/"+filedate+"/TestingforPredictions/TestforPrediction_"+modeltype+".csv"
            if exists(filename):
                test = pandas.read_csv(filename)
                saveFile = "Excel & CSV Sheets/Forecasts/"+filedate+"/TestingforPredictions/Confusion Matrix Quantities.csv"
                matrix_quantities_grid(test, date,saveFile, modeltype)

    ##Hex layout
    modeltypes = ["GF_50-50 Split","GF_75-25 Split","GF_Test","Ran_50-50 Split", "Ran_75-25 Split", "Ran_Test"]

    for date in dates:
        for modeltype in modeltypes: 
            print(date, modeltype)
            filedate = date.replace("/", "-")
            filename = "Excel & CSV Sheets/Forecasts/"+filedate+"/Hex/TestingforPredictions/"+modeltype+".csv"
            if exists(filename):
                test = pandas.read_csv(filename)
                saveFile = "Excel & CSV Sheets/Forecasts/"+filedate+"/Hex/TestingforPredictions/Hex Confusion Matrix Quantities.csv"
                matrix_quantities_hex(test, date,saveFile, modeltype)

if __name__ == "__main__":
    main()




