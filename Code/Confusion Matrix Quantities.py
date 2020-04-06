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
    print(appendList)
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
    # test = pandas.read_csv("Excel & CSV Sheets/Forecasts/1-1-2019/TestforPrediction.csv")
    # saveFile = 'Excel & CSV Sheets/Forecasts/1-1-2019/Confusion Matrix Quantities.csv'

    # ##Grid layout
    # modeltypes = ["CutGF_50-50","CutGF_75-25","CutGF_Test","CutRan_50-50","CutRan_75-25",
    # "CutRan_Test","FullGF_50-50","FullGF_75-25","FullGF_Test","FullRan_50-50", "FullRan_75-25",
    # "FullRan_Test","Spatial_50-50","Spatial_75-25","Spatial_Test","Temporal_50-50","Temporal_75-25",
    # "Temporal_Test"]
    # dates = ["1/1/2019","2/4/2018","3/12/2017","3/17/2019","4/12/2019","4/22/2018","5/11/2019",
    #     "5/16/2017","7/9/2017","8/16/2018"]

    # for date in dates:
    #     for modeltype in modeltypes: 
    #         print(date, modeltype)
    #         filedate = date.replace("/", "-")
    #         filename = "Excel & CSV Sheets/Forecasts/"+filedate+"/TestingforPredictions/TestforPrediction_"+modeltype+".csv"
    #         if exists(filename):
    #             test = pandas.read_csv(filename)
    #             saveFile = "Excel & CSV Sheets/Forecasts/"+filedate+"/TestingforPredictions/Confusion Matrix Quantities.csv"
    #             matrix_quantities_grid(test, date,saveFile, modeltype)

    ##Hex layout
    # modeltypes = ["GF_50-50 Split","GF_75-25 Split","GF_Test","Ran_50-50 Split", "Ran_75-25 Split", "Ran_Test"]

    # forecast = pandas.read_csv("/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Forecasts/01-23-2020/Hex/TestingforPredictions/75-25 Split Test 4_Test2.csv")
    # # acc = pandas.read_csv("/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Forecast Accident Dates/01-23-2020 Forecast.csv")
    # saveFile = "/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Forecasts/01-23-2020/Hex/TestingforPredictions/75-25_Test42.csv"
    # modeltype = "75-25 Test 4"
    # matrix_quantities_hex(forecast, "1/23/2020", saveFile, modeltype)
    # exit()

    # modeltypes = ["TS_50-50 Split_Test1Forecast","TS_50-50 Split_Test2Forecast","TS_50-50 Split_Test3Forecast","TS_50-50 Split_Test4Forecast", "TS_50-50 Split_Test5Forecast", 
    # "TS_75-25 Split_Test1Forecast", "TS_75-25 Split_Test2Forecast", "TS_75-25 Split_Test3Forecast", "TS_75-25 Split_Test4Forecast", "TS_75-25 Split_Test5Forecast", 
    # "TS_NoSplit_Test1Forecast","TS_NoSplit_Test2Forecast", "TS_NoSplit_Test3Forecast", "TS_NoSplit_Test4Forecast", "TS_NoSplit_Test5Forecast"]
    filedates = ['01-19-2020','01-20-2020','01-21-2020','01-22-2020','01-24-2020','01-25-2020']

    # modeltypes = ["50-50 Split_Test1","50-50 Split_Test2","50-50 Split_Test3","50-50 Split_Test4","50-50 Split_Test5", 
    # "75-25 Split_Test1","75-25 Split_Test2","75-25 Split_Test3","75-25 Split_Test4","75-25 Split_Test5", 
    # "NoSplit_Test1","NoSplit_Test2","NoSplit_Test3","NoSplit_Test4","NoSplit_Test5"]
    modeltypes = ['50-50 Split_NoShuffle_', '50-50 Split_sureRandom_','75-25 Split_NoShuffle_', '75-25 Split_sureRandom_',
    'NoSplit_NoShuffle_', 'NoSplit_sureRandom_']
    # filedates = ['02-10-2020','02-11-2020','02-12-2020' ]

    for filedate in filedates:
        for modeltype in modeltypes: 
            # print(filedate, modeltype)
            # filedate = date.replace("/", "-")
            # filename = "Excel & CSV Sheets/Forecasts/"+filedate+"/Confusion Matrix/"+modeltype+"Test.csv"
            # filename = "Excel & CSV Sheets/Forecasts/"+filedate+"/Hex/Confusion Matrix/"+modeltype+".csv"
            filename = "/Users/peteway/Downloads/Work/Top 13 Predictions/Confusion Matrix/"+modeltype+filedate+".csv"
            print(filename)
            if exists(filename):
                test = pandas.read_csv(filename)
                # saveFile = "Excel & CSV Sheets/Forecasts/"+filedate+"/Hex/TestingforPredictions/Hex Confusion Matrix Quantities.csv"
                # saveFile = "Excel & CSV Sheets/Forecasts/"+filedate+"/Hex/Confusion Matrix/"+filedate+"_Rainy Hex Confusion Matrix Quantities.csv"
                saveFile = "/Users/peteway/Downloads/Work/Top 13 Predictions/Confusion Matrix/"+ filedate+ "Shuffle Hex Confusion Matrix Quantities.csv"

                date = filedate.replace("-", "/")
                matrix_quantities_hex(test, date,saveFile, modeltype)



if __name__ == "__main__":
    main()




